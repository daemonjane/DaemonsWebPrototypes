<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const orders = ref([])
const loading = ref(true)
const error = ref('')
const router = useRouter()

async function fetchOrders() {
  loading.value = true
  error.value = ''
  try {
    const { api } = await import('../utils/api')
    orders.value = await api.orders.list()
  } catch (e) {
    error.value = e.message || 'Failed to load orders'
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)

function statusColor(status) {
  const map = {
    placed: 'text-cyan-400',
    processing: 'text-yellow-400',
    shipped: 'text-blue-400',
    out_for_delivery: 'text-purple-400',
    delivered: 'text-emerald-400',
  }
  return map[status] || 'text-slate-400'
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Order History</h1>

    <div v-if="loading" class="text-center py-12 text-slate-400">Loading orders...</div>

    <div v-else-if="error" class="bg-pink-950/30 border border-pink-700/50 rounded-xl p-6 text-center">
      <p class="text-pink-300 mb-3">{{ error }}</p>
      <button @click="fetchOrders" class="text-cyan-400 hover:underline text-sm">Try again</button>
    </div>

    <div v-else-if="orders.length === 0" class="text-center py-12 text-slate-500">
      <p class="text-lg mb-2">No orders yet</p>
      <router-link to="/shop" class="text-cyan-400 hover:underline">Start shopping</router-link>
    </div>

    <div v-else class="space-y-4">
      <div v-for="order in orders" :key="order.id" class="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div class="flex items-center justify-between mb-3">
          <div>
            <span class="text-sm text-slate-500">Order</span>
            <span class="text-lg font-mono font-bold text-white ml-2">#{{ order.id }}</span>
          </div>
          <span :class="['text-sm font-medium capitalize', statusColor(order.status)]">
            {{ order.status.replace(/_/g, ' ') }}
          </span>
        </div>
        <div class="text-sm text-slate-400 mb-2">
          Placed on {{ new Date(order.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) }}
        </div>
        <div class="border-t border-slate-800 pt-3 mt-3">
          <ul class="space-y-1 text-sm">
            <li v-for="item in order.items" :key="item.id" class="flex justify-between text-slate-400">
              <span>{{ item.name }} x{{ item.quantity }}</span>
              <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
            </li>
          </ul>
          <div class="flex justify-between mt-3 pt-3 border-t border-slate-800">
            <span class="font-semibold text-white">Total</span>
            <span class="font-bold text-cyan-400">${{ order.total.toFixed(2) }}</span>
          </div>
        </div>
        <div class="text-xs text-slate-500 mt-2">
          Ship to: {{ order.name }} — {{ order.address }}
        </div>
      </div>
    </div>
  </div>
</template>
