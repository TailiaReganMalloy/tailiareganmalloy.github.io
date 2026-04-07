
<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />
    <div class="max-w-3xl mx-auto py-12 px-4">
      <div v-if="!showDetail">
        <img
          :src="meta.image"
          alt="Cybersecurity"
          class="w-full h-64 object-cover rounded mb-6 cursor-pointer"
          @click="showDetail = true"
        />
        <h1 class="text-3xl font-bold mb-6 text-center">{{ meta.title }}</h1>
        <p class="text-lg text-gray-700 dark:text-gray-300 mb-4 text-center">{{ meta.description }}</p>
        <div v-if="meta.tags && meta.tags.length" class="mt-3 mb-4 flex flex-wrap justify-center gap-2">
          <RouterLink
            v-for="tag in meta.tags"
            :key="`cyber-${tag}`"
            :to="{ name: 'tags', params: { tag } }"
            class="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
          >
            {{ tag }}
          </RouterLink>
        </div>
      </div>
      <div v-else>
        <div class="flex flex-col items-center mb-8">
          <img
            :src="meta.image"
            alt="Cybersecurity"
            class="w-full h-64 object-cover rounded mb-4"
          />
          <h1 class="text-3xl font-bold mb-2 text-center">{{ meta.title }}</h1>
          <div v-if="meta.tags && meta.tags.length" class="mt-2 flex flex-wrap justify-center gap-2">
            <RouterLink
              v-for="tag in meta.tags"
              :key="`cyber-detail-${tag}`"
              :to="{ name: 'tags', params: { tag } }"
              class="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded hover:bg-gray-300 dark:hover:bg-gray-600"
            >
              {{ tag }}
            </RouterLink>
          </div>
        </div>
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-2">Description</h2>
          <p class="text-gray-700 dark:text-gray-300">{{ meta.description }}</p>
        </div>
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-2">Papers</h2>
          <div v-if="projectPapers.length" class="mt-4 grid gap-8 grid-cols-1 sm:grid-cols-2">
            <article
              v-for="paper in projectPapers"
              :key="paper.slug"
              class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden"
            >
              <RouterLink :to="{ name: 'paper', params: { slug: paper.slug } }" class="block">
                <div class="w-full h-48 bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img v-if="paper.image" :src="paper.image" :alt="paper.title" class="w-full h-full object-cover" />
                  <div v-else class="text-gray-500">No image</div>
                </div>
              </RouterLink>
              <div class="p-4">
                <h3 class="text-lg font-semibold">
                  <RouterLink :to="{ name: 'paper', params: { slug: paper.slug } }" class="hover:underline">
                    {{ paper.title }}
                  </RouterLink>
                </h3>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ paper.excerpt }}</p>
              </div>
            </article>
          </div>
          <p v-else class="text-gray-700 dark:text-gray-300">No papers listed for this project yet.</p>
        </div>
        <div>
          <h2 class="text-xl font-semibold mb-2">References</h2>
          <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300">
            <li><a href="https://www.usenix.org/conference/usenixsecurity23/presentation/lee" target="_blank" class="text-blue-600 hover:underline">Phishing Detection Research (USENIX Security 2023)</a></li>
            <li><a href="https://www.microsoft.com/en-us/security/business/security-intelligence/phishing" target="_blank" class="text-blue-600 hover:underline">Microsoft Security Intelligence: Phishing</a></li>
            <li><a href="https://www.ncsc.gov.uk/guidance/phishing" target="_blank" class="text-blue-600 hover:underline">UK National Cyber Security Centre: Phishing Guidance</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// Project meta info for project listing
import cyberSecurityImage from '@/assets/img/CyberSecurity.png';

export const meta = {
  title: 'Cybersecurity',
  image: cyberSecurityImage,
  description: 'Project related to cybersecurity in the areas of anti-phishing training and AI recommendation systems for network analysis.',
  tags: ['Cybersecurity', 'LLM', 'Human-AI']
}
</script>

<script setup>
import { ref } from 'vue';
import Header from '@/components/header.vue';
import { useProjectPapers } from '@/composables/useProjectPapers';

const showDetail = ref(true);
const projectPapers = useProjectPapers('cyberSecurity');
</script>
