<script setup>
import { useRoute, useRouter } from 'vue-router'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const route = useRoute()
const router = useRouter()
const orderNumber = route.query.id || Math.floor(100000 + Math.random() * 900000)
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-16 text-center">
    <div class="text-left mb-6">
      <Breadcrumbs :crumbs="[{ label: 'Order Confirmation' }]" />
    </div>
    <div class="w-20 h-20 bg-success-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
      <svg class="w-10 h-10 text-success-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
      </svg>
    </div>
    <h1 class="text-3xl font-bold text-surface-50 font-display mb-2">Order Confirmed!</h1>
    <p class="text-surface-400 mb-6">Thank you for your purchase. Your order is being processed.</p>
    <div class="bg-surface-800 border border-surface-700 rounded-xl p-6 inline-block mb-8">
      <p class="text-sm text-surface-500 mb-1">Order Number</p>
      <p class="text-2xl font-mono font-bold text-gold-500">#{{ orderNumber }}</p>
    </div>
    <div class="space-y-3">
      <router-link to="/orders" class="block w-full sm:w-auto sm:inline-block bg-gold-500 text-surface-50 px-8 py-3 rounded-lg font-semibold hover:bg-gold-400 transition-all">
        View Orders
      </router-link>
      <router-link to="/shop" class="block w-full sm:w-auto sm:inline-block border border-surface-600 text-surface-200 px-8 py-3 rounded-lg font-semibold hover:border-gold-500 hover:text-gold-500 transition-all sm:ml-3">
        Continue Shopping
      </router-link>
    </div>
  </div>
</template>
