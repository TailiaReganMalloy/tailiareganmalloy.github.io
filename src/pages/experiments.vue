<script setup>
// Header nav like index page
import Header from '@/components/header.vue'

// Load all experiments from subfolders: ./experiments/<name>/index.vue
// Each index.vue can optionally export a `meta` named export or default.meta
const experimentModules = import.meta.glob('./experiments/*/mainPage.vue', { eager: true })

const experiments = Object.entries(experimentModules).map(([path, mod]) => {
  // Example path: './experiments/foo/index.vue' -> name = 'foo'
  const parts = path.split('/')
  const name = parts[2] || path

  const meta = mod.meta || mod.default?.meta || {}
  const title = meta.title || name.replace(/[-_]/g, ' ')
  let image = meta.image || meta.thumbnail || null
  if (image && image.default) image = image.default
  const description = meta.description || ''
  const route = `/experiments/${name}`

  return { name, title, image, description, route }
})

defineOptions({ name: 'ExperimentsPage' })
</script>


<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <!-- Header nav (no particles background) -->
    <Header />

    <!-- Experiments listing -->
    <section class="container mx-auto px-4 py-20">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-semibold text-center">Experiments</h2>
        <p class="mt-4 text-center text-gray-600 dark:text-gray-300">
          Explore interactive experiments and demos. 
        </p>

        <div class="mt-10 grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          <template v-for="exp in experiments" :key="exp.name">
            <article class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden">
              <a :href="exp.route" class="block">
                <div class="w-full h-48 bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img v-if="exp.image" :src="exp.image" :alt="exp.title" class="w-full h-full object-cover" />
                  <div v-else class="text-gray-500">No image</div>
                </div>
              </a>
              <div class="p-4">
                <h3 class="text-lg font-semibold">
                  <a :href="exp.route" class="hover:underline">{{ exp.title }}</a>
                </h3>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ exp.description }}</p>
              </div>
            </article>
          </template>
        </div>
      </div>
    </section>
  </div>
  
</template>
