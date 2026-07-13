<script setup>
import { ref, reactive } from 'vue'
import { sendPasswordResetCode } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const email = ref('')
const errors = reactive({})
const pending = ref(false)
const sent = ref(false)

async function requestReset() {
  Object.keys(errors).forEach(k => delete errors[k])
  if (!email.value) {
    errors.email = 'Email is required.'
    return
  }
  pending.value = true
  try {
    await sendPasswordResetCode({ email: email.value })
    sent.value = true
  } catch (e) {
    errors.form = e.message || 'Request failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Forgot Password' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-2">Forgot Password</h1>
        <p class="text-surface-400 text-sm text-center mb-6">Enter your email and we'll send you a reset link.</p>

        <template v-if="sent">
          <div class="p-4 rounded-lg bg-success-500/10 border border-success-500/30 text-success-400 text-sm text-center">
            If that email is registered, a reset link has been sent.
          </div>
          <div class="text-center mt-4">
            <router-link to="/login" class="text-gold-500 hover:text-gold-400 text-sm font-medium transition-colors">Back to sign in</router-link>
          </div>
        </template>

        <form v-else @submit.prevent="requestReset" novalidate>
          <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-danger-500/10 border border-danger-500/30 text-danger-400 text-sm" role="alert">{{ errors.form }}</p>

          <div class="mb-4">
            <label for="fp-email" class="block text-sm text-surface-300 mb-1.5 font-medium">Email address</label>
            <input
              id="fp-email"
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

          <button type="submit" :disabled="pending" class="w-full bg-gold-500 text-surface-950 py-3 rounded-lg font-semibold hover:bg-gold-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-gold-500 disabled:opacity-50">
            {{ pending ? 'Sending...' : 'Send Reset Link' }}
          </button>

          <div class="text-center mt-4">
            <router-link to="/login" class="text-gold-500 hover:text-gold-400 text-sm font-medium transition-colors">Back to sign in</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
