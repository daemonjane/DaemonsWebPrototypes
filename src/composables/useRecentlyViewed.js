import { ref } from 'vue'
import { products } from '../data/products'

const STORAGE_KEY = 'techstore_recently_viewed'
const MAX_ITEMS = 6

let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const ids = ref(stored)

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ids.value))
}

/**
 * Composable that tracks the last 6 visited product IDs in localStorage.
 *
 * @returns {{
 *   items: import('vue').Ref<Object[]>,
 *   visit: (productId: string) => void
 * }}
 */
export function useRecentlyViewed() {
  const items = ref(
    ids.value
      .map(id => products.find(p => p.id === id))
      .filter(Boolean)
  )

  function visit(productId) {
    ids.value = ids.value.filter(id => id !== productId)
    ids.value.unshift(productId)
    if (ids.value.length > MAX_ITEMS) ids.value.pop()
    persist()
    items.value = ids.value
      .map(id => products.find(p => p.id === id))
      .filter(Boolean)
  }

  return { items, visit }
}
