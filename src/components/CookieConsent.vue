<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const COOKIE_CONSENT_KEY = 'vertex_cookie_consent'
const show = ref(false)
const router = useRouter()

onMounted(() => {
  const stored = localStorage.getItem(COOKIE_CONSENT_KEY)
  if (!stored) {
    setTimeout(() => { show.value = true }, 500)
  }
})

function acceptAll() {
  localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify({ essential: true, analytics: true, marketing: true }))
  show.value = false
}

function acceptEssential() {
  localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify({ essential: true, analytics: false, marketing: false }))
  show.value = false
}
</script>

<template>
  <transition
    enter-active-class="transition-all duration-300 ease-out"
    leave-active-class="transition-all duration-200 ease-in"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div
      v-if="show"
      class="fixed bottom-0 left-0 right-0 z-50 bg-surface-900/95 border-t border-surface-750 shadow-2xl shadow-surface-950/50 backdrop-blur-xl"
      role="dialog"
      aria-modal="true"
      aria-label="Cookie consent"
    >
      <div class="max-w-7xl mx-auto px-4 py-4 sm:py-5">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-surface-200 font-medium">This site uses cookies</p>
            <p class="text-xs text-surface-400 mt-1">
              We use essential cookies for cart and session functionality. Analytics and marketing cookies help us improve.
              <router-link to="/cookies" class="text-electric-500 hover:text-electric-400 underline underline-offset-2" @click="show = false">
                Learn more
              </router-link>
            </p>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <button
              @click="acceptEssential"
              class="text-xs text-surface-400 hover:text-surface-100 transition-colors px-3 py-2 rounded-lg border border-surface-700 hover:border-surface-600"
            >
              Essential only
            </button>
            <button
              @click="acceptAll"
              class="text-xs font-semibold bg-electric-500 hover:bg-electric-400 text-surface-950 px-4 py-2 rounded-lg transition-all active:scale-95 shadow-glow-electric"
            >
              Accept All
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
