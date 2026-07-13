<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { verifyEmail, resendVerificationCode, login, saveAuthSession } from '../services/login.js'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const route = useRoute()

const email = ref(route.query.email || '')
const code = ref('')
const error = ref('')
const pending = ref(false)
const resending = ref(false)
const resent = ref(false)
const sessionExpired = ref(false)

onMounted(() => {
  if (!email.value) {
    router.push('/register')
  }
})

function handleError(e) {
  const msg = e.message || ''
  if (msg.toLowerCase().includes('no pending registration')) {
    sessionExpired.value = true
  }
  error.value = msg || 'Verification failed'
}

async function verify() {
  if (!code.value || code.value.length < 4) {
    error.value = 'Please enter the verification code.'
    return
  }
  error.value = ''
  pending.value = true
  try {
    await verifyEmail({ email: email.value, code: code.value })
    const password = localStorage.getItem('gg-pending-password') || ''
    if (password) {
      const data = await login({ email: email.value, password })
      saveAuthSession(data)
      localStorage.removeItem('gg-pending-password')
    }
    router.push('/login?verified=1')
  } catch (e) {
    handleError(e)
  } finally {
    pending.value = false
  }
}

async function resend() {
  error.value = ''
  resent.value = false
  resending.value = true
  try {
    await resendVerificationCode({ email: email.value })
    resent.value = true
  } catch (e) {
    handleError(e)
  } finally {
    resending.value = false
  }
}
</script>

<template>
  <div>
    <div class="max-w-md mx-auto px-4 pt-4">
      <Breadcrumbs :crumbs="[{ label: 'Verify Email' }]" />
    </div>
    <div class="flex items-center justify-center min-h-[60vh]">
      <div class="bg-slate-900 p-8 rounded-2xl border border-slate-700 w-full max-w-md">
        <h1 class="text-2xl font-bold text-center mb-2">Verify Your Email</h1>
        <p class="text-slate-400 text-sm text-center mb-6">
          Enter the verification code sent to <strong class="text-slate-200">{{ email }}</strong>
        </p>

        <template v-if="sessionExpired">
          <div class="mb-4 p-4 rounded-lg bg-amber-950/30 border border-amber-700/50 text-amber-300 text-sm">
            Your verification session has expired. Please register again to receive a new code.
          </div>
          <router-link to="/register" class="block w-full text-center bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all">
            Register Again
          </router-link>
        </template>

        <template v-else>
          <form @submit.prevent="verify" novalidate>
            <p v-if="error" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ error }}</p>
            <p v-if="resent" class="mb-4 p-3 rounded-lg bg-emerald-950/30 border border-emerald-700/50 text-emerald-300 text-sm">A new code has been sent to your email.</p>

            <div class="mb-6">
              <input
                v-model="code"
                type="text"
                inputmode="numeric"
                placeholder="Enter verification code"
                maxlength="8"
                class="w-full bg-slate-800 border border-slate-700 rounded p-3 text-center text-xl tracking-widest focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent"
                autocomplete="one-time-code"
              >
            </div>

            <button type="submit" :disabled="pending" class="w-full bg-cyan-600 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus-visible:outline-2 focus-visible:outline-cyan-400 disabled:opacity-50">
              {{ pending ? 'Verifying...' : 'Verify Email' }}
            </button>
          </form>

          <div class="text-center mt-6">
            <button
              @click="resend"
              :disabled="resending"
              class="text-sm text-cyan-400 hover:underline disabled:opacity-50 disabled:no-underline"
            >
              {{ resending ? 'Sending...' : 'Resend verification code' }}
            </button>
          </div>

          <p class="text-center text-sm mt-4">
            <router-link to="/login" class="text-cyan-400 hover:underline">Back to Login</router-link>
          </p>
        </template>
      </div>
    </div>
  </div>
</template>
