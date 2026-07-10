import { ref, computed } from 'vue'

const STORAGE_KEY = 'gg_favorites'
let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const localIds = ref(stored)

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(localIds.value))
}

export function useFavorites() {
  const ids = computed(() => localIds.value)
  const count = computed(() => ids.value.length)

  async function init() {
    try {
      const { getAuthToken } = await import('../services/login.js')
      if (!getAuthToken()) return
      const { api } = await import('../utils/api')
      const data = await api.wishlist.get()
      if (data?.product_slugs?.length) {
        localIds.value = data.product_slugs
        persist()
      }
    } catch {
      // fallback to local
    }
  }

  async function toggle(productId) {
    const idx = localIds.value.indexOf(productId)
    if (idx === -1) {
      localIds.value.push(productId)
    } else {
      localIds.value.splice(idx, 1)
    }
    persist()
    try {
      const { api } = await import('../utils/api')
      await api.wishlist.toggle(productId)
    } catch {
      // local-only is fine
    }
  }

  function isFavorite(productId) {
    return localIds.value.includes(productId)
  }

  function clear() {
    localIds.value = []
    persist()
  }

  return { ids, count, init, toggle, isFavorite, clear }
}
