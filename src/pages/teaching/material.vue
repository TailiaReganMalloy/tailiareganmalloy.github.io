<script setup>
import { computed, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import Header from '@/components/header.vue';

defineOptions({ name: 'TeachingMaterialPage' });

const route = useRoute();
const imageFailed = ref(false);

watch(() => route.params.slug, () => {
  imageFailed.value = false;
});
const teachingModules = import.meta.glob('@/pages/teaching/*.md', { as: 'raw', eager: true });
const teachingImageModules = import.meta.glob('@/assets/img/teaching/*.{png,jpg,jpeg,webp}', { eager: true });

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
      metadata[currentArrayKey].push(trimmedLine.slice(2).replace(/^['"]|['"]$/g, '').trim());
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

    metadata[key] = rawValue.replace(/^['"]|['"]$/g, '').trim();
  });

  return { metadata, content: body };
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return Number.isNaN(date.getTime())
    ? ''
    : date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
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

const renderMarkdown = (markdown) => {
  if (!markdown) return '';

  let html = markdown;

  html = html.replace(/^### (.*$)/gim, '<h3 class="text-xl font-semibold mt-6 mb-3">$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold mt-8 mb-4">$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mt-8 mb-4">$1</h1>');

  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.+?)_/g, '<em>$1</em>');

  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">$1</a>');

  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-100 dark:bg-gray-800 p-4 rounded my-4 overflow-x-auto"><code>$1</code></pre>');
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">$1</code>');

  html = html.replace(/^- (.+)$/gim, '<li class="ml-6">$1</li>');
  html = html.replace(/(<li.*<\/li>)/s, '<ul class="list-disc my-4">$1</ul>');

  html = html
    .split('\n\n')
    .map((para) => {
      const trimmed = para.trim();
      if (trimmed && !trimmed.startsWith('<')) {
        return `<p class="mb-4">${trimmed}</p>`;
      }
      return trimmed;
    })
    .join('\n');

  return html;
};

const teachingMaterial = computed(() => {
  const slug = String(route.params.slug || '');
  const key = Object.keys(teachingModules).find((path) => path.endsWith(`/${slug}.md`));

  if (!key) return null;

  const raw = teachingModules[key].replace(/\r\n/g, '\n');
  const { metadata, content } = parseFrontmatter(raw);
  const lines = content.split('\n');
  const firstNonEmpty = lines.find((line) => line.trim() !== '') || '';
  const inferredTitle = firstNonEmpty.replace(/^#+\s*/, '').trim();

  return {
    slug,
    title: metadata.title || inferredTitle || slug,
    date: metadata.date || '',
    tags: Array.isArray(metadata.tags) ? metadata.tags : [],
    content,
    image: resolveTeachingImage(slug) || `/img/teaching/${slug}.png`,
  };
});
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />

    <div class="max-w-4xl mx-auto px-4 py-8">
      <template v-if="teachingMaterial">
        <RouterLink :to="{ name: 'teaching' }" class="mb-6 text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-2">
          ← Back to teaching
        </RouterLink>

        <article class="teaching-content">
          <div v-if="teachingMaterial.image && !imageFailed" class="mb-6 rounded overflow-hidden border border-gray-200 dark:border-gray-700">
            <img
              :src="teachingMaterial.image"
              :alt="teachingMaterial.title"
              class="w-full h-auto object-cover"
              @error="imageFailed = true"
            />
          </div>

          <h1 class="text-4xl font-bold mb-4">{{ teachingMaterial.title }}</h1>
          <p v-if="teachingMaterial.date" class="text-gray-600 dark:text-gray-400 mb-6">
            {{ formatDate(teachingMaterial.date) }}
          </p>
          <div v-if="teachingMaterial.tags && teachingMaterial.tags.length" class="mb-6 flex flex-wrap gap-2">
            <RouterLink
              v-for="tag in teachingMaterial.tags"
              :key="tag"
              :to="{ name: 'tags', params: { tag } }"
              class="text-sm bg-gray-200 dark:bg-gray-700 px-3 py-1 rounded"
            >
              {{ tag }}
            </RouterLink>
          </div>
          <div class="prose dark:prose-invert max-w-none" v-html="renderMarkdown(teachingMaterial.content)" />
        </article>
      </template>

      <div v-else class="text-center py-12">
        <h1 class="text-3xl font-bold mb-4">Teaching material not found</h1>
        <RouterLink :to="{ name: 'teaching' }" class="text-blue-600 dark:text-blue-400 hover:underline">
          Back to teaching
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.teaching-content :deep(h1),
.teaching-content :deep(h2),
.teaching-content :deep(h3) {
  color: inherit;
}

.teaching-content :deep(a) {
  word-break: break-word;
}

.teaching-content :deep(pre) {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.teaching-content :deep(code) {
  font-size: 0.9em;
  font-family: 'Courier New', Courier, monospace;
}

.teaching-content :deep(ul) {
  padding-left: 1.5rem;
}

.teaching-content :deep(li) {
  margin-bottom: 0.5rem;
}
</style>
