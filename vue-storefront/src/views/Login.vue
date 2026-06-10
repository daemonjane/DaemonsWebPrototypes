<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const email = ref('')
const password = ref('')

function login() {
  localStorage.setItem('techstore_user', JSON.stringify({ email: email.value }))
  router.push('/')
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[60vh]">
    <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6">Sign In</h1>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Email" class="w-full bg-slate-800 border border-slate-700 rounded p-3 mb-4" required>
        <input v-model="password" type="password" placeholder="Password" class="w-full bg-slate-800 border border-slate-700 rounded p-3 mb-4" required>
        <button type="submit" class="w-full bg-cyan-600 py-3 rounded-md font-semibold">Login</button>
      </form>
      <p class="text-center text-sm mt-4">Don't have an account? <router-link to="/register" class="text-cyan-400">Register</router-link></p>
    </div>
  </div>
</template>