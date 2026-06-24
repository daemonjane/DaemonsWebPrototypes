<script setup>
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
import { useDocumentTitle } from './composables/useDocumentTitle'

const route = useRoute()
const { showSkeleton } = useRouteLoading()
useSalesNotifications()
useDocumentTitle()
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-200 font-sans antialiased selection:bg-cyan-500 selection:text-black relative">
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
        <SkeletonLoader v-if="showSkeleton" />
        <router-view v-else v-slot="{ Component }">
          <transition name="page" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <Footer />
      <ScrollToTop />
      <ToastContainer />
      <KeyboardShortcuts />
    </div>
  </div>
</template>