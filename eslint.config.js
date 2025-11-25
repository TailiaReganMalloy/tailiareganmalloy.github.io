import js from "@eslint/js";
import globals from "globals";
import pluginVue from "eslint-plugin-vue";

export default [
  // Ignore third-party experiment source bundles from linting
  { ignores: [
    "src/pages/experiments/**/source/**",
    "src/pages/experiments/**/third_party/**",
    "src/pages/experiments/**/server/**",
    "src/pages/experiments/**/scope-styles.js"
  ] },
  js.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  {
    files: ["**/*.{js,mjs,cjs,vue}"],
    languageOptions: {
      globals: globals.browser
    }
  }
];
