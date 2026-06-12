<script setup>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import ToastContainer from './components/ToastContainer.vue'
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-200 font-sans antialiased selection:bg-cyan-500 selection:text-black relative">
    <Header />
    <main class="max-w-7xl mx-auto px-4 py-8">
      <router-view />
    </main>
    <Footer />
    <ToastContainer />
  </div>
</template>