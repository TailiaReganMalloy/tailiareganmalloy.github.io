import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/index.vue';
import CVPage from './pages/cv.vue';
import CvpdfPage from './pages/cvpdf.vue';
import BlogPage from './pages/blog.vue';
import PapersPage from './pages/papers.vue';
import PaperPage from './pages/papers/paper.vue';
import TeachingPage from './pages/teaching.vue';
import TeachingMaterialPage from './pages/teaching/material.vue';
import TagsPage from './pages/tags.vue';
import CyberSecurityPage from './pages/projects/cyberSecurity.vue';
import CognitiveModelingPage from './pages/projects/cognitiveModeling.vue';
import HumanComputerInteractionPage from './pages/projects/humanComputerInteraction.vue';
import LargeLanguageModelsPage from './pages/projects/largeLanguageModels.vue';
import VisualArtificialIntelligencePage from './pages/projects/visualArtificialIntelligence.vue';
import ReinforcementLearningPage from './pages/projects/reinforcementLearning.vue'; 
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
  { path: '/papers', name: 'papers', component: PapersPage },
  { path: '/papers/:slug', name: 'paper', component: PaperPage },
  { path: '/teaching', name: 'teaching', component: TeachingPage },
  { path: '/teaching/:slug', name: 'teaching-material', component: TeachingMaterialPage },
  { path: '/tags/:tag', name: 'tags', component: TagsPage },
  { path: '/projects/cognitiveModeling', name: 'cognitiveModeling', component: CognitiveModelingPage },
  { path: '/projects/cyberSecurity', name: 'cyberSecurity', component:  CyberSecurityPage},
  { path: '/projects/humanComputerInteraction', name: 'humanComputerInteraction', component: HumanComputerInteractionPage },
  { path: '/projects/largeLanguageModels', name: 'largeLanguageModels', component:  LargeLanguageModelsPage},
  { path: '/projects/reinforcementLearning', name: 'reinforcementLearning', component: ReinforcementLearningPage },
  { path: '/projects/visualArtificialIntelligence', name: 'visualArtificialIntelligence', component: VisualArtificialIntelligencePage },
  { path: '/experiments', name: 'experimentsPage', component: ExperimentsPage },
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