<script setup>
// @ts-ignore
defineOptions({
  name: 'ParticlesComponent'
})

import { onMounted, onBeforeUnmount } from 'vue'
// @ts-ignore
import 'particles.js'
// particles config extracted to JSON
import particlesConfig from './particles.json'

let observer = null
let themeObserver = null

function getCurrentTheme() {
  try {
    return document.documentElement.getAttribute('data-theme') || (document.documentElement.classList.contains('dark') ? 'dark' : 'light')
  } catch (e) {
    return 'light'
  }
}

function cleanupParticles() {
  // disconnect canvas observer
  if (observer) {
    try { observer.disconnect() } catch (e) { void e }
    observer = null
  }

  // clear any injected DOM inside the particles container
  const root = document.getElementById('particles-js')
  if (root) root.innerHTML = ''
}

function initParticlesForTheme(theme) {
  // Accessibility: respect prefers-reduced-motion
  const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const container = document.getElementById('particles-js')
  if (!container) return

  if (prefersReduced) {
    // mark container aria-hidden for screen readers and don't init animation
    container.setAttribute('aria-hidden', 'true')
    container.style.background = theme === 'dark' ? '#0F172A' : '#fff'
    return
  }

  // ensure container is visible and not aria-hidden
  container.removeAttribute('aria-hidden')
  container.style.background = theme === 'dark' ? '#0F172A' : '#fff'

  // create a fresh copy of the config and apply theme colors
  const cfg = JSON.parse(JSON.stringify(particlesConfig))
  const particleColor = theme === 'dark' ? '#ffffff' : '#0F172A'
  // set primary particle color and line color
  if (cfg && cfg.particles) {
    if (cfg.particles.color) cfg.particles.color.value = particleColor
    if (cfg.particles.line_linked) cfg.particles.line_linked.color = particleColor
  }

  // initialize particles
  // @ts-ignore
  if (typeof window.particlesJS === 'function') {
    // clear any previous content before initializing
    cleanupParticles()

    // prepare observer to catch injected canvas (attach before init to catch synchronous insertion)
    const root = document.getElementById('particles-js')
    if (root) {
      observer = new MutationObserver((mutations) => {
        for (const m of mutations) {
          for (const node of Array.from(m.addedNodes)) {
            if (node instanceof HTMLCanvasElement) {
              node.id = 'canvas'
              node.className = 'particles-canvas'
              if (observer) { observer.disconnect(); observer = null }
              return
            }

            if (node.nodeType === Node.ELEMENT_NODE) {
              try {
                var found = node.querySelector && node.querySelector('canvas')
                if (found && found instanceof HTMLCanvasElement) {
                  found.id = 'canvas'
                  found.className = 'particles-canvas'
                  if (observer) { observer.disconnect(); observer = null }
                  return
                }
              } catch (e) { void e }
            }
          }
        }
      })

      observer.observe(root, { childList: true, subtree: true })
    }

    // call particlesJS to build the canvas (may be synchronous)
    // Some versions of particles.js use `arguments.callee` inside Object.deepExtend which throws
    // in strict-mode environments. Replace Object.deepExtend with a safe implementation before init.
    try {
      Object.defineProperty(Object, 'deepExtend', {
        configurable: true,
        enumerable: false,
        writable: true,
        value: function(target, source) {
          function merge(a, b) {
            for (var key in b) {
              if (!Object.prototype.hasOwnProperty.call(b, key)) continue
              try {
                if (b[key] && b[key].constructor === Object) {
                  a[key] = a[key] || {}
                  merge(a[key], b[key])
                } else {
                  a[key] = b[key]
                }
              } catch (e) {
                a[key] = b[key]
              }
            }
          }
          merge(target, source)
          return target
        }
      })
    } catch (e) { void e }

    // @ts-ignore
    window.particlesJS('particles-js', cfg)

    // immediate fallback: if particles.js injected synchronously, the canvas may already exist
    if (root) {
      const existing = root.querySelector && root.querySelector('canvas')
      if (existing && existing instanceof HTMLCanvasElement) {
        existing.id = 'canvas'
        existing.className = 'particles-canvas'
        if (observer) { observer.disconnect(); observer = null }
      }
    }
  }
}

function refreshParticles() {
  const theme = getCurrentTheme()
  initParticlesForTheme(theme)
}

onMounted(() => {
  // init particles based on current theme
  refreshParticles()

  // observe theme changes made on document.documentElement (data-theme attribute)
  const docEl = document.documentElement
  if (docEl) {
    themeObserver = new MutationObserver((mutations) => {
      for (const m of mutations) {
        if (m.type === 'attributes' && m.attributeName === 'data-theme') {
          refreshParticles()
        }
      }
    })
    themeObserver.observe(docEl, { attributes: true, attributeFilter: ['data-theme', 'class'] })
  }
})

onBeforeUnmount(() => {
  if (observer) { observer.disconnect(); observer = null }
  if (themeObserver) { themeObserver.disconnect(); themeObserver = null }
})
</script>

<template>
  <div class="particles">
    <div id="particles-js" class="absolute inset-0" role="img" aria-describedby="particles-desc"></div>

      <!-- Slot content will be centered above the particles canvas -->
       <!-- Intersecting Cognition And -->
      <div class="particles-slot absolute inset-0 z-10 flex items-center justify-center pointer-events-none">
        <!-- By default the slot does not intercept pointer events so the canvas remains interactive.
             If you need interactive elements inside the slot (buttons/links), add the
             `particles-slot-content` class to those elements to re-enable pointer events. -->
        <slot />
      </div>
  </div>
</template>

<style scoped>
#particles-js {
  position: relative;
  width: 100%;
  height: 60vh;
  background: black;
}

#canvas.particles-canvas {
  position: absolute;
  inset: 0;
  width: 100% !important;
  height: 75vh !important;
}

.particles-slot-content {
  z-index: 20; /* ensure interactive content sits above canvas */
  pointer-events: auto; /* allow clicks on elements that opt-in */
}
</style>
