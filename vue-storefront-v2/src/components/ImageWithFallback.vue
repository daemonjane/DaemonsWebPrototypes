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
  <img v-if="!error" :src="src" :alt="alt" :class="class" @error="onError" />
  <div v-else :class="class" class="bg-slate-700 flex items-center justify-center text-slate-500 text-sm">
    {{ alt }}
  </div>
</template>