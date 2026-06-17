<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useCounter } from '../composables/useCounter'

const { count, increment, decrement, reset } = useCounter()

function handleKeydown(e) {
  if (e.key === 'ArrowUp') { e.preventDefault(); increment() }
  if (e.key === 'ArrowDown') { e.preventDefault(); decrement() }
}

onMounted(() => window.addEventListener('keydown', handleKeydown))
onUnmounted(() => window.removeEventListener('keydown', handleKeydown))
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950 px-4">
    <div class="text-center max-w-md w-full">
      <h1 class="text-3xl font-bold text-cyan-400 mb-2">Counter Feature</h1>
      <p class="text-slate-400 mb-8">Press <kbd class="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 text-sm font-mono">↑</kbd> <kbd class="px-2 py-0.5 rounded bg-slate-800 text-cyan-300 text-sm font-mono">↓</kbd> or click the buttons</p>

      <div class="text-8xl font-bold text-white mb-8 tabular-nums transition-all duration-200" :class="count >= 0 ? 'text-cyan-400' : 'text-rose-400'">
        {{ count }}
      </div>

      <div class="flex gap-4 justify-center">
        <button @click="decrement" class="px-8 py-3 rounded-xl bg-slate-800 text-white text-2xl font-bold hover:bg-slate-700 transition-colors focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Decrement">−</button>
        <button @click="reset" class="px-8 py-3 rounded-xl bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors focus-visible:outline-2 focus-visible:outline-cyan-400">Reset</button>
        <button @click="increment" class="px-8 py-3 rounded-xl bg-slate-800 text-white text-2xl font-bold hover:bg-slate-700 transition-colors focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Increment">+</button>
      </div>
    </div>
  </div>
</template>
