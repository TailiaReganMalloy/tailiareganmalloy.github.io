import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/index.vue';
import CVPage from './pages/cv.vue';
import CvpdfPage from './pages/cvpdf.vue';
import BlogPage from './pages/blog.vue';
import AntiPhishingPage from './pages/projects/antiPhishing.vue';
import CognitiveModelingPage from './pages/projects/cognitiveModeling.vue';
import ExperimentsPage from './pages/experiments.vue';

// Dynamically import all experiment-specific route definition files.
// Each file at ./pages/experiments/<experiment>/routes.js should export either:
//   export default [ { path, name, component }, ... ]
// or a named export `routes` with the same array.
// These will be concatenated to the base routes below.
const experimentRouteModules = import.meta.glob('./pages/experiments/*/routes.js', { eager: true });

const experimentRoutes = Object.values(experimentRouteModules).flatMap(mod => {
  // Support both default export (array) and named export `routes`.
  const candidate = (mod.routes || mod.default || []);
  return Array.isArray(candidate) ? candidate : [];
});

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/cv', name: 'Cv', component: CVPage },
  { path: '/cvpdf', name: 'Cvpdf', component: CvpdfPage },
  { path: '/blog', name: 'Blog', component: BlogPage },
  { path: '/projects/antiPhishing', name: 'AntiPhishing', component: AntiPhishingPage },
  { path: '/projects/cognitiveModeling', name: 'CognitiveModeling', component: CognitiveModelingPage },
  { path: '/experiments', name: 'experimentsPage', component: ExperimentsPage },
  // Spread in dynamically discovered experiment routes
  ...experimentRoutes
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_PUBLIC_PATH),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth' }
    }
    return savedPosition || { top: 0 }
  }
});

export default router;