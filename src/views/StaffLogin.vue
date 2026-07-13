<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { saveAuthSession } from '../services/login'
import { useUser } from '../composables/useUser'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const { setAuth } = useUser()
const email = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

const DJANGO_BASE = window.location.port === '5173'
  ? 'http://localhost:8000'
  : window.location.origin

async function staffLogin() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!email.value || !password.value) {
    if (!email.value) errors.email = 'Email is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const res = await fetch(`${DJANGO_BASE}/api/auth/staff-login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: email.value.trim(),
        password: password.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.error || 'Login failed')
    if (!data.is_staff) throw new Error('This account does not have staff access.')
    saveAuthSession({ access_token: data.id || 'django-session', user: data })
    setAuth(data)
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
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-6">Staff Sign In</h1>

        <form @submit.prevent="staffLogin" novalidate>
          <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-danger-950/30 border border-danger-700/50 text-danger-400 text-sm" role="alert">{{ errors.form }}</p>

          <div class="mb-4">
            <input
              v-model="email"
              type="email"
              placeholder="Email"
              class="w-full bg-surface-800 border border-surface-700 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-electric-500/50 focus:border-transparent text-surface-100"
              :class="{ 'border-danger-500': errors.email }"
              aria-required="true"
              autocomplete="email"
            >
            <p v-if="errors.email" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
          </div>

          <div class="mb-4">
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              class="w-full bg-surface-800 border border-surface-700 rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-electric-500/50 focus:border-transparent text-surface-100"
              :class="{ 'border-danger-500': errors.password }"
              aria-required="true"
              autocomplete="current-password"
            >
            <p v-if="errors.password" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
          </div>

          <button type="submit" :disabled="pending" class="w-full bg-electric-500 text-surface-950 py-3 rounded-xl font-display font-semibold hover:bg-electric-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-electric-500 disabled:opacity-50 shadow-glow-electric">
            {{ pending ? 'Signing in...' : 'Staff Login' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
