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
      class="fixed bottom-0 left-0 right-0 z-50 bg-slate-900 border-t border-slate-800 shadow-2xl shadow-slate-950/50"
      role="dialog"
      aria-modal="true"
      aria-label="Cookie consent"
    >
      <div class="max-w-7xl mx-auto px-4 py-4 sm:py-5">
        <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <div class="flex-1 min-w-0">
            <p class="text-sm text-slate-300 font-medium">This site uses cookies</p>
            <p class="text-xs text-slate-500 mt-1">
              We use essential cookies for cart and session functionality. Analytics and marketing cookies help us improve.
              <router-link to="/cookies" class="text-cyan-400 hover:text-cyan-300 underline underline-offset-2" @click="show = false">
                Learn more
              </router-link>
            </p>
          </div>
          <div class="flex items-center gap-3 shrink-0">
            <button
              @click="acceptEssential"
              class="text-xs text-slate-400 hover:text-white transition-colors px-3 py-2 rounded-md border border-slate-700 hover:border-slate-600"
            >
              Essential only
            </button>
            <button
              @click="acceptAll"
              class="text-xs font-semibold bg-cyan-600 hover:bg-cyan-500 text-white px-4 py-2 rounded-md transition-all active:scale-95"
            >
              Accept All
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>
