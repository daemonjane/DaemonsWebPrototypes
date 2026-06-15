<script setup>
import { ref, computed } from 'vue'
import { products } from '../data/products'
import ProductCard from '../components/ProductCard.vue'

const currentFilter = ref('all')
const currentSort = ref('default')
const searchQuery = ref('')

const filteredProducts = computed(() => {
  let list = products.filter(p => {
    if (currentFilter.value !== 'all' && p.category !== currentFilter.value) return false
    if (searchQuery.value && !p.name.toLowerCase().includes(searchQuery.value.toLowerCase())) return false
    return true
  })
  if (currentSort.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (currentSort.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  else if (currentSort.value === 'name-asc') list.sort((a, b) => a.name.localeCompare(b.name))
  return list
})
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-white mb-2">All Hardware</h1>
    <p class="text-slate-400 mb-6">High‑performance components, pre‑built systems, and peripherals.</p>

    <!-- Filter / search / sort -->
    <div class="flex flex-wrap gap-4 mb-8 items-center justify-between">
      <div class="flex gap-2 flex-wrap">
        <button @click="currentFilter = 'all'" :class="['filter-btn px-4 py-1 rounded-full text-sm', currentFilter === 'all' ? 'bg-cyan-600 text-white' : 'bg-slate-800 hover:bg-cyan-700']">All</button>
        <button @click="currentFilter = 'desktop'" :class="['filter-btn px-4 py-1 rounded-full text-sm', currentFilter === 'desktop' ? 'bg-cyan-600 text-white' : 'bg-slate-800 hover:bg-cyan-700']">Desktops</button>
        <button @click="currentFilter = 'monitors'" :class="['filter-btn px-4 py-1 rounded-full text-sm', currentFilter === 'monitors' ? 'bg-cyan-600 text-white' : 'bg-slate-800 hover:bg-cyan-700']">Monitors</button>
        <button @click="currentFilter = 'peripherals'" :class="['filter-btn px-4 py-1 rounded-full text-sm', currentFilter === 'peripherals' ? 'bg-cyan-600 text-white' : 'bg-slate-800 hover:bg-cyan-700']">Peripherals</button>
      </div>
      <div class="flex gap-2">
        <input v-model="searchQuery" type="text" placeholder="Search by name..." class="bg-slate-800 border border-slate-700 rounded-md px-3 py-1 text-sm focus:ring-2 focus:ring-cyan-400">
        <select v-model="currentSort" class="bg-slate-800 border border-slate-700 rounded px-3 py-1 text-sm">
          <option value="default">Sort by</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="name-asc">Name: A-Z</option>
        </select>
      </div>
    </div>

    <!-- Products grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" :show-full="true" />
    </div>
  </div>
</template>