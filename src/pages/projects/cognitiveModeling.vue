
<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />
    <div class="max-w-3xl mx-auto py-12 px-4">
      <div v-if="!showDetail">
        <img
          :src="meta.image"
          alt="Cognitive Modeling"
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
            alt="Cognitive Modeling"
            class="w-full h-64 object-cover rounded mb-4"
          />
          <h1 class="text-3xl font-bold mb-2 text-center">{{ meta.title }}</h1>
        </div>
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-2">Description</h2>
          <p class="text-gray-700 dark:text-gray-300 mb-4">
            Computational cognitive modeling combines psychological theory with computational methods to understand and simulate human cognition. 
            This project focuses on developing models that can predict human decision-making, learning, and problem-solving behaviors across various domains.
          </p>
          <p class="text-gray-700 dark:text-gray-300 mb-4">
            Our approach leverages instance-based learning theory, reinforcement learning, and other cognitive architectures to create 
            models that not only fit behavioral data but also provide insights into the underlying cognitive processes.
          </p>
          <p class="text-gray-700 dark:text-gray-300">
            Key areas of focus include:
          </p>
          <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300 mt-2">
            <li>Instance-Based Learning (IBL) models</li>
            <li>Cognitive architectures (ACT-R, IBLT)</li>
            <li>Decision-making under uncertainty</li>
            <li>Human-AI interaction and adaptation</li>
            <li>Individual differences in cognition</li>
          </ul>
        </div>
        <div>
          <h2 class="text-xl font-semibold mb-2">References</h2>
          <ul class="list-disc pl-6 text-gray-700 dark:text-gray-300">
            <li><a href="https://www.cmu.edu/dietrich/sds/ddmlab/index.html" target="_blank" class="text-blue-600 hover:underline">Dynamic Decision Making Laboratory - CMU</a></li>
            <li><a href="http://act-r.psy.cmu.edu/" target="_blank" class="text-blue-600 hover:underline">ACT-R Cognitive Architecture</a></li>
            <li><a href="https://www.sciencedirect.com/science/article/pii/S0010028511000910" target="_blank" class="text-blue-600 hover:underline">Instance-Based Learning Theory (Gonzalez et al., 2011)</a></li>
            <li><a href="https://psycnet.apa.org/record/2019-00310-001" target="_blank" class="text-blue-600 hover:underline">Cognitive Models of Human Decision Making</a></li>
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
import modelingImage from '@/assets/img/Modeling.png';

export const meta = {
  title: 'Computational Cognitive Modeling',
  image: modelingImage,
  description: 'Research focused on developing computational models of human cognition, decision-making, and learning using cognitive architectures and machine learning techniques.'
}
</script>

<script setup>
import { ref } from 'vue';
import Header from '@/components/header.vue';

const showDetail = ref(false);
</script>
