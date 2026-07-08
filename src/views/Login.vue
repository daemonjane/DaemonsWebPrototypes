<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const { refresh } = useUser()
const email = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

async function login() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!email.value || !password.value) {
    if (!email.value) errors.email = 'Email is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const { api, ensureCSRF } = await import('../utils/api')
    const deviceId = localStorage.getItem('device_id') || crypto.randomUUID()
    localStorage.setItem('device_id', deviceId)
    const result = await api.osimartLogin(email.value, password.value, 'web', deviceId)
    if (result.osimart_token) {
      localStorage.setItem('osimart_token', result.osimart_token)
      if (result.osimart_refresh_token) {
        localStorage.setItem('osimart_refresh_token', result.osimart_refresh_token)
      }
    }
    await ensureCSRF()
    await refresh()
    router.push('/')
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
      <Breadcrumbs :crumbs="[{ label: 'Sign In' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-6">Sign In</h1>

      <form @submit.prevent="login" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <div class="mb-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email address"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.email }"
            aria-required="true"
            autocomplete="email"
            :aria-describedby="errors.email ? 'login-email-error' : undefined"
          >
          <p v-if="errors.email" id="login-email-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
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
            :aria-describedby="errors.password ? 'login-password-error' : undefined"
          >
          <p v-if="errors.password" id="login-password-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
          {{ pending ? 'Signing in...' : 'Login' }}
        </button>
      </form>

      <div class="text-center text-sm mt-4 space-y-2">
        <p>
          Don't have an account?
          <router-link to="/register" class="text-cyan-400 hover:underline">Register</router-link>
        </p>
        <p>
          <router-link to="/forgot-password" class="text-cyan-400 hover:underline">Forgot password?</router-link>
        </p>
      </div>
    </div>
  </div>
  </div>
</template>