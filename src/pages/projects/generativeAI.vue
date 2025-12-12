
<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />
    <div class="max-w-3xl mx-auto py-12 px-4">
      <div v-if="!showDetail">
        <img
          :src="meta.image"
          alt="Generative AI"
          class="w-full h-64 object-cover rounded mb-6 cursor-pointer"
          @click="showDetail = true"
        />
        <h1 class="text-3xl font-bold mb-6 text-center">{{ meta.title }}</h1>
        <p class="text-lg text-gray-700 dark:text-gray-300 mb-4 text-center">{{ meta.description }}</p>
      </div>
      <div v-else>
        <div class="flex flex-col items-center mb-8">
          <img
            :src="meta.image"
            alt="Generative AI"
            class="w-full h-64 object-cover rounded mb-4"
          />
          <h1 class="text-3xl font-bold mb-2 text-center">{{ meta.title }}</h1>
        </div>
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-2">Description</h2>
          <p class="text-gray-700 dark:text-gray-300">{{ meta.description }}</p>
        </div>
        <div>
          <h2 class="text-xl font-semibold mb-2">References</h2>
          <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300">
            <li><a href="https://www.usenix.org/conference/usenixsecurity23/presentation/lee" target="_blank" class="text-blue-600 hover:underline">Phishing Detection Research (USENIX Security 2023)</a></li>
            <li><a href="https://www.microsoft.com/en-us/security/business/security-intelligence/phishing" target="_blank" class="text-blue-600 hover:underline">Microsoft Security Intelligence: Phishing</a></li>
            <li><a href="https://www.ncsc.gov.uk/guidance/phishing" target="_blank" class="text-blue-600 hover:underline">UK National Cyber Security Centre: Phishing Guidance</a></li>
          </ul>
        </div>
        <div class="mt-8 text-center">
          <button @click="showDetail = false" class="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600">Back</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
// Project meta info for project listing
import phishingImage from '@/assets/img/GenerativeAI.png';

export const meta = {
  title: 'Generative Artificial Intelligence',
  image: phishingImage,
  description: 'This research focuses on generative AI models including LLMs, visual based models like GANs and VEs, as well as multi-modal models.'
}
</script>

<script setup>
import { ref } from 'vue';
import Header from '@/components/header.vue';

const showDetail = ref(false);
</script>
