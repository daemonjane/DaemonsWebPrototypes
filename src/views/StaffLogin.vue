<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const { setAuth } = useUser()
const username = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

async function login() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!username.value || !password.value) {
    if (!username.value) errors.username = 'Username is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const { api } = await import('../utils/api')
    const data = await api.staffLogin(username.value, password.value)
    setAuth(data)
    if (!data?.is_staff) {
      errors.form = 'This account does not have staff access.'
      await api.logout()
      return
    }
    router.push('/admin/osimart')
  } catch (e) {
    errors.form = e.message || 'Login failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Staff Sign In' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-6">Staff Sign In</h1>

        <form @submit.prevent="login" novalidate>
          <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

          <div class="mb-4">
            <input
              v-model="username"
              type="text"
              placeholder="Username"
              class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              :class="{ 'border-pink-500': errors.username }"
              aria-required="true"
              autocomplete="username"
            >
            <p v-if="errors.username" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.username }}</p>
          </div>

          <div class="mb-4">
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              :class="{ 'border-pink-500': errors.password }"
              aria-required="true"
              autocomplete="current-password"
            >
            <p v-if="errors.password" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
          </div>

          <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
            {{ pending ? 'Signing in...' : 'Staff Login' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
