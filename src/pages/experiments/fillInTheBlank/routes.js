import MainPage from './mainPage.vue';

// Export as named export so the dynamic router loader can pick it up (mod.routes).
// Each route object: { path, name, component }
export const routes = [
  { path: '/experiments/fillInTheBlank', name: 'fillInTheBlankMain', component: MainPage }
];

// Optionally also default export for flexibility.
export default routes;