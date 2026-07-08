<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const { refresh } = useUser()
const loginField = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

// Staff login fields
const staffMode = ref(false)
const staffUsername = ref('')
const staffPassword = ref('')

async function login() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (staffMode.value) {
    await staffLogin()
    return
  }
  if (!loginField.value || !password.value) {
    if (!loginField.value) errors.loginField = 'Email or username is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const { api, ensureCSRF } = await import('../utils/api')
    const result = await api.osimartLogin(loginField.value, password.value, 'web')
    await ensureCSRF()
    await refresh()
    router.push('/')
  } catch (e) {
    errors.form = e.message || 'Login failed'
  } finally {
    pending.value = false
  }
}

async function staffLogin() {
  if (!staffUsername.value || !staffPassword.value) {
    if (!staffUsername.value) errors.username = 'Username is required.'
    if (!staffPassword.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const { api, ensureCSRF } = await import('../utils/api')
    await api.login(staffUsername.value, staffPassword.value)
    await ensureCSRF()
    await refresh()
    const { user } = useUser()
    if (!user.value?.is_staff) {
      errors.form = 'This account does not have staff access.'
      await api.logout()
      return
    }
    router.push('/admin/osimart')
  } catch (e) {
    errors.form = e.message || 'Staff login failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: staffMode ? 'Staff Sign In' : 'Sign In' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-6">{{ staffMode ? 'Staff Sign In' : 'Sign In' }}</h1>

        <!-- Mode toggle -->
        <div class="flex justify-center mb-6">
          <button @click="staffMode = !staffMode" class="px-4 py-2 text-sm rounded-lg font-medium transition-all" :class="staffMode ? 'bg-cyan-600 text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-600'">
            {{ staffMode ? 'Customer login' : 'Admin / Staff login' }}
          </button>
        </div>

      <form @submit.prevent="login" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <!-- Customer fields -->
        <template v-if="!staffMode">
          <div class="mb-4">
            <input
              v-model="loginField"
              type="text"
              placeholder="Email or username"
              class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              :class="{ 'border-pink-500': errors.loginField }"
              aria-required="true"
              autocomplete="username"
              :aria-describedby="errors.loginField ? 'login-field-error' : undefined"
            >
            <p v-if="errors.loginField" id="login-field-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.loginField }}</p>
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
        </template>

        <!-- Staff fields -->
        <template v-else>
          <div class="mb-4">
            <input
              v-model="staffUsername"
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
              v-model="staffPassword"
              type="password"
              placeholder="Password"
              class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
              :class="{ 'border-pink-500': errors.password }"
              aria-required="true"
              autocomplete="current-password"
            >
            <p v-if="errors.password" id="login-password-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
          </div>
        </template>

        <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
          {{ pending ? 'Signing in...' : (staffMode ? 'Staff Login' : 'Login') }}
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
