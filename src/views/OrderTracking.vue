<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const route = useRoute()
const router = useRouter()
const orderId = ref('')
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const tracking = ref(null)

onMounted(() => {
  if (route.query.order) {
    orderId.value = route.query.order
    fetchTracking()
  }
})

async function fetchTracking() {
  const id = orderId.value.trim()
  if (!id) { searched.value = true; return }
  loading.value = true
  error.value = ''
  searched.value = true
  try {
    const { api } = await import('../utils/api')
    tracking.value = await api.orders.tracking(id)
  } catch (e) {
    error.value = e.message || 'Failed to load tracking info'
    tracking.value = null
  } finally {
    loading.value = false
  }
}

function formatDate(iso) {
  if (!iso) return 'Pending'
  const d = new Date(iso)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) +
    ' — ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

function isPast(index, history) {
  const now = new Date()
  return new Date(history[index].timestamp) < now
}

function currentIndex(history) {
  const now = new Date()
  return history.findIndex(h => new Date(h.timestamp) >= now)
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Order Tracking' }]" />
    <h1 class="text-3xl font-bold text-white mb-2">Order Tracking</h1>
    <p class="text-slate-400 mb-8 text-sm">Enter your order number to view the current status and delivery timeline.</p>

    <div class="flex gap-2 mb-10">
      <input
        v-model="orderId"
        type="text"
        placeholder="e.g. 42"
        class="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 font-mono"
        @keyup.enter="fetchTracking"
      >
      <button
        @click="fetchTracking"
        class="bg-cyan-600 hover:bg-cyan-500 text-white font-semibold px-6 py-3 rounded-lg transition active:scale-95"
      >
        Track
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto"></div>
      <p class="text-slate-400 text-sm mt-3">Loading tracking...</p>
    </div>

    <div v-else-if="error" class="bg-pink-950/30 border border-pink-700/50 rounded-xl p-6 text-center">
      <p class="text-pink-300">{{ error }}</p>
    </div>

    <div v-else-if="searched && tracking && !tracking.tracking_number" class="bg-slate-900 rounded-xl border border-slate-800 p-6 text-center">
      <p class="text-slate-500">No tracking information available for this order yet.</p>
    </div>

    <div v-else-if="tracking && tracking.tracking_number" class="bg-slate-900 rounded-xl border border-slate-800 p-6 sm:p-8">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="text-xs text-slate-500 font-mono uppercase tracking-wider">Order #{{ tracking.order_id }}</p>
          <p class="text-white font-mono font-bold text-lg mt-1">{{ tracking.carrier }} {{ tracking.tracking_number }}</p>
          <p v-if="tracking.estimated_delivery" class="text-xs text-slate-500 mt-1">
            Est. delivery: {{ formatDate(tracking.estimated_delivery) }}
          </p>
        </div>
        <span class="bg-cyan-950/30 text-cyan-400 text-xs font-mono px-3 py-1.5 rounded-full border border-cyan-800/50">
          {{ tracking.current_status }}
        </span>
      </div>

      <div v-if="tracking.tracking_url" class="mb-6">
        <a :href="tracking.tracking_url" target="_blank"
           class="text-xs text-cyan-400 hover:text-cyan-300 underline underline-offset-2">
          View on carrier's website &rarr;
        </a>
      </div>

      <div class="relative" v-if="tracking.history && tracking.history.length">
        <div v-for="(step, i) in tracking.history" :key="i" class="flex gap-4 pb-8 last:pb-0 relative">
          <div class="flex flex-col items-center">
            <div
              class="w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 z-10"
              :class="isPast(i, tracking.history)
                ? 'bg-emerald-600 border-emerald-600'
                : i === currentIndex(tracking.history)
                  ? 'bg-slate-900 border-cyan-500'
                  : 'bg-slate-900 border-slate-700'"
            >
              <svg v-if="isPast(i, tracking.history)" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
              </svg>
              <div v-else-if="i === currentIndex(tracking.history)" class="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></div>
            </div>
            <div v-if="i < tracking.history.length - 1" class="w-0.5 flex-1 mt-1"
              :class="isPast(i, tracking.history) ? 'bg-emerald-600' : 'bg-slate-800'"></div>
          </div>
          <div class="pt-0.5">
            <p class="text-white font-medium text-sm"
               :class="{ 'text-slate-500': !isPast(i, tracking.history) && i !== currentIndex(tracking.history) }">
              {{ step.status }}
            </p>
            <p class="text-xs text-slate-500 mt-0.5 font-mono">{{ formatDate(step.timestamp) }}</p>
            <p v-if="step.location" class="text-xs text-slate-600 mt-0.5">{{ step.location }}</p>
            <p v-if="step.note" class="text-xs text-slate-600 mt-0.5">{{ step.note }}</p>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-6 text-slate-500 text-sm">
        No tracking history yet.
      </div>
    </div>

    <div v-else-if="searched && !tracking" class="text-center py-12">
      <p class="text-slate-500">Enter an order number to track.</p>
    </div>
  </div>
</template>
