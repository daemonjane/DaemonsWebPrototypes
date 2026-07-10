import { reactive, toRefs } from 'vue'
import { getAuthToken, logoutAuth } from '../services/login.js'

const state = reactive({
  user: null,
  loaded: false,
})

function loadFromStorage() {
  try {
    const raw = localStorage.getItem('gg-user')
    if (raw) state.user = JSON.parse(raw)
  } catch { state.user = null }
}

export function useUser() {
  async function refresh() {
    loadFromStorage()
    state.loaded = true
    if (state.user) {
      await syncWishlist()
    }
  }

  function setAuth(userData) {
    state.user = userData
    if (userData) {
      localStorage.setItem('gg-user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('gg-user')
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
    state.user = null
    localStorage.removeItem('gg-user')
    logoutAuth()
  }

  return {
    ...toRefs(state),
    refresh,
    logout,
    setAuth,
    isAuthenticated: () => !!state.user?.id,
    isStaff: () => !!state.user?.is_staff,
  }
}
