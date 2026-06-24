<script setup>
/**
 * Image component that falls back to showing alt text on load error.
 *
 * @component
 * @prop {string} src - Image source URL
 * @prop {string} alt - Alt text (shown on error)
 * @prop {string} [class] - Additional CSS classes
 */
import { ref } from 'vue'
const props = defineProps({
  src: String,
  alt: String,
  class: String
})
const error = ref(false)
function onError() { error.value = true }
</script>

<template>
  <img v-if="!error" :src="src" :alt="alt" :class="class" loading="lazy" @error="onError" />
  <div v-else :class="class" class="bg-slate-700 flex items-center justify-center text-slate-500 text-sm gap-2" role="img" :aria-label="alt">
    <svg class="w-6 h-6 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
    <span>{{ alt }}</span>
  </div>
</template>