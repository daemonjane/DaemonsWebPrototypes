<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const orderNumber = Math.floor(100000 + Math.random() * 900000)
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-16 text-center">
    <div class="w-20 h-20 bg-emerald-600/20 rounded-full flex items-center justify-center mx-auto mb-6">
      <svg class="w-10 h-10 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
      </svg>
    </div>
    <h1 class="text-3xl font-bold text-white mb-2">Order Confirmed!</h1>
    <p class="text-slate-400 mb-6">Thank you for your purchase. Your order is being processed.</p>
    <div class="bg-slate-800 border border-slate-700 rounded-xl p-6 inline-block mb-8">
      <p class="text-sm text-slate-500 mb-1">Order Number</p>
      <p class="text-2xl font-mono font-bold text-cyan-400">#{{ orderNumber }}</p>
    </div>
    <div class="space-y-3">
      <router-link to="/tracking" class="block w-full sm:w-auto sm:inline-block bg-cyan-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-cyan-500 transition-all">
        Track Order
      </router-link>
      <router-link to="/shop" class="block w-full sm:w-auto sm:inline-block border border-slate-600 text-slate-300 px-8 py-3 rounded-lg font-semibold hover:border-cyan-500 hover:text-cyan-400 transition-all sm:ml-3">
        Continue Shopping
      </router-link>
    </div>
  </div>
</template>
