
<template>
  <div class="fillInTheBlank-experiment">
    <!-- Experiment content container styled to match the post.html template -->
    <div class="experiment-wrapper">
      <h1 class="headline">{{ title }}</h1>
    
      <p>Large language models are making it possible for computers to <a href="https://openai.com/blog/better-language-models/" target="_blank" rel="noopener">write stories</a>, <a href="https://twitter.com/sharifshameem/status/1282676454690451457" target="_blank" rel="noopener">program a website</a> and <a href="https://openai.com/blog/dall-e/" target="_blank" rel="noopener">turn captions into images</a>.</p>

      <p>One of the first of these models, <a href="https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html" target="_blank" rel="noopener">BERT</a>, is trained by taking sentences, splitting them into individual words, randomly hiding some of them, and predicting what the hidden words are. After doing this millions of times, BERT has "read" enough Shakespeare to predict how this phrase usually ends:</p>

    <div class='sent hamlet' id="sent-hamlet"></div>

      <div v-if="summary" class="post-summary">{{ summary }}</div>
      
      <!-- Render the markdown content as HTML -->
      <div v-html="markdownHtml" class="experiment-content"></div>
    </div>
  </div>
</template>


<script>
// Project meta info for project listing
import fillInBlankThumb from './source/img/wiki-years.png';

export const meta = {
  title: 'What Have Language Models Learned?',
  image: fillInBlankThumb,
  description: 'By asking language models to fill in the blank, we can probe their understanding of the world.'
}
</script>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
// Import the post markdown file as raw text
import postMarkdownRaw from './post.md?raw';
// NOTE: style.css is imported in the <style> section below with scoping

// Simple frontmatter + markdown parser (no dependencies needed)
function parseFrontmatter(rawMarkdown) {
  const lines = rawMarkdown.split('\n');
  
  // Check if starts with ---
  if (lines[0].trim() !== '---') {
    return { frontmatter: {}, content: rawMarkdown };
  }
  
  // Find the closing ---
  let endIndex = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === '---') {
      endIndex = i;
      break;
    }
  }
  
  if (endIndex === -1) {
    return { frontmatter: {}, content: rawMarkdown };
  }
  
  // Parse YAML-like frontmatter (simple key: value pairs)
  const frontmatter = {};
  for (let i = 1; i < endIndex; i++) {
    const line = lines[i];
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();
      frontmatter[key] = value;
    }
  }
  
  const content = lines.slice(endIndex + 1).join('\n');
  return { frontmatter, content };
}

// Very basic markdown-to-HTML converter (handles common cases)
function markdownToHtml(md) {
  let html = md;
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  
  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  
  // Bold
  html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  
  // Italic
  html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
  
  // Code blocks with language hint
  html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
  
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Divs with classes (custom syntax in the post.md)
  html = html.replace(/<div class='([^']+)'><\/div>/g, '<div class="$1"></div>');
  
  // Images
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />');
  
  // Paragraphs (split on double newlines)
  const paragraphs = html.split('\n\n');
  html = paragraphs.map(p => {
    p = p.trim();
    // Don't wrap if already an HTML tag
    if (p.startsWith('<')) return p;
    return `<p>${p.replace(/\n/g, ' ')}</p>`;
  }).join('\n');
  
  return html;
}

const { frontmatter, content } = parseFrontmatter(postMarkdownRaw);

const title = ref(frontmatter.title || 'Fill in the Blank');
const summary = ref(frontmatter.summary || '');
const markdownHtml = ref('');


// Parse markdown on mount, then load experiment scripts after DOM update

onMounted(async () => {
  markdownHtml.value = markdownToHtml(content);
  // Wait for DOM to update with rendered markdown
  await nextTick();
  // Debug: check if the div is present before loading experiment scripts
  const sentDiv = document.querySelector('.sent.hamlet');
  if (sentDiv) {
    console.log('[DEBUG] .sent.hamlet div found:', sentDiv);
  } else {
    console.warn('[DEBUG] .sent.hamlet div NOT found!');
  }
  // Now load the experiment scripts after experiment divs exist
  loadExperimentScripts();
});

// Dynamically load all the JS dependencies from source and third_party
function loadExperimentScripts() {
  const scripts = [
    // Third party dependencies (absolute paths for GitHub Pages)
    '/third_party/regl.min.js',
    '/third_party/d3_.js',
    '/third_party/d3-scale-chromatic.v1.min.js',
    '/third_party/params.js',
    // Experiment source scripts
    '/source/data/cachekey2filename.js',
    '/source/post.js',
    '/source/tokenizer.js',
    '/source/scatter.js',
    '/source/init-pair.js',
    '/source/init-diff.js',
    '/source/init-sent.js',
    '/source/init-gender-over-time.js',
    '/source/init.js',
  ];
  
  console.log('[loadExperimentScripts] Starting to load', scripts.length, 'scripts');
  
  // Load scripts sequentially
  let loadNext = (index) => {
    if (index >= scripts.length) {
      console.log('[loadExperimentScripts] All scripts loaded.');
      console.log('[loadExperimentScripts] window.init type:', typeof window.init);
      console.log('[loadExperimentScripts] window.initSent type:', typeof window.initSent);
      console.log('[loadExperimentScripts] window.sents:', window.sents);
      
      // init.js already calls window.init() automatically via the resize() IIFE
      // So we don't need to call it again here
      return;
    }
    
    console.log('[loadExperimentScripts] Loading script', index + 1, '/', scripts.length, ':', scripts[index]);
    const script = document.createElement('script');
    script.src = scripts[index];
    script.onload = () => {
      console.log('[loadExperimentScripts] ✓ Loaded:', scripts[index]);
      loadNext(index + 1);
    };
    script.onerror = () => {
      console.warn(`[loadExperimentScripts] ✗ Failed to load: ${scripts[index]}`);
      loadNext(index + 1);
    };
    document.body.appendChild(script);
  };
  
  loadNext(0);
}
</script>

<style src="./style.scoped.css"></style>
