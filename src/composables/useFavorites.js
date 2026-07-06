import { ref, computed } from 'vue'

const STORAGE_KEY = 'techstore_favorites'
let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const localIds = ref(stored)
const serverSlugs = ref([])
let useServer = false

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(localIds.value))
}

export function useFavorites() {
  const ids = computed(() => {
    if (useServer) return serverSlugs.value
    return localIds.value
  })

  const count = computed(() => ids.value.length)

  async function init() {
    try {
      const { useUser } = await import('./useUser')
      const { user } = useUser()
      if (!user.value) {
        useServer = false
        return
      }
      const { api } = await import('../utils/api')
      const data = await api.wishlist.get()
      serverSlugs.value = data.product_slugs || []
      useServer = true
    } catch {
      useServer = false
    }
  }

  async function toggle(productId) {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        const data = await api.wishlist.toggle(productId)
        serverSlugs.value = data.product_slugs || []
      } catch {
        // fallback to local
        toggleLocal(productId)
      }
      return
    }
    toggleLocal(productId)
  }

  function toggleLocal(productId) {
    const idx = localIds.value.indexOf(productId)
    if (idx === -1) {
      localIds.value.push(productId)
    } else {
      localIds.value.splice(idx, 1)
    }
    persist()
  }

  function isFavorite(productId) {
    return ids.value.includes(productId)
  }

  async function clear() {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        for (const slug of serverSlugs.value) {
          await api.wishlist.toggle(slug)
        }
        serverSlugs.value = []
      } catch {
        // ignore
      }
      return
    }
    localIds.value = []
    persist()
  }

  return { ids, count, init, toggle, isFavorite, clear }
}
