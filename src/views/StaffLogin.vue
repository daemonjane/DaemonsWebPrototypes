<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login, saveAuthSession } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

async function staffLogin() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!email.value || !password.value) {
    if (!email.value) errors.email = 'Email is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const data = await login({ email: email.value, password: password.value })
    saveAuthSession(data)
    if (!data?.user?.is_staff) {
      errors.form = 'This account does not have staff access.'
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
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-6">Staff Sign In</h1>

        <form @submit.prevent="staffLogin" novalidate>
          <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

          <div class="mb-4">
            <input
              v-model="email"
              type="email"
              placeholder="Email"
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
              :class="{ 'border-pink-500': errors.email }"
              aria-required="true"
              autocomplete="email"
            >
            <p v-if="errors.email" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
          </div>

          <div class="mb-4">
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
              :class="{ 'border-pink-500': errors.password }"
              aria-required="true"
              autocomplete="current-password"
            >
            <p v-if="errors.password" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
          </div>

          <button type="submit" :disabled="pending" class="w-full bg-gold-500 py-3 rounded-lg font-semibold hover:bg-gold-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-gold-500 disabled:opacity-50">
            {{ pending ? 'Signing in...' : 'Staff Login' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
