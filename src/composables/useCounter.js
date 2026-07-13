import { ref, watch } from 'vue'

const STORAGE_KEY = 'vertex_counter'

function loadSaved() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved !== null) return parseInt(saved, 10)
  } catch {}
  return 0
}

const count = ref(loadSaved())

watch(count, (val) => {
  localStorage.setItem(STORAGE_KEY, String(val))
})

export function useCounter() {
  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  return { count, increment, decrement, reset }
}
