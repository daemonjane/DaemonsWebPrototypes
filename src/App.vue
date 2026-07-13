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
  <div lang="en" class="min-h-screen bg-surface-950 text-surface-100 font-body antialiased selection:bg-gold-500/30 selection:text-surface-50 relative">
    <BackgroundEffects />
    <div class="relative z-10">
      <!-- Skip link -->
      <a
        href="#main-content"
        class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-gold-500 focus:text-surface-950 focus:px-4 focus:py-2 focus:rounded-lg focus:font-medium"
      >
        Skip to main content
      </a>

      <Header />

      <main id="main-content" class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <div v-if="appError" class="bg-danger-500/10 border border-danger-500/30 rounded-xl p-4 mb-6 text-danger-400 text-sm flex items-center justify-between" role="alert">
          <span>{{ appError }}</span>
          <button @click="appError = null" class="text-danger-400 hover:text-danger-300 underline text-xs">Dismiss</button>
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
