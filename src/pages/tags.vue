<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import Header from '@/components/header.vue';

defineOptions({ name: 'TagsPage' });

const route = useRoute();

const normalizeTag = (value = '') => String(value).trim().toLowerCase();
const cleanTag = (value = '') => String(value).trim();

const parseFrontmatter = (content) => {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) return { metadata: {}, content };

  const frontmatter = match[1];
  const body = match[2];
  const metadata = {};
  let currentArrayKey = null;

  frontmatter.split('\n').forEach((line) => {
    const trimmedLine = line.trim();
    if (!trimmedLine) return;

    if (trimmedLine.startsWith('- ') && currentArrayKey) {
      if (!Array.isArray(metadata[currentArrayKey])) metadata[currentArrayKey] = [];
      metadata[currentArrayKey].push(trimmedLine.slice(2).replace(/^["']|["']$/g, '').trim());
      return;
    }

    currentArrayKey = null;
    const colonIndex = line.indexOf(':');
    if (colonIndex <= 0) return;

    const key = line.slice(0, colonIndex).trim();
    const rawValue = line.slice(colonIndex + 1).trim();

    if (!rawValue) {
      metadata[key] = [];
      currentArrayKey = key;
      return;
    }

    metadata[key] = rawValue.replace(/^["']|["']$/g, '').trim();
  });

  return { metadata, content: body };
};

const getExcerpt = (content, length = 160) => {
  const text = content
    .replace(/[#*`[\]]/g, '')
    .replace(/\((https?:\/\/[^)]+)\)/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  return text.length > length ? `${text.slice(0, length).trim()}...` : text;
};

const blogModules = import.meta.glob('@/posts/*.md', { as: 'raw', eager: true });
const paperModules = import.meta.glob('@/pages/papers/*.md', { as: 'raw', eager: true });
const projectModules = import.meta.glob('./projects/*.vue', { eager: true });
const experimentModules = import.meta.glob('./experiments/*/mainPage.vue', { eager: true });

const blogItems = Object.entries(blogModules)
  .map(([path, rawContent]) => {
    const filename = path.split('/').pop();
    const { metadata, content } = parseFrontmatter(rawContent.replace(/\r\n/g, '\n'));
    const tags = Array.isArray(metadata.tags) ? metadata.tags : metadata.tags ? [metadata.tags] : [];

    return {
      key: `blog-${filename}`,
      type: 'Blog',
      title: metadata.title || filename.replace('.md', ''),
      description: getExcerpt(content),
      image: null,
      tags: tags.map(cleanTag).filter(Boolean),
      to: { path: '/blog', query: { post: filename } },
    };
  })
  .filter((item) => item.tags.length);

const paperItems = Object.entries(paperModules)
  .map(([path, rawContent]) => {
    const slug = path.split('/').pop().replace('.md', '');
    const { metadata, content } = parseFrontmatter(rawContent.replace(/\r\n/g, '\n'));
    const tags = Array.isArray(metadata.tags) ? metadata.tags : metadata.tags ? [metadata.tags] : [];

    return {
      key: `paper-${slug}`,
      type: 'Paper',
      title: metadata.title || slug,
      description: getExcerpt(content),
      image: null,
      tags: tags.map(cleanTag).filter(Boolean),
      to: { path: `/papers/${slug}` },
    };
  })
  .filter((item) => item.tags.length);

const projectItems = Object.entries(projectModules)
  .map(([path, mod]) => {
    const name = path.split('/').pop().replace('.vue', '');
    const meta = mod.meta || mod.default?.meta || {};
    const tags = Array.isArray(meta.tags) ? meta.tags : [];
    let image = meta.image || meta.thumbnail || null;
    if (image && image.default) image = image.default;

    return {
      key: `project-${name}`,
      type: 'Project',
      title: meta.title || name,
      description: meta.description || '',
      image,
      tags: tags.map(cleanTag).filter(Boolean),
      to: { path: `/projects/${name}` },
    };
  })
  .filter((item) => item.tags.length);

const experimentItems = Object.entries(experimentModules)
  .map(([path, mod]) => {
    const parts = path.split('/');
    const name = parts[2] || path;
    const meta = mod.meta || mod.default?.meta || {};
    const tags = Array.isArray(meta.tags) ? meta.tags : [];
    let image = meta.image || meta.thumbnail || null;
    if (image && image.default) image = image.default;

    return {
      key: `experiment-${name}`,
      type: 'Experiment',
      title: meta.title || name,
      description: meta.description || '',
      image,
      tags: tags.map(cleanTag).filter(Boolean),
      to: { path: `/experiments/${name}` },
    };
  })
  .filter((item) => item.tags.length);

const allItems = [...paperItems, ...projectItems, ...experimentItems, ...blogItems];

const selectedTag = computed(() => cleanTag(route.params.tag || ''));
const selectedTagNormalized = computed(() => normalizeTag(route.params.tag || ''));

const filteredItems = computed(() => allItems.filter((item) => item.tags.some((tag) => normalizeTag(tag) === selectedTagNormalized.value)));
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />

    <section class="container mx-auto px-4 py-12">
      <div class="max-w-5xl mx-auto">
        <h1 class="text-3xl font-semibold text-center">Tag: {{ selectedTag }}</h1>
        <p class="mt-3 text-center text-gray-600 dark:text-gray-300">
          Showing papers, projects, experiments, and blog posts with this tag.
        </p>

        <div v-if="filteredItems.length" class="mt-10 space-y-6">
          <article
            v-for="item in filteredItems"
            :key="item.key"
            class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden border border-gray-200 dark:border-gray-700"
          >
            <RouterLink :to="item.to" class="block hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <div class="md:flex">
                <div class="md:w-1/3 w-full h-48 md:h-auto bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img v-if="item.image" :src="item.image" :alt="item.title" class="w-full h-full object-cover" />
                  <div v-else class="text-gray-500">No image</div>
                </div>
                <div class="p-4 md:w-2/3">
                  <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">{{ item.type }}</p>
                  <h2 class="text-xl font-semibold mt-1">{{ item.title }}</h2>
                  <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ item.description }}</p>
                  <div v-if="item.tags.length" class="mt-3 flex flex-wrap gap-2">
                    <RouterLink
                      v-for="tag in item.tags"
                      :key="`${item.key}-${tag}`"
                      :to="{ name: 'tags', params: { tag } }"
                      class="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
                      @click.stop
                    >
                      {{ tag }}
                    </RouterLink>
                  </div>
                </div>
              </div>
            </RouterLink>
          </article>
        </div>

        <div v-else class="mt-12 text-center">
          <p class="text-gray-600 dark:text-gray-300">No papers, projects, experiments, or blog posts found for this tag.</p>
        </div>
      </div>
    </section>
  </div>
</template>
