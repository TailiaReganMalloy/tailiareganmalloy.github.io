import { createApp } from 'vue';
import '@/assets/styles/fonts.css';
import '@/assets/styles/main.css';
import '@/assets/styles/tailwind.css';
import App from '@/app.vue';
import router from './routes';

const app = createApp(App);

app.use(router);
app.mount('#app');
