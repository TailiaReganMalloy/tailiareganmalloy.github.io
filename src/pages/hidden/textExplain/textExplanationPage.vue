<template>
  <div class="text-explanation-experiment">
    <!-- Completion page - shown after submit -->
    <div v-if="studyCompleted" class="completion-page">
      <div class="completion-wrapper">
        <h1 class="completion-title">Thank You!</h1>
        <p class="completion-message">Your completion code:</p>
        <code class="completion-code-display">{{ completionToken }}</code>
        <p class="completion-instructions">You can now go back to the survey.</p>
      </div>
    </div>

    <!-- Experiment content container -->
    <div v-else class="experiment-wrapper">
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
        <h2 class="section-title">{{ currentSection.title }}</h2>
        <div v-html="currentSection.html" class="experiment-content"></div>
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
          :disabled="!currentResponse.trim()"
          class="nav-button nav-button-continue"
        >
          Continue →
        </button>
        <button 
          v-else
          @click="submitAndFinish"
          :disabled="!currentResponse.trim()"
          class="nav-button nav-button-continue"
        >
          Submit & Finish
        </button>
      </div>
    </div>
  </div>
</template>


<script>
// Project meta info for project listing
export const meta = {
  title: 'What Have Language Models Learned?',
  description: 'Understanding how large language models learn patterns and biases from text.'
}
</script>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Generate a unique completion token at the start
function generateCompletionToken() {
  return Math.random().toString(36).slice(2, 12).toUpperCase();
}

// Generate a unique session ID for this browser session
function generateSessionId() {
  return 'SES_' + Math.random().toString(36).slice(2, 10).toUpperCase() + '_' + Date.now().toString(36).toUpperCase();
}

const completionToken = ref(generateCompletionToken());
const sessionId = ref(generateSessionId());
const title = ref('What Have Language Models Learned?');
const currentSectionIndex = ref(0);
const currentResponse = ref('');
const studyCompleted = ref(false);

// Study type for this version
const studyType = ref('text-only');

// User info from study entry page
const userEmail = ref(null);
const userProlificId = ref(null);

// Define the four sections with the provided content
const sections = ref([
  {
    title: 'Introduction to Language Models',
    html: `
      <p>Large language models are making it possible for computers to write stories, program a website and turn captions into images.</p>
      <p>One of the first of these models, <strong>BERT</strong>, is trained by taking sentences, splitting them into individual words, randomly hiding some of them, and predicting what the hidden words are. After doing this millions of times, BERT has "read" enough Shakespeare to predict how this phrase usually ends:</p>
      <blockquote class="quote-block">'To be or not to be, that is the _'</blockquote>
      <p>This sentence is followed by the word <em>'question'</em> about half the time but other less likely options are words like 'problem', 'truth' or 'definition'.</p>
    `
  },
  {
    title: 'Cattle or Clothes? Regional Patterns',
    html: `
      <p>Besides Hamlet's existential dread, the text BERT was trained on also contains more patterns:</p>
      <p>When prompted with the following sentence:</p>
      <blockquote class="quote-block">'In Texas, they like to buy _'</blockquote>
      <p>The most common items are <strong>beer, horses, coffee or cattle</strong>.</p>
      <p>But cattle and horses aren't top purchase predictions in every state, though! In New York, some of the most likely words are <strong>clothes, books and art</strong>.</p>
      <p>There are more than 30,000 words, punctuation marks and word fragments in BERT's vocabulary. Every time BERT fills in a hidden word, it assigns each of them a probability. By looking at how slightly different sentences shift those probabilities, we can get a glimpse at how purchasing patterns in different places are understood.</p>
      <p class="highlight-text">To the extent that a computer program can "know" something, what does BERT know about where you live?</p>
    `
  },
  {
    title: "What's in a Name? Learned Associations",
    html: `
      <p>This technique can also probe what associations BERT has learned about different groups of people. For example, it predicts people named <strong>Elsie</strong> are older than people named <strong>Lauren</strong>.</p>
      <p>It's also learned that people named <strong>Jim</strong> have more typically masculine jobs than people named <strong>Jane</strong>.</p>
      <p>These aren't just spurious correlations — Elsies really are more likely to be older than Laurens. And occupations the model associates with feminine names are held by a higher percentage of women.</p>
      <div class="concern-box">
        <h4>Should we be concerned about these correlations?</h4>
        <p>BERT was trained to fill in blanks in Wikipedia articles and books — it does a great job at that! The problem is that the internal representations of language these models have learned are used for much more – by some measures, they're the best way we have of getting computers to understand and manipulate text.</p>
        <p>We wouldn't hesitate to call a conversation partner or recruiter who blithely assumed that doctors are men sexist, but that's exactly what BERT might do if heedlessly incorporated into a chatbot or HR software.</p>
      </div>
      <p>Adjusting for assumptions like this isn't trivial. Why machine learning systems produce a given output still isn't well understood – determining if a credit model built on top of BERT rejected a loan application because of gender discrimination might be quite difficult.</p>
      <p>Deploying large language models at scale also risks amplifying and perpetuating today's harmful stereotypes. When prompted with "Two Muslims walked into a…", for example, GPT-3 typically finishes the sentence with descriptions of violence.</p>
    `
  },
  {
    title: 'How Can We Fix This?',
    html: `
      <p>One conceptually straightforward approach: <strong>reduce unwanted correlations from the training data</strong> to mitigate model bias.</p>
      <div class="example-box">
        <h4>The Zari Approach</h4>
        <p>Last year a version of BERT called <strong>Zari</strong> was trained with an additional set of generated sentences. For every sentence with a gendered noun, like <em>boy</em> or <em>aunt</em>, another sentence that replaced the noun with its gender-partner was added to the training data: in addition to "The lady doth protest too much," Zari was also trained on "The gentleman doth protest too much."</p>
      </div>
      <p>Unlike BERT, Zari assigns nurses and doctors an equal probability of being a "she" or a "he" after being trained on the swapped sentences. This approach hasn't removed all the gender correlations; because names weren't swapped, Zari's association between masculine names and doctors has only slightly decreased from BERT's. And the retraining doesn't change how the model understands nonbinary gender.</p>
      <p>It's possible to mathematically define bias and perform "brain surgery" on a model to remove it, but language is steeped in gender. Large models can have billions of parameters in which to learn stereotypes — slightly different measures of bias have found the retrained models only shifted the stereotypes around to be undetectable by the initial measure.</p>
      <div class="future-box">
        <h4>Looking Forward</h4>
        <p>It's also possible that as models grow more capable, they might be able to explain and perform some of this debiasing themselves. Instead of forcing the model to tell us the gender of "the doctor," we could let it respond with uncertainty that's shown to the user and controls to override assumptions.</p>
      </div>
    `
  }
]);

// Load user info from sessionStorage
function loadUserInfo() {
  try {
    const stored = sessionStorage.getItem('studyUserInfo');
    if (stored) {
      const info = JSON.parse(stored);
      userEmail.value = info.email || null;
      userProlificId.value = info.prolificId || null;
    }
  } catch (e) {
    console.warn('Could not load user info from sessionStorage:', e);
  }
}

// Computed property for current section
const currentSection = computed(() => sections.value[currentSectionIndex.value] || null);

// Computed property for progress percentage
const progressPercentage = computed(() => {
  if (sections.value.length === 0) return 0;
  return ((currentSectionIndex.value + 1) / sections.value.length) * 100;
});

// Navigation methods
async function nextSection() {
  if (currentSectionIndex.value < sections.value.length - 1 && currentResponse.value.trim()) {
    // Save response to backend before moving to next section
    await saveResponse();
    
    currentSectionIndex.value++;
    currentResponse.value = '';
    scrollToTop();
  }
}

// Save response to backend
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
        completionToken: completionToken.value,
        sessionId: sessionId.value,
        email: userEmail.value,
        prolificId: userProlificId.value,
        studyType: studyType.value
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

// Submit final response and show completion code
async function submitAndFinish() {
  if (!currentResponse.value.trim()) return;
  await saveResponse();
  studyCompleted.value = true;
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize on mount
onMounted(() => {
  loadUserInfo();
});
</script>

<style scoped>
/* Main container styles */
.text-explanation-experiment {
  max-width: 850px;
  margin: 0 auto;
  margin-top: 20px;
  margin-bottom: 80px;
  padding: 0 20px;
  color: #3C4043;
  font-weight: 300;
  font-size: 16px;
  font-family: 'Roboto', Helvetica, sans-serif;
  line-height: 1.6em;
  background-color: #fff;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Headings */
.headline {
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-weight: 400;
  font-size: 36px;
  line-height: 1.3em;
  text-align: center;
  color: #202124;
  margin-bottom: 30px;
  margin-top: 40px;
}

.section-title {
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-weight: 400;
  font-size: 28px;
  color: #1a73e8;
  margin-bottom: 20px;
  margin-top: 10px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e8f0fe;
}

/* Progress bar */
.section-progress {
  margin-bottom: 30px;
}

.progress-bar {
  height: 8px;
  background-color: #e8eaed;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #1a73e8, #34a853);
  border-radius: 4px;
  transition: width 0.4s ease-out;
}

.progress-text {
  font-size: 14px;
  color: #5f6368;
  text-align: center;
}

/* Section content styling */
.section-content {
  background: #fafafa;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.experiment-content :deep(p) {
  margin-bottom: 16px;
  line-height: 1.7em;
  color: #3c4043;
}

.experiment-content :deep(strong) {
  font-weight: 500;
  color: #202124;
}

.experiment-content :deep(em) {
  font-style: italic;
  color: #5f6368;
}

/* Quote blocks */
.experiment-content :deep(.quote-block) {
  font-family: 'Georgia', serif;
  font-size: 20px;
  font-style: italic;
  color: #1a73e8;
  background: #e8f0fe;
  padding: 20px 25px;
  margin: 20px 0;
  border-left: 4px solid #1a73e8;
  border-radius: 0 8px 8px 0;
}

/* Highlight text */
.experiment-content :deep(.highlight-text) {
  background: linear-gradient(120deg, #fef7e0 0%, #fef7e0 100%);
  padding: 15px 20px;
  border-radius: 8px;
  font-weight: 400;
  color: #856404;
  border-left: 4px solid #ffc107;
  margin: 20px 0;
}

/* Concern box */
.experiment-content :deep(.concern-box) {
  background: #fce8e6;
  border: 1px solid #f5c6cb;
  border-left: 4px solid #ea4335;
  border-radius: 0 8px 8px 0;
  padding: 20px 25px;
  margin: 25px 0;
}

.experiment-content :deep(.concern-box h4) {
  color: #c5221f;
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 12px;
  margin-top: 0;
}

.experiment-content :deep(.concern-box p) {
  margin-bottom: 10px;
  color: #5f2120;
}

.experiment-content :deep(.concern-box p:last-child) {
  margin-bottom: 0;
}

/* Example box */
.experiment-content :deep(.example-box) {
  background: #e6f4ea;
  border: 1px solid #ceead6;
  border-left: 4px solid #34a853;
  border-radius: 0 8px 8px 0;
  padding: 20px 25px;
  margin: 25px 0;
}

.experiment-content :deep(.example-box h4) {
  color: #137333;
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 12px;
  margin-top: 0;
}

.experiment-content :deep(.example-box p) {
  margin-bottom: 10px;
  color: #1e4620;
}

.experiment-content :deep(.example-box p:last-child) {
  margin-bottom: 0;
}

/* Future box */
.experiment-content :deep(.future-box) {
  background: #e8f0fe;
  border: 1px solid #d2e3fc;
  border-left: 4px solid #1a73e8;
  border-radius: 0 8px 8px 0;
  padding: 20px 25px;
  margin: 25px 0;
}

.experiment-content :deep(.future-box h4) {
  color: #1967d2;
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 12px;
  margin-top: 0;
}

.experiment-content :deep(.future-box p) {
  margin-bottom: 10px;
  color: #174ea6;
}

.experiment-content :deep(.future-box p:last-child) {
  margin-bottom: 0;
}

/* Response section */
.response-section {
  background: #fff;
  border: 1px solid #dadce0;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
}

.response-label {
  display: block;
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #202124;
  margin-bottom: 12px;
}

.response-textarea {
  width: 100%;
  min-height: 120px;
  padding: 15px;
  font-family: 'Roboto', sans-serif;
  font-size: 15px;
  line-height: 1.5em;
  color: #3c4043;
  background: #f8f9fa;
  border: 1px solid #dadce0;
  border-radius: 8px;
  resize: vertical;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

.response-textarea:focus {
  outline: none;
  border-color: #1a73e8;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.2);
  background: #fff;
}

.response-textarea::placeholder {
  color: #9aa0a6;
}

.response-warning {
  font-size: 13px;
  color: #ea4335;
  margin-top: 8px;
  margin-bottom: 0;
}

/* Navigation */
.section-navigation {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.nav-button {
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 16px;
  font-weight: 500;
  padding: 14px 32px;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.nav-button-continue {
  background: #1a73e8;
  color: white;
}

.nav-button-continue:hover:not(:disabled) {
  background: #1557b0;
  box-shadow: 0 2px 8px rgba(26, 115, 232, 0.4);
}

.nav-button:disabled {
  background: #dadce0;
  color: #9aa0a6;
  cursor: not-allowed;
}

/* Completion page */
.completion-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.completion-wrapper {
  text-align: center;
  padding: 60px 40px;
  background: linear-gradient(135deg, #e8f0fe 0%, #e6f4ea 100%);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.completion-title {
  font-family: 'Google Sans', 'Roboto', sans-serif;
  font-size: 42px;
  font-weight: 400;
  color: #34a853;
  margin-bottom: 20px;
}

.completion-message {
  font-size: 18px;
  color: #5f6368;
  margin-bottom: 15px;
}

.completion-code-display {
  display: inline-block;
  font-family: 'Roboto Mono', monospace;
  font-size: 28px;
  font-weight: 500;
  color: #1a73e8;
  background: white;
  padding: 15px 30px;
  border-radius: 12px;
  border: 2px solid #1a73e8;
  letter-spacing: 2px;
}

.completion-instructions {
  font-size: 16px;
  color: #5f6368;
  margin-top: 25px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .text-explanation-experiment {
    padding: 0 15px;
    margin-top: 10px;
  }

  .headline {
    font-size: 28px;
  }

  .section-title {
    font-size: 22px;
  }

  .section-content {
    padding: 20px;
  }

  .completion-wrapper {
    padding: 40px 25px;
  }

  .completion-title {
    font-size: 32px;
  }

  .completion-code-display {
    font-size: 20px;
    padding: 12px 20px;
  }
}
</style>
