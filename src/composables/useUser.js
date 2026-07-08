import { reactive, toRefs } from 'vue'

const state = reactive({
  user: null,
  loaded: false,
})

export function useUser() {
  async function refresh() {
    try {
      const { api } = await import('../utils/api')
      state.user = await api.profile.get()
    } catch {
      state.user = null
    } finally {
      state.loaded = true
    }
    if (state.user) {
      await Promise.allSettled([
        syncCart(),
        syncWishlist(),
      ])
    }
  }

  async function syncCart() {
    try {
      const { useCart } = await import('./useCart')
      const cart = useCart()
      await cart.mergeLocalIntoServer()
      await cart.init()
    } catch {
      // ignore
    }
  }

  async function syncWishlist() {
    try {
      const { useFavorites } = await import('./useFavorites')
      const favs = useFavorites()
      await favs.init()
    } catch {
      // ignore
    }
  }

  async function logout() {
    try {
      const { api } = await import('../utils/api')
      await api.logout()
    } catch { /* ignore */ }
    state.user = null
  }

  return {
    ...toRefs(state),
    refresh,
    logout,
    isAuthenticated: () => !!state.user?.id,
    isStaff: () => !!state.user?.is_staff,
  }
}
