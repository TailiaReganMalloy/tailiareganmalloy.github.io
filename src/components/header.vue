<script setup>
// @ts-ignore
defineOptions({ name: 'HeaderComponent' })

//import { ref } from 'vue'
import useTheme from '@/composables/useTheme.js'
const { currentTheme, switchTheme } = useTheme()
//import useLocale from '@/composables/useLocale.js'
//const { currentLocale, setLocale, supported } = useLocale()
import { useRouter } from 'vue-router'
const router = useRouter()
  /*
  const showLocales = ref(false)
    function selectLocale(loc) {
    showLocales.value = false
    setLocale(loc)
    if(currentLocale == "None"){
      setLocale("en")
    }
  }
  */


function goToSection(hash) {
  // navigate to home with hash
  router.push({ path: '/', hash })
}
</script>

<template>
  <header class="relative inset-x-0 top-0 z-20">
    <div class="container mx-auto flex justify-between items-center p-4">
      <h1 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Tailia Malloy</h1>
      <nav>
        <ul class="flex space-x-6 text-gray-700 dark:text-gray-200">
          <li><a href="/" class="hover:underline">Home</a></li>
          <li><button @click.prevent="goToSection('#about')" class="hover:underline">About</button></li>
          <li><button @click.prevent="goToSection('#projects')" class="hover:underline">Projects</button></li>
          <li><a href="/blog" class="hover:underline">Blog</a></li>
          <li><a href="/cv" class="hover:underline">CV</a></li>
          <li><a href="/experiments" class="hover:underline">Experiments</a></li>
        </ul>
      </nav>
  <div class="flex items-center space-x-2">
        <!-- Locale selector 
        <div class="relative" @mouseleave="showLocales = false">
          <button class="overflow-hidden p-2" @mouseenter="showLocales = true">
            <i class="fa-solid fa-globe"></i>
          </button>
          <div v-if="showLocales" class="absolute right-0 mt-2 w-24 bg-white dark:bg-gray-800 border rounded shadow-lg py-1 text-sm">
            <button v-for="loc in supported" :key="loc" @click="selectLocale(loc)" class="w-full text-left px-3 py-1 hover:bg-gray-100 dark:hover:bg-gray-700">
              {{ loc }}
            </button>
          </div>
        </div>
        -->

        <button class="overflow-hidden p-2" @click="switchTheme">
        <transition
          enter-active-class="transition duration-200 ease-out"
          leave-active-class="transition duration-200 ease-in"
          :enter-from-class="currentTheme === 'dark' ? 'transform -translate-y-full scale-50 opacity-0' : 'transform translate-y-full scale-50 opacity-0'"
          enter-to-class="transform translate-y-0"
          leave-from-class="transform translate-y-0"
          :leave-to-class="currentTheme === 'dark' ? 'transform translate-y-full scale-50 opacity-0' : 'transform -translate-y-full scale-50 opacity-0'"
          mode="out-in"
        >
          <svg
            v-if="currentTheme === 'dark'"
            xmlns="http://www.w3.org/2000/svg"
            class="size-8"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          >
            <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>

          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            class="size-8"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
          >
            <path d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </transition>
      </button>
      </div>
      
    </div>
  </header>
</template>

