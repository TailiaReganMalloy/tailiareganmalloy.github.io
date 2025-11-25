import { createApp } from 'vue';
import '@/assets/styles/fonts.css';
import '@/assets/styles/main.css';
import '@/assets/styles/tailwind.css';
import App from '@/app.vue';
import router from './routes';

const app = createApp(App);

// Set favicon at runtime so Vite will fingerprint the asset during build
import faviconUrl from '@/assets/favicon.svg';

function setFavicon(href) {
	let link = document.querySelector("link[rel~='icon']");
	if (!link) {
		link = document.createElement('link');
		link.rel = 'icon';
		document.getElementsByTagName('head')[0].appendChild(link);
	}
	link.href = href;
}

if (typeof document !== 'undefined') setFavicon(faviconUrl);

app.use(router);
app.mount('#app');
