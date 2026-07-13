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
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-2">Forgot Password</h1>
      <p class="text-slate-400 text-sm text-center mb-6">Enter your email and we'll send you a reset link.</p>

      <template v-if="sent">
        <div class="p-4 rounded-lg bg-emerald-950/30 border border-emerald-700/50 text-emerald-300 text-sm text-center">
          If that email is registered, a reset link has been sent.
        </div>
        <div class="text-center mt-4">
          <router-link to="/login" class="text-cyan-400 hover:underline text-sm">Back to sign in</router-link>
        </div>
      </template>

      <form v-else @submit.prevent="requestReset" novalidate>
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
          >
          <p v-if="errors.email" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
          {{ pending ? 'Sending...' : 'Send Reset Link' }}
        </button>

        <div class="text-center mt-4">
          <router-link to="/login" class="text-cyan-400 hover:underline text-sm">Back to sign in</router-link>
        </div>
      </form>
    </div>
  </div>
  </div>
</template>
