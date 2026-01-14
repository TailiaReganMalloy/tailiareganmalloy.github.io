
<template>
  <div class="fill-in-the-blank-experiment">
    <!-- Experiment content container styled to match the post.html template -->
    <div class="experiment-wrapper">
      <h1 class="headline">{{ title }}</h1>
      
      <!-- Progress indicator -->
      <div class="section-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <p class="progress-text">Section {{ currentSectionIndex + 1 }} of {{ sections.length }}</p>
      </div>
      
      <!-- Current section content -->
      <div v-if="currentSection" class="section-content">
        <div v-html="currentSection.html" class="experiment-content"></div>
      </div>
      
      <!-- Interactive submissions notice -->
      <div v-if="currentSectionIndex < sections.length - 1 && !hasInteractiveSubmissionInSection" class="interactive-notice">
        <p class="interactive-notice-text">💡 This section has interactive elements. Try clicking an "Update" button to generate new text!</p>
      </div>

      <!-- Open response text box -->
      <div class="response-section">
        <label for="section-response" class="response-label">
          {{ currentSectionIndex < sections.length - 1 ? 'What did you learn from this section? (required to continue)' : 'What did you think about what you learned? (required to finish)' }}
        </label>
        <textarea
          id="section-response"
          v-model="currentResponse"
          class="response-textarea"
          placeholder="Share your thoughts..."
          rows="4"
        ></textarea>
        <p v-if="!currentResponse.trim()" class="response-warning">
          Please write something before continuing
        </p>
      </div>
      
      <!-- Navigation buttons -->
      <div class="section-navigation">
        <button 
          v-if="currentSectionIndex < sections.length - 1" 
          @click="nextSection"
          :disabled="!currentResponse.trim() || !hasInteractiveSubmissionInSection"
          class="nav-button nav-button-continue"
        >
          Continue →
        </button>
        <button 
          v-else
          @click="finishAndRestart"
          :disabled="!currentResponse.trim()"
          class="nav-button nav-button-continue"
        >
          Submit & Finish
        </button>
      </div>

      <!-- Completion code display -->
      <div v-if="currentSectionIndex === sections.length - 1" class="completion-code" style="margin-top: 20px; text-align: center;">
        <p style="margin-bottom: 8px;">Your completion code:</p>
        <code style="font-size: 18px; font-weight: 600; letter-spacing: 1px;">{{ completionToken }}</code>
      </div>
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
import { ref, computed, onMounted, nextTick } from 'vue';
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

// Generate a unique completion token at the start
function generateCompletionToken() {
  return Math.random().toString(36).slice(2, 12).toUpperCase();
}

const completionToken = ref(generateCompletionToken());
const title = ref(frontmatter.title || 'Fill in the Blank');
const sections = ref([]);
const currentSectionIndex = ref(0);
const currentResponse = ref('');
const interactiveSubmissions = ref([]);

// Computed property for current section
const currentSection = computed(() => sections.value[currentSectionIndex.value] || null);

// Computed property for progress percentage
const progressPercentage = computed(() => {
  if (sections.value.length === 0) return 0;
  return ((currentSectionIndex.value + 1) / sections.value.length) * 100;
});

// Computed property to check if current section has at least one interactive submission
const hasInteractiveSubmissionInSection = computed(() => {
  return interactiveSubmissions.value.some(sub => sub.sectionIndex === currentSectionIndex.value);
});

// Define logInteractiveSubmission on window EARLY so scripts can call it
// This must be defined before scripts are loaded
window.logInteractiveSubmission = function(originalText, updatedText, submissionType = 'sentence_update') {
  console.log('[logInteractiveSubmission] Function called with:', { originalText, updatedText, submissionType });
  console.log('[logInteractiveSubmission] currentSectionIndex:', currentSectionIndex.value);
  console.log('[logInteractiveSubmission] sections.length:', sections.value.length);
  
  const section = currentSection.value;
  if (!section) {
    console.error('[logInteractiveSubmission] ERROR: No current section found. Section index:', currentSectionIndex.value, 'Total sections:', sections.value.length);
    return;
  }
  
  console.log('[logInteractiveSubmission] Recording submission for section:', section.title);
  
  const submission = {
    pageTitle: title.value,
    sectionTitle: section.title,
    sectionIndex: currentSectionIndex.value,
    originalText: originalText,
    updatedText: updatedText,
    submissionType: submissionType
  };
  
  // Add to local tracking
  interactiveSubmissions.value.push(submission);
  console.log('[logInteractiveSubmission] ✓ Submission recorded. Total submissions:', interactiveSubmissions.value.length);
  console.log('[logInteractiveSubmission] hasInteractiveSubmissionInSection now:', hasInteractiveSubmissionInSection.value);
  
  // Save to backend
  saveInteractiveSubmission(submission);
};

// Split content into sections based on H1 headings (#)
function splitIntoSections(markdownContent) {
  const sectionsList = [];
  
  // Split by # headings
  const parts = markdownContent.split(/(?=^# )/gm);
  
  // First part is the introduction (before any # heading)
  if (parts[0] && parts[0].trim()) {
    sectionsList.push({
      title: 'Introduction',
      content: parts[0].trim(),
      html: markdownToHtml(parts[0].trim())
    });
  }
  
  // Process remaining sections (each starts with #)
  for (let i = 1; i < parts.length; i++) {
    const part = parts[i].trim();
    if (part) {
      // Extract title from # heading
      const titleMatch = part.match(/^# (.+)$/m);
      const sectionTitle = titleMatch ? titleMatch[1] : `Section ${i}`;
      
      sectionsList.push({
        title: sectionTitle,
        content: part,
        html: markdownToHtml(part)
      });
    }
  }
  
  return sectionsList;
}

// Navigation methods
async function nextSection() {
  if (currentSectionIndex.value < sections.value.length - 1 && currentResponse.value.trim()) {
    // Save response to backend before moving to next section
    await saveResponse();
    
    currentSectionIndex.value++;
    currentResponse.value = '';
    scrollToTop();
    // Reload experiment scripts for new section content
    nextTick(() => loadExperimentScripts());
  }
}

// Save response to Heroku backend
async function saveResponse() {
  const section = currentSection.value;
  if (!section || !currentResponse.value.trim()) return;

  try {
    const apiUrl = (window.__API_URL__ && typeof window.__API_URL__ === 'string'
      ? window.__API_URL__
      : (import.meta.env.VITE_API_URL || 'http://localhost:3001'));
    
    const response = await fetch(`${apiUrl}/api/responses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        pageTitle: title.value,
        sectionTitle: section.title,
        sectionIndex: currentSectionIndex.value,
        responseText: currentResponse.value,
        completionToken: completionToken.value
      })
    });

    if (!response.ok) {
      console.error('Failed to save response:', response.statusText);
    } else {
      const data = await response.json();
      console.log('Response saved successfully:', data);
    }
  } catch (error) {
    console.error('Error saving response:', error);
  }
}

async function finishAndRestart() {
  if (!currentResponse.value.trim()) return;
  await saveResponse();
}

function restartFromBeginning() {
  currentSectionIndex.value = 0;
  currentResponse.value = '';
  scrollToTop();
  nextTick(() => loadExperimentScripts());
}

// Save interactive submission to backend
async function saveInteractiveSubmission(submission) {
  // Validate submission object
  if (!submission.pageTitle || !submission.sectionTitle || submission.sectionIndex === undefined || 
      !submission.originalText || !submission.updatedText || !submission.submissionType) {
    console.error('Invalid submission object:', submission);
    return;
  }

  // Add completionToken to submission
  submission.completionToken = completionToken.value;

  try {
    const apiUrl = (window.__API_URL__ && typeof window.__API_URL__ === 'string'
      ? window.__API_URL__
      : (import.meta.env.VITE_API_URL || 'http://localhost:3001'));
    
    const response = await fetch(`${apiUrl}/api/interactive-submissions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(submission)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Failed to save interactive submission:', response.statusText, errorData);
    } else {
      const data = await response.json();
      console.log('Interactive submission saved:', data);
    }
  } catch (error) {
    console.error('Error saving interactive submission:', error);
  }
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Parse markdown on mount, then load experiment scripts after DOM update
onMounted(async () => {
  sections.value = splitIntoSections(content);
  
  // Wait for DOM to update with rendered markdown
  await nextTick();
  
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
      
      // Attach event listeners to Update buttons
      attachUpdateButtonListeners();
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

// Attach event listeners to "Update" buttons to track submissions
function attachUpdateButtonListeners() {
  console.log('[attachUpdateButtonListeners] Starting...');
  
  // Use event delegation on document to catch all current and future Update button clicks
  document.addEventListener('click', function(event) {
    const button = event.target.closest('button');
    if (button && button.textContent.includes('Update')) {
      console.log('[attachUpdateButtonListeners] Update button clicked!', button.textContent, button);
      
      // Record this as an interactive submission
      if (window.logInteractiveSubmission) {
        console.log('[attachUpdateButtonListeners] Calling logInteractiveSubmission...');
        window.logInteractiveSubmission('clicked', 'update', 'button_click');
      } else {
        console.error('[attachUpdateButtonListeners] window.logInteractiveSubmission is not defined');
      }
    }
  }, true); // Use capture phase to catch events early
  
  console.log('[attachUpdateButtonListeners] Event delegation attached to document');
}

</script>

<style src="./style.scoped.css"></style>
