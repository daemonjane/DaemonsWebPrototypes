<script setup>
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