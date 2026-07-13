import { ref } from 'vue'

const STORAGE_KEY = 'vertex_recently_viewed'
const MAX_ITEMS = 6

let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const items = ref(stored)

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
}

export function useRecentlyViewed() {
  function visit(product) {
    items.value = items.value.filter(item => item.id !== product.id)
    items.value.unshift({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
    })
    if (items.value.length > MAX_ITEMS) items.value.pop()
    persist()
  }

  return { items, visit }
}
