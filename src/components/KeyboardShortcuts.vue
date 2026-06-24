<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const visible = ref(false)
const router = useRouter()

const shortcuts = [
  { key: '?', desc: 'Toggle this modal' },
  { key: 'h', desc: 'Go to Home' },
  { key: 's', desc: 'Go to Shop' },
  { key: 'f', desc: 'Go to Favorites' },
  { key: 'c', desc: 'Go to Checkout' },
  { key: 't', desc: 'Go to Order Tracking' },
  { key: 'Escape', desc: 'Close this modal' },
]

function handler(e) {
  if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
    e.preventDefault()
    visible.value = !visible.value
    return
  }
  if (e.key === 'Escape') { visible.value = false; return }
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return
  if (e.ctrlKey || e.metaKey) return
  const map = { h: '/', s: '/shop', f: '/favorites', c: '/checkout', t: '/tracking' }
  if (map[e.key]) {
    e.preventDefault()
    router.push(map[e.key])
    visible.value = false
  }
}

onMounted(() => window.addEventListener('keydown', handler))
onUnmounted(() => window.removeEventListener('keydown', handler))
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="visible = false">
      <div class="bg-slate-900 border border-slate-700 rounded-xl p-6 w-full max-w-sm mx-4 shadow-2xl">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-white">Keyboard Shortcuts</h2>
          <button @click="visible = false" class="text-slate-500 hover:text-white transition-colors text-sm">Close</button>
        </div>
        <div class="space-y-2">
          <div v-for="s in shortcuts" :key="s.key" class="flex items-center justify-between text-sm">
            <span class="text-slate-400">{{ s.desc }}</span>
            <kbd class="bg-slate-800 border border-slate-700 text-slate-200 font-mono text-xs px-2 py-0.5 rounded">{{ s.key }}</kbd>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>
