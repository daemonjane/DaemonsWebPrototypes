<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'

const router = useRouter()
const { refresh } = useUser()
const username = ref('')
const email = ref('')
const password = ref('')
const errors = reactive({})
const pending = ref(false)

async function register() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!username.value || !email.value || !password.value) {
    if (!username.value) errors.username = 'Username is required.'
    if (!email.value) errors.email = 'Email is required.'
    if (!password.value) errors.password = 'Password is required.'
    return
  }
  pending.value = true
  try {
    const { api } = await import('../utils/api')
    await api.register(username.value, email.value, password.value)
    await refresh()
    router.push('/')
  } catch (e) {
    errors.form = e.message || 'Registration failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[60vh]">
    <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Create Account</h1>

      <form @submit.prevent="register" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <div class="mb-4">
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.username }"
            aria-required="true"
          >
          <p v-if="errors.username" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.username }}</p>
        </div>

        <div class="mb-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.email }"
            aria-required="true"
          >
          <p v-if="errors.email" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
        </div>

        <div class="mb-4">
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full bg-slate-800 border border-slate-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
            :class="{ 'border-pink-500': errors.password }"
            aria-required="true"
          >
          <p v-if="errors.password" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.password }}</p>
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
          {{ pending ? 'Creating account...' : 'Register' }}
        </button>
      </form>

      <p class="text-center text-sm mt-4">
        Already have an account?
        <router-link to="/login" class="text-cyan-400 hover:underline">Login</router-link>
      </p>
    </div>
  </div>
</template>