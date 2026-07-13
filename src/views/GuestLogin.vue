<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { saveAuthSession } from '../services/login'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const errors = reactive({})
const pending = ref(false)

async function guestLogin() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (!firstName.value) {
    errors.firstName = 'First name is required.'
    return
  }
  pending.value = true
  try {
    const guestUser = {
      id: 'guest_' + Date.now(),
      email: email.value || '',
      first_name: firstName.value,
      last_name: lastName.value,
      is_guest: true,
    }
    localStorage.setItem('gg-user', JSON.stringify(guestUser))
    window.dispatchEvent(new Event('storage'))
    router.push('/checkout')
  } catch (e) {
    errors.form = e.message || 'Guest login failed'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Guest Login' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-surface-900 p-8 rounded-2xl border border-surface-700 w-full max-w-md">
        <h1 class="text-2xl font-bold font-display text-center mb-2">Continue as Guest</h1>
        <p class="text-sm text-surface-400 text-center mb-6">No password needed — we'll save your info for next time.</p>

      <form @submit.prevent="guestLogin" novalidate>
        <p v-if="errors.form" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.form }}</p>

        <div class="flex gap-3 mb-4">
          <div class="flex-1">
            <input
              v-model="firstName"
              type="text"
              placeholder="First name"
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-electric-500/50 focus:border-transparent"
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
              class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-electric-500/50 focus:border-transparent"
              autocomplete="family-name"
            >
          </div>
        </div>

        <div class="mb-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email (optional)"
            class="w-full bg-surface-800 border border-surface-700 rounded p-3 focus:outline-none focus:ring-2 focus:ring-electric-500/50 focus:border-transparent"
            autocomplete="email"
          >
        </div>

        <button type="submit" :disabled="pending" class="w-full bg-electric-500 py-3 rounded-lg font-semibold hover:bg-electric-400 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-electric-500 disabled:opacity-50">
          {{ pending ? 'Continuing...' : 'Continue as Guest' }}
        </button>
      </form>

      <div class="text-center text-sm mt-4 space-y-2">
        <p>
          Want to create an account?
          <router-link to="/register" class="text-electric-500 hover:underline">Register</router-link>
        </p>
        <p>
          Already have an account?
          <router-link to="/login" class="text-electric-500 hover:underline">Sign In</router-link>
        </p>
      </div>
    </div>
  </div>
  </div>
</template>
