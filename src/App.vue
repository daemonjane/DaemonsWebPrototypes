<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import ScrollToTop from './components/ScrollToTop.vue'
import ToastContainer from './components/ToastContainer.vue'
import SkeletonLoader from './components/SkeletonLoader.vue'
import { useRouteLoading } from './composables/useRouteLoading'
import { useSalesNotifications } from './composables/useSalesNotifications'
import KeyboardShortcuts from './components/KeyboardShortcuts.vue'
import BackgroundEffects from './components/BackgroundEffects.vue'
import CookieConsent from './components/CookieConsent.vue'
import { useMeta } from './composables/useMeta'

const route = useRoute()
const { showSkeleton } = useRouteLoading()
useSalesNotifications()
useMeta()
const appError = ref(null)

onErrorCaptured((err) => {
  appError.value = err.message || 'An unexpected error occurred'
  console.error(err)
  return false
})
</script>

<template>
  <div lang="en" class="min-h-screen bg-slate-950 text-slate-200 font-sans antialiased selection:bg-cyan-500 selection:text-black relative">
    <BackgroundEffects />
    <div class="relative z-10">
      <!-- Skip link for keyboard users -->
      <a
        href="#main-content"
        class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-cyan-600 focus:text-white focus:px-4 focus:py-2 focus:rounded"
      >
        Skip to main content
      </a>

      <Header />

      <main id="main-content" class="max-w-7xl mx-auto px-4 py-8">
        <div v-if="appError" class="bg-pink-900/30 border border-pink-700/50 rounded-xl p-4 mb-6 text-pink-300 text-sm" role="alert">
          {{ appError }}
          <button @click="appError = null" class="ml-2 text-pink-400 hover:text-pink-200 underline">Dismiss</button>
        </div>
        <SkeletonLoader v-if="showSkeleton" />
        <router-view v-else v-slot="{ Component }">
          <transition name="page">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <Footer />
      <ScrollToTop />
      <ToastContainer />
      <KeyboardShortcuts />
      <CookieConsent />
    </div>
  </div>
</template>