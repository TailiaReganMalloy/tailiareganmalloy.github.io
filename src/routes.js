import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/index.vue';
import CVPage from './pages/cv.vue';
import CvpdfPage from './pages/cvpdf.vue'
import BlogPage from './pages/blog.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PUBLIC_PATH),
  routes: [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/cv', name: 'Cv', component: CVPage },
    { path: '/cvpdf', name: 'Cvpdf', component: CvpdfPage },
    { path: '/blog', name: 'Blog', component: BlogPage}
  ],
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return savedPosition || { top: 0 }
  }
});

export default router;