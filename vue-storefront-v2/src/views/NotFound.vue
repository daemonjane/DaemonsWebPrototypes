<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 relative overflow-hidden">
    <!-- Animated SVG background -->
    <svg class="absolute inset-0 w-full h-full opacity-10 pointer-events-none" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <radialGradient id="pulse-grad" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.3">
            <animate attributeName="stop-opacity" values="0.3;0.1;0.3" dur="3s" repeatCount="indefinite"/>
          </stop>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <circle cx="200" cy="200" r="180" fill="url(#pulse-grad)">
        <animate attributeName="r" values="120;200;120" dur="4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="200" cy="200" r="80" fill="none" stroke="#06b6d4" stroke-width="0.5" stroke-dasharray="4 4">
        <animateTransform attributeName="transform" type="rotate" from="0 200 200" to="360 200 200" dur="20s" repeatCount="indefinite"/>
      </circle>
      <circle cx="200" cy="200" r="140" fill="none" stroke="#06b6d4" stroke-width="0.5" stroke-dasharray="4 4">
        <animateTransform attributeName="transform" type="rotate" from="360 200 200" to="0 200 200" dur="25s" repeatCount="indefinite"/>
      </circle>
      <line x1="0" y1="200" x2="400" y2="200" stroke="#06b6d4" stroke-width="0.3" opacity="0.3"/>
      <line x1="200" y1="0" x2="200" y2="400" stroke="#06b6d4" stroke-width="0.3" opacity="0.3"/>
      <circle cx="200" cy="200" r="2" fill="#06b6d4">
        <animate attributeName="r" values="2;6;2" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>
      </circle>
    </svg>

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
