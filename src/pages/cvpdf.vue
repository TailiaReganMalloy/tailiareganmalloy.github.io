<script>
import pdfUrl from '@/assets/pdf/CV.pdf'

export default {
  name: 'CvpdfPage',
  data() {
    return {
      pdfUrl
    }
  }
}
</script>

<template>
  <div class="cv-pdf-container">
    <!-- PDF Viewer using iframe -->
    <div class="pdf-viewer">
      <iframe 
        :src="pdfUrl" 
        class="w-full h-screen border-0"
        title="CV PDF"
      ></iframe>
    </div>
    
    <!-- Download link -->
    <div class="mt-4">
      <a 
        :href="pdfUrl" 
        download="CV.pdf"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
      >
        Download CV
      </a>
    </div>
  </div>
</template>

<style scoped>
.cv-pdf-container {
  max-width: 100%;
  padding: 1rem;
  
}

.pdf-viewer {
  height: 80vh;
  min-height: 600px;
}

@media (width <= 768px) {
  .pdf-viewer {
    height: 70vh;
    min-height: 500px;
  }
}
</style>