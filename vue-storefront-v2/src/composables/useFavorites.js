import { ref, computed } from 'vue'
import { products } from '../data/products'

const STORAGE_KEY = 'techstore_favorites'

const ids = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(ids.value))
}

/**
 * Composable for managing a wishlist of favorite products.
 * Persists to localStorage automatically.
 *
 * @returns {{
 *   favoriteIds: import('vue').Ref<string[]>,
 *   items: import('vue').ComputedRef<Object[]>,
 *   count: import('vue').ComputedRef<number>,
 *   toggle: (productId: string) => void,
 *   isFavorite: (productId: string) => boolean,
 *   clear: () => void
 * }}
 */
export function useFavorites() {
  const favoriteIds = ids

  const items = computed(() =>
    ids.value.map(id => products.find(p => p.id === id)).filter(Boolean)
  )

  const count = computed(() => ids.value.length)

  function toggle(productId) {
    const idx = ids.value.indexOf(productId)
    if (idx === -1) {
      ids.value.push(productId)
    } else {
      ids.value.splice(idx, 1)
    }
    persist()
  }

  function isFavorite(productId) {
    return ids.value.includes(productId)
  }

  function clear() {
    ids.value = []
    persist()
  }

  return { favoriteIds, items, count, toggle, isFavorite, clear }
}
