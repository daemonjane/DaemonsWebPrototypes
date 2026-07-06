<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  aspect: { type: String, default: null },
  loading: { type: String, default: 'lazy' },
  priority: { type: Boolean, default: false },
  imgClass: { type: String, default: '' },
  wrapperClass: { type: String, default: '' }
})

const loaded = ref(false)
const errored = ref(false)

const resolvedSrc = computed(() => {
  if (!props.src) return '/assets/placeholder.svg'
  if (props.src.startsWith('http')) return props.src
  return `https://api.osimart.com/${props.src.replace(/^\//, '')}`
})

function onLoad() { loaded.value = true }
function onError() { errored.value = true; loaded.value = true }
</script>

<template>
  <div
    class="relative overflow-hidden bg-slate-800"
    :class="wrapperClass"
    :style="aspect ? { aspectRatio: aspect } : {}"
  >
    <div v-if="!loaded" class="absolute inset-0 bg-slate-800/50 animate-pulse" />

    <img
      v-if="!errored"
      :src="resolvedSrc"
      :alt="alt"
      :class="['w-full h-full object-cover transition-opacity duration-500', loaded ? 'opacity-100' : 'opacity-0', imgClass]"
      :loading="priority ? 'eager' : loading"
      :fetchpriority="priority ? 'high' : undefined"
      @load="onLoad"
      @error="onError"
    />

    <div
      v-else
      class="absolute inset-0 flex items-center justify-center text-slate-600"
      role="img"
      :aria-label="alt || 'Image unavailable'"
    >
      <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
      </svg>
    </div>
  </div>
</template>
