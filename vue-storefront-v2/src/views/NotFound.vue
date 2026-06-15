<script setup>
/**
 * 404 Not Found page with animated glitch effect.
 * @view
 */
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] text-center px-4">
    <div class="relative mb-6">
      <p class="text-[120px] sm:text-[180px] font-mono font-black text-slate-800 leading-none select-none" aria-hidden="true">404</p>
      <p class="absolute inset-0 flex items-center justify-center text-[120px] sm:text-[180px] font-mono font-black text-cyan-500 leading-none mix-blend-screen animate-pulse select-none" aria-hidden="true">404</p>
    </div>
    <h1 class="text-2xl sm:text-3xl font-bold text-white mb-2">Signal Lost</h1>
    <p class="text-slate-400 max-w-md mb-8">This page doesn't exist or has been relocated. The system is still online.</p>
    <div class="flex gap-4">
      <button @click="router.back()" class="border border-slate-600 text-slate-300 px-5 py-2.5 rounded-lg font-medium hover:border-cyan-500 hover:text-cyan-400 transition-all">
        Go Back
      </button>
      <router-link to="/" class="bg-cyan-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-cyan-500 transition-all">
        Return to Command Station
      </router-link>
    </div>
  </div>
</template>
