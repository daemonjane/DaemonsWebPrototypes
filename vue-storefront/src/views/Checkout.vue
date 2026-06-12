<script setup>
import { reactive, computed } from 'vue'
import { useCart } from '../composables/useCart'
import { useRouter } from 'vue-router'
import { validateForm } from '../utils/validation'

const { cart, totalPrice, clearCart } = useCart()
const router = useRouter()

const form = reactive({
  name: '',
  email: '',
  address: ''
})
const errors = reactive({})

const cartSubtotal = computed(() =>
  cart.value
    .filter(item => item.type !== 'upgrade' && item.type !== 'membership')
    .reduce((sum, item) => sum + item.price * item.quantity, 0)
)
const upgradesTotal = computed(() =>
  cart.value.filter(item => item.type === 'upgrade').reduce((sum, item) => sum + item.price, 0)
)
const membershipTotal = computed(() =>
  cart.value.filter(item => item.type === 'membership').reduce((sum, item) => sum + item.price, 0)
)

function placeOrder() {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])

  const validationErrors = validateForm(form, {
    name: ['required'],
    email: ['required', 'email'],
    address: ['required']
  })

  if (Object.keys(validationErrors).length > 0) {
    Object.assign(errors, validationErrors)
    return
  }

  alert('Demo order placed! Cart will be cleared.')
  clearCart()
  router.push('/')
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Checkout</h1>
    <div class="grid md:grid-cols-2 gap-8">
      <!-- Order Summary -->
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
        <ul v-if="cart.length" class="space-y-2">
          <li v-for="item in cart" :key="item.id" class="flex justify-between">
            <span>{{ item.name }} (x{{ item.quantity }})</span>
            <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
          </li>
        </ul>
        <p v-else class="text-slate-400">Your cart is empty.</p>

        <div class="border-t border-slate-700 mt-4 pt-4 space-y-2 text-sm">
          <div class="flex justify-between text-slate-400">
            <span>Subtotal</span>
            <span>${{ cartSubtotal.toFixed(2) }}</span>
          </div>
          <div v-if="upgradesTotal > 0" class="flex justify-between text-slate-400">
            <span>Upgrades</span>
            <span>${{ upgradesTotal.toFixed(2) }}</span>
          </div>
          <div v-if="membershipTotal > 0" class="flex justify-between text-slate-400">
            <span>Membership</span>
            <span>${{ membershipTotal.toFixed(2) }}</span>
          </div>
        </div>

        <div class="border-t border-slate-700 mt-4 pt-4 text-right">
          <span class="text-lg">Total: </span>
          <span class="text-2xl font-bold text-cyan-400">${{ totalPrice.toFixed(2) }}</span>
        </div>

        <button
          @click="placeOrder"
          class="mt-6 w-full bg-cyan-600 py-3 rounded-md font-bold hover:bg-cyan-500 transition"
        >
          Place Order (Demo)
        </button>
      </div>

      <!-- Shipping Form -->
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Shipping Info</h2>
        <form @submit.prevent="placeOrder" novalidate>
          <div class="mb-3">
            <input
              v-model="form.name"
              type="text"
              placeholder="Full Name"
              class="w-full bg-slate-800 border border-slate-700 rounded p-2"
              :class="{ 'border-pink-500': errors.name }"
              :aria-describedby="errors.name ? 'name-error' : undefined"
              aria-required="true"
            >
            <p v-if="errors.name" id="name-error" class="text-pink-400 text-xs mt-1" role="alert">
              {{ errors.name }}
            </p>
          </div>

          <div class="mb-3">
            <input
              v-model="form.email"
              type="email"
              placeholder="Email"
              class="w-full bg-slate-800 border border-slate-700 rounded p-2"
              :class="{ 'border-pink-500': errors.email }"
              :aria-describedby="errors.email ? 'email-error' : undefined"
              aria-required="true"
            >
            <p v-if="errors.email" id="email-error" class="text-pink-400 text-xs mt-1" role="alert">
              {{ errors.email }}
            </p>
          </div>

          <div class="mb-3">
            <input
              v-model="form.address"
              type="text"
              placeholder="Address"
              class="w-full bg-slate-800 border border-slate-700 rounded p-2"
              :class="{ 'border-pink-500': errors.address }"
              :aria-describedby="errors.address ? 'address-error' : undefined"
              aria-required="true"
            >
            <p v-if="errors.address" id="address-error" class="text-pink-400 text-xs mt-1" role="alert">
              {{ errors.address }}
            </p>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>