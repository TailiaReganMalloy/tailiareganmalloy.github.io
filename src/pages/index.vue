<script setup>
// @ts-ignore
import Header from '@/components/header.vue'
import Particles from "@/components/particles.vue";

// Dynamically load all project pages in src/pages/projects/*.vue
// Each project page should export a `meta` named export with { title, image, description }
const projectModules = import.meta.glob('./projects/*.vue', { eager: true })
console.log('Project modules:', projectModules)
const projects = Object.entries(projectModules).map(([path, mod]) => {
  const name = path.split('/').pop().replace('.vue', '')
  const meta = mod.meta || mod.default?.meta || {}
  const title = meta.title || name.replace(/[-_]/g, ' ')
  let image = meta.image || meta.thumbnail || null
  if (image && image.default) image = image.default
  const description = meta.description || ''
  const route = `/projects/${name}`
  console.log('Project loaded:', { name, title, image, description, route, meta })
  return { name, title, image, description, route }
})
console.log('All projects:', projects)

defineOptions({ 
  name: 'HomePage'
})
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />

    <Particles>
      <main class="relative z-10 mx-auto flex h-full max-w-3xl flex-col items-center justify-center px-4 py-16 particles-slot-content">
        <h1 class="relative pb-20 text-center text-6xl text-gray-700 transition-colors dark:text-gray-100" style="padding-bottom:50vh; font-size:50pt">
          Tailia Malloy
        </h1>

        <h2 class="absolute pb-20 text-center text-6xl text-gray-700 transition-colors dark:text-gray-100" style="padding-bottom:25vh; font-size:25pt">
          Human and Machine Learning Research
        </h2>
      </main>
    </Particles>
    
    <!-- About section (anchor target) -->
    <section id="about" class="container mx-auto px-4 py-20">
      <div class="max-w-3xl mx-auto text-center">
        <h1 class="text-3xl font-semibold">About</h1>
        <p class="mt-6 text-gray-600 dark:text-gray-300 leading-relaxed">
          Hello! My name is Tailia Malloy. I am a researcher in human and machine learning. I am currently a postdoctoral researcher at the University of Luxembourg working under the advisement of <a href="https://scholar.google.com/citations?user=t73Mqm8AAAAJ&hl=en&oi=ao" target="_blank" rel="noopener" class="text-blue-600 hover:underline"> Professor Tegawendé F. Bissyandé</a> studying Human-Computer Interaction with a focus on LLM applications in software engineering and human resources. This is a joint research effort between the private HR technology company <a href="https://zortify.com/labs/" target="_blank" rel="noopener" class="text-blue-600 hover:underline">Zortify</a> and the <a href="https://www.uni.lu/snt-en/research-groups/trux/" target="_blank" rel="noopener" class="text-blue-600 hover:underline">Trustworthy Software Engineering (TruX) Lab</a>.
        </p>
      </div>
    </section>

    <!-- Projects section (anchor target) -->
    <section id="projects" class="container mx-auto px-4 py-20">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-semibold text-center">Projects</h2>
        <p class="mt-4 text-center text-gray-600 dark:text-gray-300">Visit back later for more information on my personal projects.</p>

        <div class="mt-10 grid gap-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          <template v-for="proj in projects" :key="proj.name">
            <article class="bg-white dark:bg-gray-800 shadow rounded overflow-hidden">
              <a :href="proj.route" class="block">
                <div class="w-full h-48 bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden">
                  <img v-if="proj.image" :src="proj.image" :alt="proj.title" class="w-full h-full object-cover" />
                  <div v-else class="text-gray-500">No image</div>
                </div>
              </a>
              <div class="p-4">
                <h3 class="text-lg font-semibold"><a :href="proj.route" class="hover:underline">{{ proj.title }}</a></h3>
                <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ proj.description }}</p>
              </div>
            </article>
          </template>
        </div>
      </div>
    </section>
  </div>
</template>
