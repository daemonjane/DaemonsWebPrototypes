<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { validateForm } from '../utils/validation'

const router = useRouter()
const email = ref('')
const password = ref('')
const errors = reactive({})

function login() {
  Object.keys(errors).forEach(key => delete errors[key])

  const validationErrors = validateForm(
    { email: email.value, password: password.value },
    { email: ['required', 'email'], password: ['required'] }
  )

  if (Object.keys(validationErrors).length > 0) {
    Object.assign(errors, validationErrors)
    return
  }

  localStorage.setItem('techstore_user', JSON.stringify({ email: email.value }))
  router.push('/')
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[60vh]">
    <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Sign In</h1>
      <form @submit.prevent="login">
        <div class="mb-4">
          <input v-model="email" type="email" placeholder="Email" class="w-full bg-slate-800 border border-slate-700 rounded p-3" :class="{ 'border-pink-500': errors.email }">
          <p v-if="errors.email" class="text-pink-400 text-xs mt-1">{{ errors.email }}</p>
        </div>
        <div class="mb-4">
          <input v-model="password" type="password" placeholder="Password" class="w-full bg-slate-800 border border-slate-700 rounded p-3" :class="{ 'border-pink-500': errors.password }">
          <p v-if="errors.password" class="text-pink-400 text-xs mt-1">{{ errors.password }}</p>
        </div>
        <button type="submit" class="w-full bg-cyan-600 py-3 rounded-md font-semibold">Login</button>
      </form>
      <p class="text-center text-sm mt-4">Don't have an account? <router-link to="/register" class="text-cyan-400">Register</router-link></p>
    </div>
  </div>
</template>