import { computed } from 'vue';

const teachingModules = import.meta.glob('@/pages/teaching/*.md', { as: 'raw', eager: true });
const teachingImageModules = import.meta.glob('@/assets/img/teaching/*.{png,jpg,jpeg,webp}', { eager: true });

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

const resolveTeachingImage = (slug) => {
  const imageEntry = Object.entries(teachingImageModules).find(([path]) => path.endsWith(`/${slug}.png`)
    || path.endsWith(`/${slug}.jpg`)
    || path.endsWith(`/${slug}.jpeg`)
    || path.endsWith(`/${slug}.webp`));

  if (!imageEntry) return null;
  const imageModule = imageEntry[1];
  return imageModule?.default || imageModule || null;
};

const parseTeachingMaterial = (path, rawContent) => {
  const slug = path.split('/').pop().replace('.md', '');
  const normalizedContent = rawContent.replace(/\r\n/g, '\n');
  const { metadata, body } = parseFrontmatter(normalizedContent);
  const lines = body.split('\n');
  const firstContentLine = lines.findIndex((line) => line.trim() !== '');

  if (firstContentLine === -1) {
    return null;
  }

  const firstNonEmpty = lines[firstContentLine].trim();
  const inferredTitle = cleanText(firstNonEmpty.replace(/^#+\s*/, ''));
  const bodyContent = lines.slice(firstContentLine + 1).join('\n').trim();
  const tags = Array.isArray(metadata.tags)
    ? metadata.tags.map((tag) => cleanText(tag)).filter(Boolean)
    : metadata.tags
      ? [cleanText(metadata.tags)].filter(Boolean)
      : [];

  return {
    slug,
    title: cleanText(metadata.title || inferredTitle || slug),
    date: metadata.date || '',
    tags,
    excerpt: getExcerpt(bodyContent),
    image: resolveTeachingImage(slug) || `/img/teaching/${slug}.png`,
    route: `/teaching/${slug}`,
  };
};

const allTeachingMaterials = Object.entries(teachingModules)
  .map(([path, content]) => parseTeachingMaterial(path, content))
  .filter(Boolean);

export const useAllTeachingMaterials = () => computed(() => [...allTeachingMaterials].sort((a, b) => b.slug.localeCompare(a.slug)));
