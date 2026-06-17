<script setup>
import { useFreeShipping } from '../composables/useFreeShipping'

const { remaining, progress, qualifies } = useFreeShipping()
</script>

<template>
  <div class="bg-slate-800 border border-slate-700 rounded-lg px-3 sm:px-4 py-2.5 text-xs sm:text-sm">
    <div class="flex items-center justify-between gap-2 mb-1.5">
      <span v-if="qualifies" class="text-emerald-400 font-semibold flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
        Free Shipping Applied!
      </span>
      <span v-else class="text-slate-400">
        Add <span class="text-cyan-400 font-semibold">${{ remaining.toFixed(2) }}</span> for free shipping
      </span>
    </div>
    <div class="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-500 ease-out"
        :class="qualifies ? 'bg-emerald-400' : 'bg-gradient-to-r from-cyan-600 to-cyan-400'"
        :style="{ width: progress + '%' }"
      ></div>
    </div>
  </div>
</template>
