<script setup>
import { computed, ref } from 'vue';
import Header from '@/components/header.vue';
import { useAllPapers } from '@/composables/useProjectPapers';

defineOptions({ name: 'PapersPage' });

const papers = useAllPapers();
const filterMode = ref('none'); // none | year | project | tag
const selectedValue = ref('all');

const years = computed(() => [...new Set(papers.value.map((p) => p.year).filter(Boolean))].sort((a, b) => b.localeCompare(a)));
const projects = computed(() => [...new Set(papers.value.flatMap((p) => p.projects || []).filter(Boolean))].sort((a, b) => a.localeCompare(b)));
const tags = computed(() => [...new Set(papers.value.flatMap((p) => p.tags || []).filter(Boolean))].sort((a, b) => a.localeCompare(b)));

const availableOptions = computed(() => {
  if (filterMode.value === 'year') return years.value;
  if (filterMode.value === 'project') return projects.value;
  if (filterMode.value === 'tag') return tags.value;
  return [];
});

const filteredPapers = computed(() => {
  if (filterMode.value === 'none' || selectedValue.value === 'all') return papers.value;

  if (filterMode.value === 'year') {
    return papers.value.filter((paper) => paper.year === selectedValue.value);
  }

  if (filterMode.value === 'project') {
    return papers.value.filter((paper) => (paper.projects || []).includes(selectedValue.value));
  }

  if (filterMode.value === 'tag') {
    const normalized = selectedValue.value.trim().toLowerCase();
    return papers.value.filter((paper) => (paper.tags || []).some((tag) => tag.trim().toLowerCase() === normalized));
  }

  return papers.value;
});

const setFilterMode = (mode) => {
  filterMode.value = mode;
  selectedValue.value = 'all';
};

const formatProjectLabel = (project) => {
  if (project === 'generativeAI') return 'Generative AI';
  if (project === 'cognitiveModeling') return 'Cognitive Modeling';
  if (project === 'CyberSecurityPage') return 'Cybersecurity';
  return project;
};
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />

    <section class="container mx-auto px-4 py-12">
      <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-bold mb-8">Papers</h1>

        <div class="mb-6 flex flex-wrap items-center gap-2">
          <span class="text-sm font-medium text-gray-700 dark:text-gray-200">Filter by:</span>
          <button
            @click="setFilterMode('none')"
            :class="['px-3 py-1 rounded text-sm', filterMode === 'none' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            All
          </button>
          <button
            @click="setFilterMode('year')"
            :class="['px-3 py-1 rounded text-sm', filterMode === 'year' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            Year
          </button>
          <button
            @click="setFilterMode('project')"
            :class="['px-3 py-1 rounded text-sm', filterMode === 'project' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            Project
          </button>
          <button
            @click="setFilterMode('tag')"
            :class="['px-3 py-1 rounded text-sm', filterMode === 'tag' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            Tag
          </button>
        </div>

        <div v-if="filterMode !== 'none'" class="mb-8 flex flex-wrap gap-2">
          <button
            @click="selectedValue = 'all'"
            :class="['px-3 py-1 rounded text-sm', selectedValue === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            All
          </button>
          <button
            v-for="option in availableOptions"
            :key="option"
            @click="selectedValue = option"
            :class="['px-3 py-1 rounded text-sm', selectedValue === option ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600']"
          >
            {{ filterMode === 'project' ? formatProjectLabel(option) : option }}
          </button>
        </div>

        <div v-if="filteredPapers.length" class="space-y-6">
          <article
            v-for="paper in filteredPapers"
            :key="paper.slug"
            class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden border border-gray-200 dark:border-gray-700"
          >
            <RouterLink :to="paper.route" class="block hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <div class="md:flex">
                <div class="md:w-1/3 w-full h-48 md:h-auto bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img v-if="paper.image" :src="paper.image" :alt="paper.title" class="w-full h-full object-cover" />
                  <div v-else class="text-gray-500">No image</div>
                </div>
                <div class="p-4 md:w-2/3">
                  <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">Paper • {{ paper.year }}</p>
                  <h2 class="text-xl font-semibold mt-1">{{ paper.title }}</h2>
                  <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ paper.excerpt }}</p>
                  <div v-if="paper.tags && paper.tags.length" class="mt-3 flex flex-wrap gap-2">
                    <RouterLink
                      v-for="tag in paper.tags"
                      :key="`${paper.slug}-${tag}`"
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

        <div v-else class="text-center py-12">
          <p class="text-gray-600 dark:text-gray-300">No papers found for this filter.</p>
        </div>
      </div>
    </section>
  </div>
</template>
