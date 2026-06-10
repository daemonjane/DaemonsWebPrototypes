<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-center mb-8">Market Pulse</h1>
    <div class="mt-8 grid md:grid-cols-3 gap-6">
      <div class="bg-slate-900 p-5 rounded-xl">
        <div class="text-cyan-400 text-xl">RTX 5070 Stock</div>
        <div class="text-3xl font-mono font-bold">142 ▲12%</div>
      </div>
      <div class="bg-slate-900 p-5 rounded-xl">
        <div class="text-cyan-400 text-xl">Avg Price Trend</div>
        <div class="text-3xl font-mono font-bold">$1,249 ▼2.4%</div>
      </div>
      <div class="bg-slate-900 p-5 rounded-xl">
        <div class="text-cyan-400 text-xl">Demand Score</div>
        <div class="text-3xl font-mono font-bold">87/100 HIGH</div>
      </div>
    </div>
    <div class="bg-slate-900 mt-8 p-6 rounded-xl text-center">
      <p class="text-slate-300">Real-time allocation alerts, historical charts, and price efficiency tools available to members.</p>
      <button @click="router.push('/login')" class="mt-4 bg-cyan-600 px-6 py-2 rounded-md">Subscribe Now</button>
    </div>
  </div>
</template>