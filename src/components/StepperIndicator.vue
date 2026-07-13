<script setup>
defineProps({
  steps: { type: Array, required: true },
  current: { type: Number, default: 0 },
})
</script>

<template>
  <div class="flex items-center justify-center gap-0 mb-8">
    <template v-for="(step, i) in steps" :key="i">
      <div class="flex items-center">
        <div
          class="flex items-center justify-center w-8 h-8 rounded-full text-xs font-bold transition-all duration-300"
          :class="i === current
            ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-900/40 scale-110'
            : i < current
              ? 'bg-emerald-600 text-white'
              : 'bg-charcoal-700 text-charcoal-500'"
        >
          <svg v-if="i < current" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
          </svg>
          <span v-else>{{ i + 1 }}</span>
        </div>
        <span class="hidden sm:inline text-xs ml-2 mr-2 font-medium" :class="i === current ? 'text-electric-400' : i < current ? 'text-emerald-400' : 'text-charcoal-500'">
          {{ step }}
        </span>
      </div>
      <div v-if="i < steps.length - 1" class="w-10 sm:w-16 h-px mx-1" :class="i < current ? 'bg-emerald-600' : 'bg-charcoal-600'"></div>
    </template>
  </div>
</template>
