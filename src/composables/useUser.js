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
