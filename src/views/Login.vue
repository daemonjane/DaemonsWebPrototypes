<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { login, signup, saveAuthSession, verifyEmail, resendVerificationCode } from "../services/login.js"
import { useOsimartCart } from "../composables/useOsimartCart"
import { useWishlistStore } from "../composables/useWishlistStore"

const router = useRouter()
const { setUser: setUserForCart } = useOsimartCart()
const wishlistStore = useWishlistStore()

const mode = ref("login") // "login" | "signup" | "verify"
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
  <div class="body-font bg-secondary flex items-center justify-center min-h-screen">
    <div class="w-full max-w-md bg-card shadow-theme-heavy rounded-3xl p-10 border border-theme">
      <h1 class="heading-font text-4xl font-bold text-center text-[#D4AF37] mb-2">Golden Glow</h1>

      <p class="text-center text-secondary mb-8">
        {{
          mode === "login" ? "Login to your beauty account" :
          mode === "signup" ? "Create your beauty account" :
          "Verify your email address"
        }}
      </p>

      <div v-if="successMessage" class="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 text-sm rounded-xl text-center">
        {{ successMessage }}
      </div>

      <div v-if="mode !== 'verify'" class="flex mb-6 bg-secondary rounded-xl p-1 border border-theme">
        <button
          type="button"
          class="flex-1 py-2 rounded-lg text-sm font-semibold transition"
          :class="mode === 'login' ? 'bg-[#D4AF37] text-white' : 'text-secondary'"
          @click="switchMode('login')"
        >
          Login
        </button>
        <button
          type="button"
          class="flex-1 py-2 rounded-lg text-sm font-semibold transition"
          :class="mode === 'signup' ? 'bg-[#D4AF37] text-white' : 'text-secondary'"
          @click="switchMode('signup')"
        >
          Sign Up
        </button>
      </div>

      <form v-if="mode !== 'verify'" @submit.prevent="handleSubmit" class="space-y-5">
        <div v-if="mode === 'signup'">
          <label class="text-sm font-medium text-secondary">Full Name</label>
          <input
            v-model="name"
            type="text"
            required
            autocomplete="name"
            class="w-full mt-1 px-4 py-3 border border-theme rounded-xl focus:ring-2 focus:ring-[#D4AF37] outline-none bg-input text-primary"
            placeholder="Enter your name"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-secondary">Email</label>
          <input
            v-model="email"
            type="email"
            required
            autocomplete="email"
            class="w-full mt-1 px-4 py-3 border border-theme rounded-xl focus:ring-2 focus:ring-[#D4AF37] outline-none bg-input text-primary"
            placeholder="Enter your email"
          />
        </div>

        <div v-if="mode === 'signup'">
          <label class="text-sm font-medium text-secondary">Mobile Number</label>
          <input
            v-model="phone"
            type="tel"
            autocomplete="tel"
            class="w-full mt-1 px-4 py-3 border border-theme rounded-xl focus:ring-2 focus:ring-[#D4AF37] outline-none bg-input text-primary"
            placeholder="e.g. +961 71 234 567"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-secondary">Password</label>
          <input
            v-model="password"
            type="password"
            required
            :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
            class="w-full mt-1 px-4 py-3 border border-theme rounded-xl focus:ring-2 focus:ring-[#D4AF37] outline-none bg-input text-primary"
            placeholder="••••••••"
          />
        </div>

        <p v-if="error" class="text-sm text-red-500">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-[#D4AF37] text-white py-3 rounded-xl font-semibold hover:bg-[#c39d28] transition disabled:opacity-60"
        >
          {{ loading ? "Please wait..." : mode === "login" ? "Login" : "Sign Up" }}
        </button>
      </form>

      <form v-else @submit.prevent="handleVerify" class="space-y-5">
        <p class="text-xs text-secondary text-center">
          We sent a 4-digit verification code to <br><strong class="text-primary">{{ email }}</strong>
        </p>

        <div>
          <label class="text-sm font-medium text-secondary block text-center">Verification Code</label>
          <input
            v-model="verificationCode"
            type="text"
            inputmode="numeric"
            pattern="[0-9]*"
            maxlength="4"
            required
            placeholder="0000"
            class="w-full max-w-[160px] mx-auto block mt-2 px-4 py-3 border border-theme rounded-xl text-center text-2xl tracking-[0.5em] font-bold focus:ring-2 focus:ring-[#D4AF37] outline-none bg-input text-primary"
          />
        </div>

        <p v-if="error" class="text-sm text-red-500 text-center">{{ error }}</p>

        <button
          type="submit"
          :disabled="loading || verificationCode.length !== 4"
          class="w-full bg-[#D4AF37] text-white py-3 rounded-xl font-semibold hover:bg-[#c39d28] transition disabled:opacity-60"
        >
          {{ loading ? "Verifying..." : "Verify & Log In" }}
        </button>

        <button
          type="button"
          @click="handleResendCode"
          :disabled="resending"
          class="w-full text-xs text-center text-[#D4AF37] hover:underline block pt-2 disabled:opacity-60"
        >
          {{ resending ? "Sending..." : "Resend Code" }}
        </button>

        <button
          type="button"
          @click="switchMode('login')"
          class="w-full text-xs text-center text-secondary hover:underline block pt-2"
        >
          Back to Login
        </button>
      </form>

      <p class="text-xs text-center text-muted mt-6">By continuing, you join Glow Rewards ✨</p>
    </div>
  </div>
</template>

<style scoped>
.heading-font {
  font-family: "Playfair Display", serif;
}
.body-font {
  font-family: "Poppins", sans-serif;
}
</style>
