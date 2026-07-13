import { ref, onMounted, onUnmounted } from 'vue'

const VISITOR_KEY = 'vertex_visitor_count'
const base = parseInt(localStorage.getItem(VISITOR_KEY) || '142', 10)
const count = ref(base)
let interval = null

export function useLiveVisitorCount() {
  function start() {
    interval = setInterval(() => {
      const delta = Math.random() > 0.3 ? 1 : -1
      count.value = Math.max(1, count.value + delta)
      localStorage.setItem(VISITOR_KEY, String(count.value))
    }, 4000)
  }

  function stop() {
    if (interval) clearInterval(interval)
  }

  onMounted(start)
  onUnmounted(stop)

  return { count }
}
