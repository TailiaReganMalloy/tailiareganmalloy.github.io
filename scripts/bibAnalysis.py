#!/usr/bin/env python3
"""Compare Google Scholar citations and self-citations per publication.

This script fetches publications from a Google Scholar profile, estimates
self-citations by matching citing-paper author last names (default: malloy),
and outputs a stacked bar chart where:

- Blue segment = non-self citations
- Orange segment = self citations

Dependencies:
	pip install scholarly matplotlib

Example:
	python scripts/bibAnalysis.py \
	  --profile "https://scholar.google.com/citations?user=jktsx4EAAAAJ&hl=en"
"""

from __future__ import annotations

import argparse
import csv
import re
import signal
import sys
import time
import unicodedata
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator
from urllib.parse import parse_qs, urlparse

try:
	import matplotlib.pyplot as plt  # type: ignore[reportMissingImports]
except ImportError as exc:
	raise SystemExit(
		"matplotlib is required. Install with: pip install matplotlib"
	) from exc

try:
	from scholarly import scholarly  # type: ignore[reportMissingImports]
except ImportError as exc:
	raise SystemExit(
		"scholarly is required. Install with: pip install scholarly"
	) from exc


DEFAULT_PROFILE = "https://scholar.google.com/citations?user=jktsx4EAAAAJ&hl=en"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PNG_PATH = str(SCRIPT_DIR / "output" / "scholar_self_citation_chart.png")
DEFAULT_CSV_PATH = str(SCRIPT_DIR / "output" / "scholar_self_citation_counts.csv")
DEFAULT_SELF_LAST_NAME = "malloy"
DEFAULT_REQUEST_TIMEOUT_SECONDS = 25.0


class ScholarRequestTimeoutError(TimeoutError):
	"""Raised when a Scholar request exceeds timeout."""


@contextmanager
def time_limit(seconds: float | None) -> Iterator[None]:
	"""Limit execution time for a synchronous call (Unix only)."""
	if seconds is None or seconds <= 0:
		yield
		return

	if not hasattr(signal, "setitimer"):
		yield
		return

	def _handle_timeout(_signum: int, _frame: Any) -> None:
		raise ScholarRequestTimeoutError(f"Request timed out after {seconds:.1f} seconds")

	previous_handler = signal.getsignal(signal.SIGALRM)
	signal.signal(signal.SIGALRM, _handle_timeout)
	signal.setitimer(signal.ITIMER_REAL, seconds)
	try:
		yield
	finally:
		signal.setitimer(signal.ITIMER_REAL, 0)
		signal.signal(signal.SIGALRM, previous_handler)


def run_scholar_call(
	call_name: str,
	timeout_seconds: float | None,
	func: Callable[..., Any],
	*args: Any,
	**kwargs: Any,
) -> Any:
	"""Run a Scholar call with timeout and a clearer error context."""
	try:
		with time_limit(timeout_seconds):
			return func(*args, **kwargs)
	except ScholarRequestTimeoutError as exc:
		raise ScholarRequestTimeoutError(f"{call_name}: {exc}") from exc


@dataclass(frozen=True)
class PublicationCitationStats:
	"""Stores per-publication citation counts."""

	title: str
	year: str
	total_citations: int
	self_citations: int

	@property
	def non_self_citations(self) -> int:
		"""Return citations that are not self-citations."""
		return max(self.total_citations - self.self_citations, 0)


def parse_args() -> argparse.Namespace:
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description=(
			"Build a stacked bar chart of Google Scholar citations per "
			"publication (non-self in blue, self in orange)."
		)
	)
	parser.add_argument(
		"--profile",
		default=DEFAULT_PROFILE,
		help=(
			"Google Scholar profile URL or Scholar user id. "
			f"Default: {DEFAULT_PROFILE}"
		),
	)
	parser.add_argument(
		"--author-alias",
		action="append",
		default=[],
		help=(
			"Additional author alias used to infer possible self last names. "
			"Can be provided multiple times."
		),
	)
	parser.add_argument(
		"--self-last-name",
		action="append",
		default=[DEFAULT_SELF_LAST_NAME],
		help=(
			"Last name to treat as self-citation when it appears among citing "
			"authors. Can be provided multiple times. Default: malloy"
		),
	)
	parser.add_argument(
		"--min-citations",
		type=int,
		default=1,
		help="Only include publications with at least this many citations.",
	)
	parser.add_argument(
		"--max-papers",
		type=int,
		default=None,
		help="Optional limit on number of cited papers to process.",
	)
	parser.add_argument(
		"--max-citing-per-paper",
		type=int,
		default=None,
		help=(
			"Optional cap on citing papers inspected per publication. "
			"Useful for faster test runs."
		),
	)
	parser.add_argument(
		"--paper-title-contains",
		default=None,
		help=(
			"Only process publications whose title contains this text "
			"(case-insensitive)."
		),
	)
	parser.add_argument(
		"--debug-print-checked-authors",
		action="store_true",
		help=(
			"Print citing-paper author strings, parsed authors, parsed last names, "
			"and self-citation match decisions."
		),
	)
	parser.add_argument(
		"--sleep-seconds",
		type=float,
		default=0.35,
		help="Pause between Scholar requests to reduce rate-limit risk.",
	)
	parser.add_argument(
		"--request-timeout-seconds",
		type=float,
		default=DEFAULT_REQUEST_TIMEOUT_SECONDS,
		help=(
			"Timeout per Scholar request in seconds. Failed requests are skipped. "
			f"Default: {DEFAULT_REQUEST_TIMEOUT_SECONDS}"
		),
	)
	parser.add_argument(
		"--output",
		default=DEFAULT_PNG_PATH,
		help=f"Path for the output chart image. Default: {DEFAULT_PNG_PATH}",
	)
	parser.add_argument(
		"--csv-output",
		default=DEFAULT_CSV_PATH,
		help=f"Path for CSV output. Default: {DEFAULT_CSV_PATH}",
	)
	parser.add_argument(
		"--show",
		action="store_true",
		help="Display chart window in addition to saving image.",
	)
	return parser.parse_args()


def extract_scholar_id(profile_or_id: str) -> str:
	"""Extract Scholar user id from a profile URL, or return the input as id."""
	parsed = urlparse(profile_or_id)
	if parsed.scheme and parsed.netloc:
		user = parse_qs(parsed.query).get("user", [None])[0]
		if user:
			return user
		raise ValueError(
			"Could not find 'user=' parameter in the provided Google Scholar URL."
		)
	return profile_or_id.strip()


def strip_accents(text: str) -> str:
	"""Remove accents and diacritics from text."""
	normalized = unicodedata.normalize("NFKD", text)
	return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_name(name: str) -> str:
	"""Normalize author names for approximate matching."""
	text = strip_accents(name).casefold()
	text = re.sub(r"[^a-z\s]", " ", text)
	text = re.sub(r"\s+", " ", text).strip()
	return text


def extract_last_name(name: str) -> str | None:
	"""Extract a normalized last name token from a full author name."""
	normalized = normalize_name(name)
	if not normalized:
		return None
	parts = normalized.split()
	if not parts:
		return None
	return parts[-1]


def parse_author_list(raw_authors: str) -> list[str]:
	"""Parse Scholar author string into individual author names."""
	if not raw_authors:
		return []

	# Scholar data commonly uses comma separators and/or "and".
	normalized = re.sub(r"\band\b", ",", raw_authors, flags=re.IGNORECASE)
	parts = normalized.split(",")

	cleaned = [part.strip() for part in parts if part.strip()]
	return cleaned


def is_self_citation(raw_authors: str, self_last_names: set[str]) -> bool:
	"""Return True if any citing-paper author matches a self last name."""
	for author_name in parse_author_list(raw_authors):
		last_name = extract_last_name(author_name)
		if last_name is None:
			continue
		if last_name in self_last_names:
			return True
	return False


def self_citation_debug_details(
	raw_authors: str,
	self_last_names: set[str],
) -> tuple[bool, list[str], list[str]]:
	"""Return self-citation match plus parsed author/last-name details."""
	parsed_authors = parse_author_list(raw_authors)
	parsed_last_names: list[str] = []
	is_match = False

	for author_name in parsed_authors:
		last_name = extract_last_name(author_name)
		if last_name is None:
			continue
		parsed_last_names.append(last_name)
		if last_name in self_last_names:
			is_match = True

	return is_match, parsed_authors, parsed_last_names


def iter_with_limit(items: Iterable, limit: int | None) -> Iterator:
	"""Iterate over items with an optional maximum count."""
	for index, item in enumerate(items):
		if limit is not None and index >= limit:
			break
		yield item


def collect_publication_stats(
	scholar_id: str,
	aliases: list[str],
	self_last_names_input: list[str],
	min_citations: int,
	max_papers: int | None,
	max_citing_per_paper: int | None,
	paper_title_contains: str | None,
	debug_print_checked_authors: bool,
	sleep_seconds: float,
	request_timeout_seconds: float,
) -> tuple[list[PublicationCitationStats], str]:
	"""Fetch publication citation stats from Google Scholar."""
	try:
		author = run_scholar_call(
			"search_author_id",
			request_timeout_seconds,
			scholarly.search_author_id,
			scholar_id,
		)
	except Exception as exc:  # pragma: no cover - network behavior
		raise RuntimeError(f"Failed to load Scholar profile for id '{scholar_id}': {exc}") from exc

	# Publications are needed to inspect per-paper citations.
	author = run_scholar_call(
		"fill_author_profile",
		request_timeout_seconds,
		scholarly.fill,
		author,
		sections=["basics", "publications"],
	)

	profile_name = str(author.get("name", "")).strip() or scholar_id
	self_last_names = {
		normalized_last_name
		for last_name in self_last_names_input
		for normalized_last_name in [extract_last_name(last_name)]
		if normalized_last_name is not None
	}
	for alias in [profile_name, *aliases]:
		alias_last_name = extract_last_name(alias)
		if alias_last_name is not None:
			self_last_names.add(alias_last_name)
	if not self_last_names:
		self_last_names.add(DEFAULT_SELF_LAST_NAME)

	publications = author.get("publications", [])
	print(f"Loaded profile: {profile_name}")
	print(f"Publications discovered: {len(publications)}")
	print(f"Self-citation last-name match: {', '.join(sorted(self_last_names))}")
	if paper_title_contains:
		print(f"Paper title filter: {paper_title_contains}")

	normalized_title_filter = (
		normalize_name(paper_title_contains) if paper_title_contains else None
	)

	stats: list[PublicationCitationStats] = []
	for pub in publications:
		try:
			publication = run_scholar_call(
				"fill_publication",
				request_timeout_seconds,
				scholarly.fill,
				pub,
				sections=["bib", "indices"],
			)
		except Exception as exc:
			fallback_title = str(pub.get("bib", {}).get("title", "Untitled"))
			print(f"Skipping publication due to fetch error: {fallback_title[:90]} | {exc}")
			continue

		title = str(publication.get("bib", {}).get("title", "Untitled"))
		year = str(publication.get("bib", {}).get("pub_year", ""))
		total_citations = int(publication.get("num_citations", 0) or 0)

		if normalized_title_filter and normalized_title_filter not in normalize_name(title):
			continue

		if total_citations < min_citations:
			continue

		print(f"Processing: {title[:90]}")
		if max_citing_per_paper == 0:
			print(
				"  Info: max-citing-per-paper=0, skipping citing-paper fetch and "
				"using self_citations=0 for this paper."
			)
			stats.append(
				PublicationCitationStats(
					title=title,
					year=year,
					total_citations=total_citations,
					self_citations=0,
				)
			)
			if max_papers is not None and len(stats) >= max_papers:
				break
			continue

		try:
			citing_papers = run_scholar_call(
				"citedby",
				request_timeout_seconds,
				scholarly.citedby,
				publication,
			)
		except Exception as exc:
			print(
				"  Warning: failed to fetch citing papers; using self_citations=0 "
				f"for this paper. Reason: {exc}"
			)
			stats.append(
				PublicationCitationStats(
					title=title,
					year=year,
					total_citations=total_citations,
					self_citations=0,
				)
			)
			if max_papers is not None and len(stats) >= max_papers:
				break
			continue

		self_citations = 0
		inspected = 0

		while True:
			if max_citing_per_paper is not None and inspected >= max_citing_per_paper:
				break

			try:
				citing_pub = run_scholar_call(
					"next_citing_publication",
					request_timeout_seconds,
					next,
					citing_papers,
				)
			except StopIteration:
				break
			except Exception as exc:
				print(f"  Warning: failed while iterating citing papers, stopping early. Reason: {exc}")
				break

			try:
				inspected += 1
				filled_citing = run_scholar_call(
					"fill_citing_publication",
					request_timeout_seconds,
					scholarly.fill,
					citing_pub,
					sections=["bib"],
				)
				citing_authors = str(filled_citing.get("bib", {}).get("author", ""))
				is_match, parsed_authors, parsed_last_names = self_citation_debug_details(
					citing_authors,
					self_last_names,
				)
				if debug_print_checked_authors:
					print(f"    Checked citing authors raw: {citing_authors}")
					print(f"    Parsed citing authors: {parsed_authors}")
					print(f"    Parsed last names: {parsed_last_names}")
					print(f"    Self-citation match: {is_match}")
				if is_match:
					self_citations += 1
			except Exception as exc:
				print(f"  Warning: failed to fetch one citing paper, skipping. Reason: {exc}")
				continue
			finally:
				if sleep_seconds > 0:
					time.sleep(sleep_seconds)

		if debug_print_checked_authors and inspected == 0:
			print("    Debug: no citing author records were fetched for this paper.")

		if max_citing_per_paper is not None and total_citations > max_citing_per_paper:
			print(
				"  Warning: only a subset of citing papers was inspected; "
				"self-citation count is a lower-bound estimate."
			)

		print(
			f"  Citations: total={total_citations}, "
			f"self={self_citations}, non-self={max(total_citations - self_citations, 0)}, "
			f"inspected={inspected}"
		)

		stats.append(
			PublicationCitationStats(
				title=title,
				year=year,
				total_citations=total_citations,
				self_citations=self_citations,
			)
		)
		if max_papers is not None and len(stats) >= max_papers:
			break

	stats.sort(key=lambda item: item.total_citations, reverse=True)
	if max_papers is not None:
		stats = stats[:max_papers]

	return stats, profile_name


def shorten_title(title: str, max_len: int = 55) -> str:
	"""Shorten long titles for chart axis labels."""
	if len(title) <= max_len:
		return title
	return f"{title[: max_len - 3].rstrip()}..."


def save_csv(stats: list[PublicationCitationStats], csv_path: Path) -> None:
	"""Save per-publication citation counts to CSV."""
	csv_path.parent.mkdir(parents=True, exist_ok=True)
	with csv_path.open("w", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow(
			["title", "year", "total_citations", "self_citations", "non_self_citations"]
		)
		for item in stats:
			writer.writerow(
				[
					item.title,
					item.year,
					item.total_citations,
					item.self_citations,
					item.non_self_citations,
				]
			)


def save_plot(stats: list[PublicationCitationStats], profile_name: str, output_path: Path) -> None:
	"""Create and save a stacked bar chart (blue non-self, orange self)."""
	output_path.parent.mkdir(parents=True, exist_ok=True)

	labels = [shorten_title(item.title) for item in stats]
	non_self = [item.non_self_citations for item in stats]
	self_cites = [item.self_citations for item in stats]
	x_positions = list(range(len(stats)))

	width = max(12.0, len(stats) * 0.5)
	fig, ax = plt.subplots(figsize=(width, 8.5))
	ax.bar(x_positions, non_self, color="tab:blue", label="Non-self citations")
	ax.bar(
		x_positions,
		self_cites,
		bottom=non_self,
		color="tab:orange",
		label="Self citations",
	)

	ax.set_title(f"Citation Comparison by Publication: {profile_name}")
	ax.set_ylabel("Citations")
	ax.set_xlabel("Publications")
	ax.set_xticks(x_positions)
	ax.set_xticklabels(labels, rotation=70, ha="right", fontsize=8)
	ax.legend()
	ax.grid(axis="y", alpha=0.25)

	fig.tight_layout()
	fig.savefig(output_path, dpi=220)
	plt.close(fig)


def main() -> int:
	"""Entry point."""
	args = parse_args()

	try:
		scholar_id = extract_scholar_id(args.profile)
	except ValueError as exc:
		print(f"Error: {exc}")
		return 2

	try:
		stats, profile_name = collect_publication_stats(
			scholar_id=scholar_id,
			aliases=args.author_alias,
			self_last_names_input=args.self_last_name,
			min_citations=max(args.min_citations, 0),
			max_papers=args.max_papers,
			max_citing_per_paper=args.max_citing_per_paper,
			paper_title_contains=args.paper_title_contains,
			debug_print_checked_authors=args.debug_print_checked_authors,
			sleep_seconds=max(args.sleep_seconds, 0),
			request_timeout_seconds=max(args.request_timeout_seconds, 0),
		)
	except RuntimeError as exc:
		print(f"Error: {exc}")
		return 1
	except Exception as exc:  # pragma: no cover - network behavior
		print("Unexpected error while talking to Google Scholar.")
		print(
			"If prompted for CAPTCHA or blocked requests, wait a bit and retry "
			"with a larger --sleep-seconds value."
		)
		print(f"Details: {exc}")
		return 1

	if not stats:
		print("No publications met the citation threshold. Nothing to plot.")
		return 0

	output_path = Path(args.output)
	csv_path = Path(args.csv_output)

	save_csv(stats, csv_path)
	save_plot(stats, profile_name, output_path)

	total = sum(item.total_citations for item in stats)
	self_total = sum(item.self_citations for item in stats)
	non_self_total = sum(item.non_self_citations for item in stats)

	print("\nDone.")
	print(f"Chart saved to: {output_path}")
	print(f"CSV saved to:   {csv_path}")
	print(
		f"Included papers: {len(stats)} | "
		f"Total citations: {total} | "
		f"Self citations: {self_total} | "
		f"Non-self citations: {non_self_total}"
	)

	if args.show:
		# Reopen the saved chart for optional display in local runs.
		image = plt.imread(output_path)
		plt.figure(figsize=(10, 6))
		plt.imshow(image)
		plt.axis("off")
		plt.show()

	return 0


if __name__ == "__main__":
	sys.exit(main())
