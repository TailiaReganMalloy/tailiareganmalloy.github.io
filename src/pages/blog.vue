<script setup>
import { ref, computed, onMounted } from 'vue';
import Header from '@/components/header.vue';

defineOptions({ name: 'BlogPage' });

const posts = ref([]);
const selectedYear = ref(null);
const selectedPost = ref(null);
const loading = ref(true);

// Parse frontmatter from markdown content
const parseFrontmatter = (content) => {
  const frontmatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);
  
  if (!match) return { metadata: {}, content };
  
  const frontmatter = match[1];
  const body = match[2];
  const metadata = {};
  
  frontmatter.split('\n').forEach(line => {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();
      // Remove quotes from strings
      value = value.replace(/^["']|["']$/g, '');
      metadata[key] = value;
    }
  });
  
  return { metadata, content: body };
};

// Get excerpt from content
const getExcerpt = (content, length = 200) => {
  const text = content.replace(/[#*`[\]]/g, '').trim();
  return text.length > length ? text.substring(0, length) + '...' : text;
};

// Load all blog posts
const loadPosts = async () => {
  try {
    // Import all markdown files from the posts directory
    const postModules = import.meta.glob('@/posts/*.md', { as: 'raw', eager: true });
    
    const allPosts = Object.entries(postModules).map(([path, content]) => {
      const filename = path.split('/').pop();
      const { metadata, content: body } = parseFrontmatter(content);
      
      return {
        filename,
        title: metadata.title || 'Untitled',
        date: metadata.date || '',
        draft: metadata.draft === 'true' || metadata.draft === true,
        tags: metadata.tags || [],
        excerpt: getExcerpt(body),
        content: body,
        metadata
      };
    });
    
    // Filter out drafts and sort by date (newest first)
    posts.value = allPosts
      .filter(post => !post.draft && post.date)
      .sort((a, b) => new Date(b.date) - new Date(a.date));
    
    loading.value = false;
  } catch (error) {
    console.error('Error loading posts:', error);
    loading.value = false;
  }
};

// Year-based filtering
const availableYears = computed(() => {
  const years = [...new Set(posts.value.map(post => new Date(post.date).getFullYear()))];
  return years.sort((a, b) => b - a); // Sort newest to oldest
});

const postsForSelectedYear = computed(() => {
  if (!selectedYear.value) {
    // If no year selected, show the most recent year
    if (availableYears.value.length > 0) {
      return posts.value.filter(post => 
        new Date(post.date).getFullYear() === availableYears.value[0]
      );
    }
    return [];
  }
  return posts.value.filter(post => 
    new Date(post.date).getFullYear() === selectedYear.value
  );
});

const selectYear = (year) => {
  selectedYear.value = year;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const viewPost = (post) => {
  selectedPost.value = post;
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const backToList = () => {
  selectedPost.value = null;
};

// Format date for display
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};

// Simple markdown to HTML converter
const renderMarkdown = (markdown) => {
  if (!markdown) return '';
  
  let html = markdown;
  
  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3 class="text-xl font-semibold mt-6 mb-3">$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold mt-8 mb-4">$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold mt-8 mb-4">$1</h1>');
  
  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.+?)_/g, '<em>$1</em>');
  
  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-600 dark:text-blue-400 hover:underline" target="_blank" rel="noopener noreferrer">$1</a>');
  
  // Code blocks
  html = html.replace(/```([\s\S]*?)```/g, '<pre class="bg-gray-100 dark:bg-gray-800 p-4 rounded my-4 overflow-x-auto"><code>$1</code></pre>');
  html = html.replace(/`([^`]+)`/g, '<code class="bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">$1</code>');
  
  // Lists
  html = html.replace(/^- (.+)$/gim, '<li class="ml-6">$1</li>');
  html = html.replace(/(<li.*<\/li>)/s, '<ul class="list-disc my-4">$1</ul>');
  
  // Paragraphs
  html = html.split('\n\n').map(para => {
    para = para.trim();
    if (para && !para.startsWith('<')) {
      return `<p class="mb-4">${para}</p>`;
    }
    return para;
  }).join('\n');
  
  return html;
};

onMounted(() => {
  loadPosts();
});
</script>

<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-50">
    <Header />
    
    <div class="max-w-4xl mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600 dark:text-gray-400">Loading posts...</p>
      </div>
      
      <!-- Post List View -->
      <div v-else-if="!selectedPost">
        <h1 class="text-4xl font-bold mb-8">Blog Posts</h1>
        
        <!-- No posts message -->
        <div v-if="posts.length === 0" class="text-center py-12">
          <p class="text-gray-600 dark:text-gray-400">No posts found.</p>
        </div>
        
        <!-- Posts list -->
        <div v-else class="space-y-6">
          <!-- Year Selection -->
          <div v-if="availableYears.length > 1" class="mb-6 flex justify-center items-center gap-2 flex-wrap">
            <button
              v-for="year in availableYears"
              :key="year"
              @click="selectYear(year)"
              :class="[
                'px-4 py-2 rounded font-medium transition-colors',
                (selectedYear === year || (!selectedYear && year === availableYears[0]))
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600'
              ]"
            >
              {{ year }}
            </button>
          </div>
          
          <article
            v-for="post in postsForSelectedYear"
            :key="post.filename"
            class="border-b border-gray-200 dark:border-gray-700 pb-6 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 p-4 rounded transition-colors"
            @click="viewPost(post)"
          >
            <h2 class="text-2xl font-semibold mb-2 text-blue-600 dark:text-blue-400 hover:underline">
              {{ post.title }}
            </h2>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
              {{ formatDate(post.date) }}
            </p>
            <p class="text-gray-700 dark:text-gray-300">
              {{ post.excerpt }}
            </p>
            <div v-if="post.tags && post.tags.length" class="mt-3 flex flex-wrap gap-2">
              <span
                v-for="tag in post.tags"
                :key="tag"
                class="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded"
              >
                {{ tag }}
              </span>
            </div>
          </article>
        </div>
      </div>
      
      <!-- Single Post View -->
      <div v-else class="post-content">
        <button
          @click="backToList"
          class="mb-6 text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-2"
        >
          ← Back to posts
        </button>
        
        <article>
          <h1 class="text-4xl font-bold mb-4">{{ selectedPost.title }}</h1>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            {{ formatDate(selectedPost.date) }}
          </p>
          <div v-if="selectedPost.tags && selectedPost.tags.length" class="mb-6 flex flex-wrap gap-2">
            <span
              v-for="tag in selectedPost.tags"
              :key="tag"
              class="text-sm bg-gray-200 dark:bg-gray-700 px-3 py-1 rounded"
            >
              {{ tag }}
            </span>
          </div>
          <div
            class="prose dark:prose-invert max-w-none"
            v-html="renderMarkdown(selectedPost.content)"
          />
        </article>
      </div>
    </div>
  </div>
</template>

<style scoped>
.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3) {
  color: inherit;
}

.post-content :deep(a) {
  word-break: break-word;
}

.post-content :deep(pre) {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.post-content :deep(code) {
  font-size: 0.9em;
  font-family: 'Courier New', Courier, monospace;
}

.post-content :deep(ul) {
  padding-left: 1.5rem;
}

.post-content :deep(li) {
  margin-bottom: 0.5rem;
}
</style>