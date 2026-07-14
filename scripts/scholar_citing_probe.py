#!/usr/bin/env python3
"""Probe citing-author retrieval for one Scholar publication."""

import signal
from scholarly import scholarly

TARGET_CITES_ID = "14778966596409886909"
TIMEOUT_SECONDS = 8
MAX_ITEMS = 5


class ProbeTimeout(Exception):
    """Raised when an operation exceeds timeout."""


def _timeout_handler(_signum, _frame):
    raise ProbeTimeout(f"operation timed out after {TIMEOUT_SECONDS}s")


def with_timeout(label, fn):
    signal.alarm(TIMEOUT_SECONDS)
    try:
        return fn()
    except ProbeTimeout as exc:
        print(f"timeout_during_{label}: {exc}")
        raise
    finally:
        signal.alarm(0)


def main():
    signal.signal(signal.SIGALRM, _timeout_handler)

    print("building_query...")
    try:
        query = with_timeout(
            "search_pubs",
            lambda: scholarly.search_pubs(f"cites:{TARGET_CITES_ID}"),
        )
    except ProbeTimeout:
        return

    checked = 0
    for index in range(MAX_ITEMS):
        try:
            item = with_timeout("next", lambda: next(query))
        except ProbeTimeout:
            break
        except StopIteration:
            print("no_more_results")
            break

        bib = item.get("bib", {})
        title = bib.get("title", "")
        authors = bib.get("author", "")
        print(f"item_{index + 1}_title: {title}")
        print(f"item_{index + 1}_authors: {authors}")
        checked += 1

    print(f"checked_items: {checked}")


if __name__ == "__main__":
    main()
