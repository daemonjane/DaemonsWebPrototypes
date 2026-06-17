<script setup>
/**
 * Market Pulse dashboard with live stats and membership CTA.
 * @view
 */
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <div class="text-center mb-10">
      <span class="inline-block bg-cyan-900/40 text-cyan-300 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider mb-4">LIVE DATA STREAM</span>
      <h1 class="text-3xl sm:text-4xl font-bold text-white">Market Pulse</h1>
      <p class="text-slate-400 mt-2 max-w-xl mx-auto">Real-time component pricing, stock levels, and demand forecasts.</p>
    </div>

    <div class="grid sm:grid-cols-3 gap-6">
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-3 hover:border-cyan-800 transition-colors">
        <div class="flex items-center justify-between">
          <span class="text-sm text-slate-500 font-mono uppercase tracking-wider">RTX 5070 Stock</span>
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>
        <div class="text-3xl font-mono font-bold text-cyan-400">142 <span class="text-sm text-cyan-500">▲ +12%</span></div>
        <div class="text-xs text-slate-500">Units available across all warehouses</div>
      </div>
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-3 hover:border-cyan-800 transition-colors">
        <div class="flex items-center justify-between">
          <span class="text-sm text-slate-500 font-mono uppercase tracking-wider">Avg Price Trend</span>
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>
        <div class="text-3xl font-mono font-bold text-emerald-400">$1,249 <span class="text-sm text-emerald-500">▼ -2.4%</span></div>
        <div class="text-xs text-slate-500">30-day moving average across vendors</div>
      </div>
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-3 hover:border-cyan-800 transition-colors">
        <div class="flex items-center justify-between">
          <span class="text-sm text-slate-500 font-mono uppercase tracking-wider">Demand Score</span>
          <span class="w-2 h-2 rounded-full bg-fuchsia-500 animate-pulse"></span>
        </div>
        <div class="text-3xl font-mono font-bold text-fuchsia-400">87/100 <span class="text-sm text-fuchsia-500">HIGH</span></div>
        <div class="text-xs text-slate-500">Based on search volume + order velocity</div>
      </div>
    </div>

    <div class="mt-8 grid sm:grid-cols-2 gap-6">
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
        <h2 class="text-lg font-semibold text-white mb-4">Price History (7d)</h2>
        <div class="h-24 flex items-end gap-2">
          <div v-for="(h, i) in [65, 72, 68, 85, 78, 92, 88]" :key="i" class="flex-1 bg-cyan-500/30 rounded-t hover:bg-cyan-500/50 transition-colors relative group" :style="{ height: h + '%' }">
            <span class="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity">${{ (1249 + (h - 75) * 3).toFixed(0) }}</span>
          </div>
        </div>
        <div class="flex justify-between text-[10px] text-slate-600 mt-2 font-mono">
          <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span>
        </div>
      </div>
      <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 flex flex-col items-center justify-center text-center space-y-4">
        <p class="text-slate-400 text-sm">Unlock historical charts, allocation alerts, and price efficiency tools.</p>
        <button @click="router.push('/login')" class="bg-cyan-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-cyan-500 active:scale-95 transition-all">
          Subscribe to Unlock →
        </button>
      </div>
    </div>
  </div>
</template>
