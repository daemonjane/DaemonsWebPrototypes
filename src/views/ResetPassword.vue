<script setup>
import { ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { resetPassword } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const route = useRoute()
const router = useRouter()
const email = ref(route.query.email || '')
const code = ref(route.query.code || '')

const password = ref('')
const confirmPassword = ref('')
const errors = reactive({})
const pending = ref(false)
const done = ref(false)

async function handleReset() {
  Object.keys(errors).forEach(k => delete errors[k])
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
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-6">Set New Password</h1>

      <template v-if="done">
        <div class="p-4 rounded-lg bg-emerald-950/30 border border-emerald-700/50 text-emerald-300 text-sm text-center">
          Password has been reset successfully.
        </div>
        <div class="text-center mt-4">
          <router-link to="/login" class="text-cyan-400 hover:underline text-sm">Sign in with your new password</router-link>
        </div>
      </template>

      <form v-else @submit.prevent="handleReset" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <div class="mb-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email address"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            aria-required="true"
            autocomplete="email"
          >
        </div>

        <div class="mb-4">
          <input
            v-model="code"
            type="text"
            placeholder="Reset code from email"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            aria-required="true"
          >
        </div>

        <div class="mb-4">
          <input
            v-model="password"
            type="password"
            placeholder="New password"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.password }"
            aria-required="true"
            autocomplete="new-password"
          >
          <p v-if="errors.password" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
        </div>

        <div class="mb-4">
          <input
            v-model="confirmPassword"
            type="password"
            placeholder="Confirm new password"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.confirm }"
            aria-required="true"
            autocomplete="new-password"
          >
          <p v-if="errors.confirm" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.confirm }}</p>
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
          {{ pending ? 'Resetting...' : 'Reset Password' }}
        </button>
      </form>
    </div>
  </div>
  </div>
</template>
