<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { resetPassword } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const route = useRoute()
const router = useRouter()
const email = ref(route.query.email || '')
const code = ref(route.query.code || route.params.token || '')

const password = ref('')
const confirmPassword = ref('')
const errors = reactive({})
const pending = ref(false)
const done = ref(false)

async function handleReset() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!email.value) {
    errors.email = 'Email is required.'
    return
  }
  if (!code.value) {
    errors.code = 'Reset code is required.'
    return
  }
  if (!password.value) {
    errors.password = 'Password is required.'
    return
  }
  if (password.value.length < 8) {
    errors.password = 'Password must be at least 8 characters.'
    return
  }
  if (password.value !== confirmPassword.value) {
    errors.confirm = 'Passwords do not match.'
    return
  }
  pending.value = true
  try {
    await resetPassword({ email: email.value, code: code.value, new_password: password.value })
    done.value = true
  } catch (e) {
    errors.form = e.message || 'Reset failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Reset Password' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-6">Set New Password</h1>

        <template v-if="done">
          <div class="p-4 rounded-lg bg-success-500/10 border border-success-500/30 text-success-400 text-sm text-center">
            Password has been reset successfully.
          </div>
          <div class="text-center mt-4">
            <router-link to="/login" class="text-gold-500 hover:text-gold-400 text-sm font-medium transition-colors">Sign in with your new password</router-link>
          </div>
        </template>

        <form v-else @submit.prevent="handleReset" novalidate>
          <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-danger-500/10 border border-danger-500/30 text-danger-400 text-sm" role="alert">{{ errors.form }}</p>

          <div class="mb-3">
            <label for="rp-email" class="block text-sm text-surface-300 mb-1.5 font-medium">Email address</label>
            <input
              id="rp-email"
              v-model="email"
              type="email"
              placeholder="you@example.com"
              class="w-full bg-surface-800 border border-surface-700 rounded-lg px-4 py-3 text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
              :class="{ 'border-danger-500': errors.email }"
              aria-required="true"
              autocomplete="email"
            >
            <p v-if="errors.email" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
          </div>

          <div class="mb-3">
            <label for="rp-code" class="block text-sm text-surface-300 mb-1.5 font-medium">Reset code</label>
            <input
              id="rp-code"
              v-model="code"
              type="text"
              placeholder="Enter the code from your email"
              class="w-full bg-surface-800 border border-surface-700 rounded-lg px-4 py-3 text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
              :class="{ 'border-danger-500': errors.code }"
              aria-required="true"
            >
            <p v-if="errors.code" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.code }}</p>
          </div>

          <div class="mb-3">
            <label for="rp-password" class="block text-sm text-surface-300 mb-1.5 font-medium">New password</label>
            <input
              id="rp-password"
              v-model="password"
              type="password"
              placeholder="Min. 8 characters"
              class="w-full bg-surface-800 border border-surface-700 rounded-lg px-4 py-3 text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
              :class="{ 'border-danger-500': errors.password }"
              aria-required="true"
              autocomplete="new-password"
            >
            <p v-if="errors.password" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
          </div>

          <div class="mb-4">
            <label for="rp-confirm" class="block text-sm text-surface-300 mb-1.5 font-medium">Confirm password</label>
            <input
              id="rp-confirm"
              v-model="confirmPassword"
              type="password"
              placeholder="Re-enter password"
              class="w-full bg-surface-800 border border-surface-700 rounded-lg px-4 py-3 text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
              :class="{ 'border-danger-500': errors.confirm }"
              aria-required="true"
              autocomplete="new-password"
            >
            <p v-if="errors.confirm" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.confirm }}</p>
          </div>

          <button type="submit" :disabled="pending" class="w-full bg-gold-500 text-surface-950 py-3 rounded-lg font-semibold hover:bg-gold-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-gold-500 disabled:opacity-50">
            {{ pending ? 'Resetting...' : 'Reset Password' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
