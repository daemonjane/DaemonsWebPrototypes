<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  target: { type: Number, required: true },
  suffix: { type: String, default: '' },
  prefix: { type: String, default: '' },
  label: { type: String, required: true },
  decimals: { type: Number, default: 0 },
  duration: { type: Number, default: 2000 },
})

const count = ref(0)
const visible = ref(false)
const elementRef = ref(null)
let observer = null
let rafId = null

function animate(from, to, duration) {
  const start = performance.now()
  function tick(now) {
    const elapsed = now - start
    const progress = Math.min(elapsed / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    count.value = from + (to - from) * eased
    if (progress < 1) {
      rafId = requestAnimationFrame(tick)
    } else {
      count.value = to
    }
  }
  rafId = requestAnimationFrame(tick)
}

onMounted(() => {
  if (elementRef.value) {
    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !visible.value) {
          visible.value = true
          animate(0, props.target, props.duration)
          if (observer) observer.disconnect()
        }
      },
      { threshold: 0.3 }
    )
    observer.observe(elementRef.value)
  }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
  if (rafId) cancelAnimationFrame(rafId)
})
</script>

<template>
  <div ref="elementRef" class="text-center space-y-1">
    <div class="text-3xl sm:text-4xl font-bold font-mono text-cyan-400">
      {{ prefix }}<span>{{ count.toFixed(decimals) }}</span>{{ suffix }}
    </div>
    <div class="text-xs sm:text-sm text-slate-400 uppercase tracking-wider font-medium">{{ label }}</div>
  </div>
</template>
