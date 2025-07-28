/** @type {import('tailwindcss').Config} */
import defaultTheme from 'tailwindcss/defaultTheme.js';

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class', // enables class-based dark mode
  theme: {
    extend: {
      fontFamily: {
        sans: ['InterVariable', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [],
};