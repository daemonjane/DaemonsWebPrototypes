<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { login, signup, saveAuthSession, verifyEmail, resendVerificationCode } from "../services/login.js"
import { useOsimartCart } from "../composables/useOsimartCart"
import { useWishlistStore } from "../composables/useWishlistStore"

const router = useRouter()
const { setUser: setUserForCart } = useOsimartCart()
const wishlistStore = useWishlistStore()

const mode = ref("login")
const name = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const verificationCode = ref("")
const error = ref("")
const successMessage = ref("")
const loading = ref(false)
const resending = ref(false)

function switchMode(next) {
  mode.value = next
  error.value = ""
  successMessage.value = ""
  verificationCode.value = ""
}

async function handleSubmit() {
  error.value = ""
  successMessage.value = ""
  loading.value = true

  const cleanEmail = email.value.trim()
  const cleanPassword = password.value
  const cleanName = name.value.trim()

  try {
    if (mode.value === "login") {
      const data = await login({ email: cleanEmail, password: cleanPassword })
      saveAuthSession(data)
      setUserForCart(cleanEmail)
      wishlistStore.setUser(cleanEmail)
      window.dispatchEvent(new Event("storage"))
      router.push("/")
    } else {
      await signup({ name: cleanName, email: cleanEmail, password: cleanPassword, phone: phone.value.trim() })
      successMessage.value = "Account created! Please check your email for a verification code."
      mode.value = "verify"
    }
  } catch (err) {
    console.error(`[Login.vue] ${mode.value} failed:`, err)
    error.value = err.message || "An error occurred. Please try again."
  } finally {
    loading.value = false
  }
}

async function handleResendCode() {
  error.value = ""
  successMessage.value = ""
  resending.value = true
  try {
    await resendVerificationCode({ email: email.value.trim() })
    successMessage.value = "A new code has been sent to your email."
  } catch (err) {
    console.error("[Login.vue] resend code failed:", err)
    error.value = err.message || "Could not resend the code. Please try again."
  } finally {
    resending.value = false
  }
}

async function handleVerify() {
  error.value = ""
  successMessage.value = ""
  loading.value = true
  const cleanEmail = email.value.trim()
  try {
    await verifyEmail({ email: cleanEmail, code: verificationCode.value.trim() })
    const data = await login({ email: cleanEmail, password: password.value })
    saveAuthSession(data)
    setUserForCart(cleanEmail)
    wishlistStore.setUser(cleanEmail)
    window.dispatchEvent(new Event("storage"))
    router.push("/")
  } catch (err) {
    console.error("[Login.vue] verification workflow failed:", err)
    error.value = err.message || "Verification code is incorrect or expired."
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex items-center justify-center min-h-[80vh]">
    <div class="w-full max-w-md bg-surface-800/60 shadow-elevated rounded-2xl p-8 sm:p-10 border border-surface-700">
      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="font-display text-3xl font-bold text-gold-500 tracking-tight">VERTEX</h1>
        <p class="text-surface-400 text-sm mt-2">
          {{
            mode === "login" ? "Sign in to your account" :
            mode === "signup" ? "Create your account" :
            "Verify your email address"
          }}
        </p>
      </div>

      <!-- Success message -->
      <div v-if="successMessage" class="mb-6 p-4 bg-success-500/10 border border-success-500/30 text-success-400 text-sm rounded-xl text-center">
        {{ successMessage }}
      </div>

      <!-- Login / Signup toggle -->
      <div v-if="mode !== 'verify'" class="flex mb-6 bg-surface-900 rounded-xl p-1 border border-surface-700">
        <button
          type="button"
          class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all"
          :class="mode === 'login' ? 'bg-gold-500 text-surface-950' : 'text-surface-400 hover:text-surface-200'"
          @click="switchMode('login')"
        >
          Login
        </button>
        <button
          type="button"
          class="flex-1 py-2.5 rounded-lg text-sm font-semibold transition-all"
          :class="mode === 'signup' ? 'bg-gold-500 text-surface-950' : 'text-surface-400 hover:text-surface-200'"
          @click="switchMode('signup')"
        >
          Sign Up
        </button>
      </div>

      <!-- Login / Signup form -->
      <form v-if="mode !== 'verify'" @submit.prevent="handleSubmit" class="space-y-5">
        <div v-if="mode === 'signup'">
          <label class="text-sm font-medium text-surface-300">Full Name</label>
          <input
            v-model="name" type="text" required autocomplete="name"
            class="w-full mt-1.5 px-4 py-3 border border-surface-700 rounded-xl focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 outline-none bg-surface-900 text-surface-100 transition-all placeholder-surface-600"
            placeholder="Enter your name"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-surface-300">Email</label>
          <input
            v-model="email" type="email" required autocomplete="email"
            class="w-full mt-1.5 px-4 py-3 border border-surface-700 rounded-xl focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 outline-none bg-surface-900 text-surface-100 transition-all placeholder-surface-600"
            placeholder="Enter your email"
          />
        </div>

        <div v-if="mode === 'signup'">
          <label class="text-sm font-medium text-surface-300">Mobile Number</label>
          <input
            v-model="phone" type="tel" autocomplete="tel"
            class="w-full mt-1.5 px-4 py-3 border border-surface-700 rounded-xl focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 outline-none bg-surface-900 text-surface-100 transition-all placeholder-surface-600"
            placeholder="e.g. +961 71 234 567"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-surface-300">Password</label>
          <input
            v-model="password" type="password" required
            :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
            class="w-full mt-1.5 px-4 py-3 border border-surface-700 rounded-xl focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 outline-none bg-surface-900 text-surface-100 transition-all placeholder-surface-600"
            placeholder="••••••••"
          />
        </div>

        <p v-if="error" class="text-sm text-danger-400">{{ error }}</p>

        <button
          type="submit" :disabled="loading"
          class="w-full bg-gold-500 text-surface-950 py-3 rounded-xl font-display font-semibold hover:bg-gold-400 transition-all disabled:opacity-60 active:scale-[0.98] shadow-glow-gold"
        >
          {{ loading ? "Please wait..." : mode === "login" ? "Login" : "Sign Up" }}
        </button>
      </form>

      <!-- Verification form -->
      <form v-else @submit.prevent="handleVerify" class="space-y-5">
        <p class="text-xs text-surface-400 text-center">
          We sent a 4-digit verification code to <br><strong class="text-surface-200">{{ email }}</strong>
        </p>

        <div>
          <label class="text-sm font-medium text-surface-300 block text-center">Verification Code</label>
          <input
            v-model="verificationCode"
            type="text" inputmode="numeric" pattern="[0-9]*" maxlength="4" required placeholder="0000"
            class="w-full max-w-[160px] mx-auto block mt-2 px-4 py-3 border border-surface-700 rounded-xl text-center text-2xl tracking-[0.5em] font-bold focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 outline-none bg-surface-900 text-surface-100 transition-all"
          />
        </div>

        <p v-if="error" class="text-sm text-danger-400 text-center">{{ error }}</p>

        <button
          type="submit" :disabled="loading || verificationCode.length !== 4"
          class="w-full bg-gold-500 text-surface-950 py-3 rounded-xl font-display font-semibold hover:bg-gold-400 transition-all disabled:opacity-60 active:scale-[0.98] shadow-glow-gold"
        >
          {{ loading ? "Verifying..." : "Verify & Log In" }}
        </button>

        <button
          type="button" @click="handleResendCode" :disabled="resending"
          class="w-full text-xs text-center text-gold-500 hover:text-gold-400 hover:underline block pt-2 disabled:opacity-60"
        >
          {{ resending ? "Sending..." : "Resend Code" }}
        </button>

        <button
          type="button" @click="switchMode('login')"
          class="w-full text-xs text-center text-surface-500 hover:text-surface-300 hover:underline block pt-2"
        >
          Back to Login
        </button>
      </form>

      <p class="text-xs text-center text-surface-600 mt-6">By continuing, you agree to our Terms of Service</p>
    </div>
  </div>
</template>
