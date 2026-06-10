<script setup>
import { computed } from 'vue'
import { useCart } from '../composables/useCart'
import { useRouter } from 'vue-router'

const { cart, totalPrice, clearCart } = useCart()
const router = useRouter()

function placeOrder() {
  alert('Demo order placed! Cart will be cleared.')
  clearCart()
  router.push('/')
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Checkout</h1>
    <div class="grid md:grid-cols-2 gap-8">
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
        <ul v-if="cart.length" class="space-y-2">
          <li v-for="item in cart" :key="item.id" class="flex justify-between">
            <span>{{ item.name }} (x{{ item.quantity }})</span>
            <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
          </li>
        </ul>
        <p v-else class="text-slate-400">Your cart is empty.</p>
        <div class="border-t border-slate-700 mt-4 pt-4 text-right">
          <span class="text-lg">Total: </span>
          <span class="text-2xl font-bold text-cyan-400">${{ totalPrice.toFixed(2) }}</span>
        </div>
        <button @click="placeOrder" class="mt-6 w-full bg-cyan-600 py-3 rounded-md font-bold hover:bg-cyan-500 transition">Place Order (Demo)</button>
      </div>
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold mb-4">Shipping Info</h2>
        <form @submit.prevent>
          <input type="text" placeholder="Full Name" class="w-full bg-slate-800 border border-slate-700 rounded p-2 mb-3">
          <input type="email" placeholder="Email" class="w-full bg-slate-800 border border-slate-700 rounded p-2 mb-3">
          <input type="text" placeholder="Address" class="w-full bg-slate-800 border border-slate-700 rounded p-2 mb-3">
        </form>
      </div>
    </div>
  </div>
</template>