<script setup>
import { ref } from 'vue'

const orderId = ref('')
const searched = ref(false)

const timeline = [
  { status: 'Order Placed', date: 'Jun 14, 2026 — 09:23', done: true },
  { status: 'Processing', date: 'Jun 14, 2026 — 14:17', done: true },
  { status: 'Shipped', date: 'Jun 15, 2026 — 08:45', done: false },
  { status: 'Out for Delivery', date: 'Expected Jun 17', done: false },
  { status: 'Delivered', date: 'Pending', done: false },
]

function track() {
  searched.value = true
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-white mb-2">Order Tracking</h1>
    <p class="text-slate-400 mb-8 text-sm">Enter your order ID to view the current status and delivery timeline.</p>

    <!-- Search -->
    <div class="flex gap-2 mb-10">
      <input
        v-model="orderId"
        type="text"
        placeholder="e.g. TS-2026-0X7A"
        class="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 font-mono"
        @keyup.enter="track"
      >
      <button
        @click="track"
        class="bg-cyan-600 hover:bg-cyan-500 text-white font-semibold px-6 py-3 rounded-lg transition active:scale-95"
      >
        Track
      </button>
    </div>

    <!-- Result -->
    <div v-if="searched && orderId.trim()" class="bg-slate-900 rounded-xl border border-slate-800 p-6 sm:p-8">
      <div class="flex items-center justify-between mb-6">
        <div>
          <p class="text-xs text-slate-500 font-mono uppercase tracking-wider">Order ID</p>
          <p class="text-white font-mono font-bold text-lg">{{ orderId.toUpperCase() }}</p>
        </div>
        <span class="bg-cyan-950/30 text-cyan-400 text-xs font-mono px-3 py-1.5 rounded-full border border-cyan-800/50">
          In Transit
        </span>
      </div>

      <!-- Timeline -->
      <div class="relative">
        <div v-for="(step, i) in timeline" :key="i" class="flex gap-4 pb-8 last:pb-0 relative">
          <div class="flex flex-col items-center">
            <div
              class="w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0 z-10"
              :class="step.done
                ? 'bg-emerald-600 border-emerald-600'
                : i === timeline.findIndex(s => !s.done)
                  ? 'bg-slate-900 border-cyan-500'
                  : 'bg-slate-900 border-slate-700'"
            >
              <svg v-if="step.done" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
              </svg>
              <div v-else-if="i === timeline.findIndex(s => !s.done)" class="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></div>
            </div>
            <div v-if="i < timeline.length - 1" class="w-0.5 flex-1 mt-1"
              :class="step.done ? 'bg-emerald-600' : 'bg-slate-800'"></div>
          </div>
          <div class="pt-0.5">
            <p class="text-white font-medium text-sm" :class="{ 'text-slate-500': !step.done && i !== timeline.findIndex(s => !s.done) }">
              {{ step.status }}
            </p>
            <p class="text-xs text-slate-500 mt-0.5 font-mono">{{ step.date }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- No order searched -->
    <div v-else-if="searched && !orderId.trim()" class="text-center py-12">
      <p class="text-slate-500">Please enter an order ID to track.</p>
    </div>

    <!-- Examples -->
    <div class="mt-10 text-center">
      <p class="text-xs text-slate-600 mb-2">Try a demo ID:</p>
      <button @click="orderId = 'TS-2026-0X7A'; track()" class="text-xs text-cyan-500 hover:text-cyan-400 font-mono underline underline-offset-2 mx-2">
        TS-2026-0X7A
      </button>
      <button @click="orderId = 'TS-2026-1B3C'; track()" class="text-xs text-cyan-500 hover:text-cyan-400 font-mono underline underline-offset-2 mx-2">
        TS-2026-1B3C
      </button>
    </div>
  </div>
</template>
