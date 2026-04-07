import { computed } from 'vue';

const paperModules = import.meta.glob('@/pages/papers/*.md', { as: 'raw', eager: true });
const paperImageModules = import.meta.glob('@/assets/img/papers/*.{png,jpg,jpeg,webp}', { eager: true });

const cleanText = (value = '') => value.replace(/\s+/g, ' ').trim();

const parseFrontmatter = (rawContent) => {
  const frontmatterMatch = rawContent.match(/^---\n([\s\S]*?)\n---\n?/);

  if (!frontmatterMatch) {
    return { metadata: {}, body: rawContent };
  }

  const frontmatter = frontmatterMatch[1];
  const body = rawContent.slice(frontmatterMatch[0].length);
  const metadata = {};
  let currentArrayKey = null;

  frontmatter.split('\n').forEach((line) => {
    const trimmedLine = line.trim();

    if (!trimmedLine) {
      return;
    }

    if (trimmedLine.startsWith('- ') && currentArrayKey) {
      metadata[currentArrayKey].push(cleanText(trimmedLine.slice(2)).replace(/^['"]|['"]$/g, ''));
      return;
    }

    currentArrayKey = null;
    const colonIndex = line.indexOf(':');

    if (colonIndex === -1) {
      return;
    }

    const key = line.slice(0, colonIndex).trim();
    const rawValue = line.slice(colonIndex + 1).trim();

    if (!rawValue) {
      metadata[key] = [];
      currentArrayKey = key;
      return;
    }

    metadata[key] = rawValue.replace(/^['"]|['"]$/g, '');
  });

  return { metadata, body };
};

const getExcerpt = (content, maxLength = 180) => {
  const withoutMarkdown = content
    .replace(/^#+\s+/gm, '')
    .replace(/[*_`[\]]/g, '')
    .replace(/\((https?:\/\/[^)]+)\)/g, '')
    .trim();

  if (!withoutMarkdown) return '';
  return withoutMarkdown.length > maxLength
    ? `${withoutMarkdown.slice(0, maxLength).trim()}...`
    : withoutMarkdown;
};

const resolvePaperImage = (slug) => {
  const imageEntry = Object.entries(paperImageModules).find(([path]) => path.endsWith(`/${slug}.png`)
    || path.endsWith(`/${slug}.jpg`)
    || path.endsWith(`/${slug}.jpeg`)
    || path.endsWith(`/${slug}.webp`));

  if (!imageEntry) return null;
  const imageModule = imageEntry[1];
  return imageModule?.default || imageModule || null;
};

const parsePaper = (path, rawContent) => {
  const slug = path.split('/').pop().replace('.md', '');
  const normalizedContent = rawContent.replace(/\r\n/g, '\n');
  const { metadata, body } = parseFrontmatter(normalizedContent);
  const lines = body.split('\n');
  const firstContentLine = lines.findIndex((line) => line.trim() !== '');

  if (firstContentLine === -1) {
    return null;
  }

  let projects = Array.isArray(metadata.projects)
    ? metadata.projects.map((project) => cleanText(project)).filter(Boolean)
    : [];
  let titleLineIndex = firstContentLine;
  const firstLine = lines[firstContentLine].trim();

  if (firstLine.toLowerCase().startsWith('projects ')) {
    projects = firstLine
      .slice('projects '.length)
      .split(',')
      .map((project) => cleanText(project))
      .filter(Boolean);

    titleLineIndex = lines.findIndex((line, index) => index > firstContentLine && line.trim() !== '');
  }

  const title = titleLineIndex > -1 ? lines[titleLineIndex].trim() : slug;
  const bodyContent = titleLineIndex > -1
    ? lines.slice(titleLineIndex + 1).join('\n').trim()
    : body.trim();

  const resolvedTitle = cleanText(metadata.title || title) || slug;
  const tags = Array.isArray(metadata.tags)
    ? metadata.tags.map((tag) => cleanText(tag)).filter(Boolean)
    : metadata.tags
      ? [cleanText(metadata.tags)].filter(Boolean)
      : [];
  const year = metadata.date ? String(metadata.date).slice(0, 4) : slug.slice(0, 4);

  return {
    slug,
    title: resolvedTitle,
    date: metadata.date || '',
    year,
    tags,
    projects,
    excerpt: getExcerpt(bodyContent),
    image: resolvePaperImage(slug),
    route: `/papers/${slug}`,
  };
};

const allPapers = Object.entries(paperModules)
  .map(([path, content]) => parsePaper(path, content))
  .filter(Boolean);

export const useAllPapers = () => computed(() => [...allPapers].sort((a, b) => b.slug.localeCompare(a.slug)));

export const useProjectPapers = (projectName) => computed(() => allPapers
  .filter((paper) => paper.projects.includes(projectName))
  .sort((a, b) => b.slug.localeCompare(a.slug)));
