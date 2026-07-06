<script setup>
import { ref, onMounted } from 'vue'

const orders = ref([])
const loading = ref(true)

onMounted(fetchOrders)

async function fetchOrders() {
  loading.value = true
  try {
    const data = await request('GET', '/api/admin/orders/')
    orders.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('Failed to load orders', e)
    orders.value = []
  } finally {
    loading.value = false
  }
}

async function request(method, path, body) {
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] || ''
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token },
    credentials: 'same-origin',
    body: body ? JSON.stringify(body) : undefined,
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || data.detail || 'Request failed')
  return data
}

async function updateStatus(orderId, status) {
  try {
    await request('PATCH', `/api/admin/orders/${orderId}/status/`, { status })
    orders.value = orders.value.map(o => o.id === orderId ? { ...o, status } : o)
  } catch (e) {
    alert(e.message)
  }
}

const statusOptions = ['placed', 'processing', 'shipped', 'out_for_delivery', 'delivered']

function statusColor(status) {
  const map = {
    placed: 'text-cyan-400 bg-cyan-950/30 border-cyan-800/50',
    processing: 'text-yellow-400 bg-yellow-950/30 border-yellow-800/50',
    shipped: 'text-blue-400 bg-blue-950/30 border-blue-800/50',
    out_for_delivery: 'text-purple-400 bg-purple-950/30 border-purple-800/50',
    delivered: 'text-emerald-400 bg-emerald-950/30 border-emerald-800/50',
  }
  return map[status] || 'text-slate-400 bg-slate-800 border-slate-700'
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-white">Orders</h2>
      <span class="text-sm text-slate-500">{{ orders.length }} total</span>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-slate-500 text-sm mt-3">Loading orders...</p>
    </div>

    <div v-else-if="!orders.length" class="text-center py-12 text-slate-500">
      <p class="text-4xl mb-4">📋</p>
      <p>No orders yet.</p>
    </div>

    <div v-else class="space-y-3">
      <div v-for="order in orders" :key="order.id" class="bg-slate-800/50 border border-slate-700 rounded-xl p-4">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-lg font-mono font-bold text-white">#{{ order.id }}</span>
              <span class="text-xs text-slate-500">{{ new Date(order.created_at).toLocaleDateString() }}</span>
            </div>
            <p class="text-sm text-slate-400 truncate">{{ order.name }} — {{ order.email }}</p>
            <p class="text-xs text-slate-500 truncate">{{ order.address }}</p>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <select
              :value="order.status"
              @change="updateStatus(order.id, $event.target.value)"
              class="text-xs rounded-full px-3 py-1.5 border font-mono font-medium bg-slate-900 cursor-pointer"
              :class="statusColor(order.status)"
            >
              <option v-for="s in statusOptions" :key="s" :value="s">{{ s.replace(/_/g, ' ') }}</option>
            </select>
          </div>
        </div>

        <div v-if="order.items?.length" class="mt-3 pt-3 border-t border-slate-700">
          <div v-for="item in order.items" :key="item.id" class="flex justify-between text-sm text-slate-400 py-0.5">
            <span>{{ item.name }} <span class="text-slate-600">x{{ item.quantity }}</span></span>
            <span class="font-mono">${{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-sm font-bold text-white pt-2 mt-2 border-t border-slate-700">
            <span>Total</span>
            <span class="text-cyan-400 font-mono">${{ order.total?.toFixed(2) || '0.00' }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
