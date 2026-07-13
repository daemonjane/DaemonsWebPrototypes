<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { signup } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const phone = ref('')
const errors = reactive({})
const pending = ref(false)

async function register() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!firstName.value || !email.value || !password.value) {
    if (!firstName.value) errors.firstName = 'First name is required.'
    if (!email.value) errors.email = 'Email is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const name = `${firstName.value} ${lastName.value}`.trim()
    await signup({ name, email: email.value, password: password.value, phone: phone.value })
    router.push(`/verify-email?email=${encodeURIComponent(email.value)}`)
  } catch (e) {
    errors.form = e.message || 'Registration failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Create Account' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-6">Create Account</h1>

      <form @submit.prevent="register" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <div class="flex gap-3 mb-4">
          <div class="flex-1">
            <input
              v-model="firstName"
              type="text"
              placeholder="First name"
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
              :class="{ 'border-pink-500': errors.firstName }"
              aria-required="true"
              autocomplete="given-name"
            >
            <p v-if="errors.firstName" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.firstName }}</p>
          </div>
          <div class="flex-1">
            <input
              v-model="lastName"
              type="text"
              placeholder="Last name"
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
              autocomplete="family-name"
            >
          </div>
        </div>

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
            v-model="phone"
            type="tel"
            placeholder="Phone (optional)"
            class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
            autocomplete="tel"
          >
        </div>

        <div class="mb-4">
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-gold-500/50 focus:border-transparent"
            :class="{ 'border-pink-500': errors.password }"
            aria-required="true"
            autocomplete="new-password"
          >
          <p v-if="errors.password" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-gold-500 py-3 rounded-lg font-semibold hover:bg-gold-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-gold-500 disabled:opacity-50">
          {{ pending ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <p class="text-center text-sm mt-4">
        Already have an account?
        <router-link to="/login" class="text-gold-500 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
  </div>
</template>
