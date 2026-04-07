<script setup>
import { ref } from 'vue';
import Header from '@/components/header.vue';
import { useAllTeachingMaterials } from '@/composables/useTeachingMaterials';

defineOptions({ name: 'TeachingPage' });

const teachingMaterials = useAllTeachingMaterials();
const imageErrors = ref({});

const markImageError = (slug) => {
  imageErrors.value[slug] = true;
};

const hasImageError = (slug) => !!imageErrors.value[slug];
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />

    <section class="container mx-auto px-4 py-12">
      <div class="max-w-6xl mx-auto">
        <h1 class="text-4xl font-bold mb-8">Teaching</h1>

        <div v-if="teachingMaterials.length" class="space-y-6">
          <article
            v-for="item in teachingMaterials"
            :key="item.slug"
            class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden border border-gray-200 dark:border-gray-700"
          >
            <RouterLink :to="item.route" class="block hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <div class="md:flex">
                <div class="md:w-1/3 w-full h-48 md:h-auto bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img
                    v-if="item.image && !hasImageError(item.slug)"
                    :src="item.image"
                    :alt="item.title"
                    class="w-full h-full object-cover"
                    @error="markImageError(item.slug)"
                  />
                  <div v-else class="text-gray-500">No image</div>
                </div>
                <div class="p-4 md:w-2/3">
                  <p class="text-xs uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Teaching
                    <span v-if="item.date"> • {{ item.date }}</span>
                  </p>
                  <h2 class="text-xl font-semibold mt-1">{{ item.title }}</h2>
                  <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ item.excerpt }}</p>
                  <div v-if="item.tags && item.tags.length" class="mt-3 flex flex-wrap gap-2">
                    <RouterLink
                      v-for="tag in item.tags"
                      :key="`${item.slug}-${tag}`"
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
          <p class="text-gray-600 dark:text-gray-300">No teaching materials found.</p>
        </div>
      </div>
    </section>
  </div>
</template>
