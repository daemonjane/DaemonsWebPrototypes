<script setup>
import { ref, computed } from 'vue'
import { products } from '../data/products'
import ProductCard from '../components/ProductCard.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import EmptyState from '../components/EmptyState.vue'

const categoryMeta = {
  all: { label: 'All Products', icon: '🔧', desc: 'Every component in our catalogue.' },
  desktop: { label: 'Desktops', icon: '🖥️', desc: 'Custom-configured performance towers.' },
  monitors: { label: 'Monitors', icon: '🖥️', desc: 'High-refresh QD-OLED and IPS panels.' },
  peripherals: { label: 'Peripherals', icon: '⌨️', desc: 'Keyboards, mice, audio, and accessories.' },
}

const currentFilter = ref('all')
const currentSort = ref('default')
const searchQuery = ref('')
const priceMin = ref(0)
const priceMax = ref(3000)
const showFilters = ref(false)

const maxPrice = computed(() => Math.max(...products.map(p => p.price)))

const filteredProducts = computed(() => {
  let list = products.filter(p => {
    if (currentFilter.value !== 'all' && p.category !== currentFilter.value) return false
    if (searchQuery.value && !p.name.toLowerCase().includes(searchQuery.value.toLowerCase())) return false
    if (p.price < priceMin.value || p.price > priceMax.value) return false
    return true
  })
  if (currentSort.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (currentSort.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  else if (currentSort.value === 'name-asc') list.sort((a, b) => a.name.localeCompare(b.name))
  return list
})

function resetFilters() {
  currentFilter.value = 'all'
  currentSort.value = 'default'
  searchQuery.value = ''
  priceMin.value = 0
  priceMax.value = maxPrice.value
}
</script>

<template>
  <div>
    <Breadcrumbs :crumbs="[{ label: 'Shop' }]" />

    <!-- Category hero banner -->
    <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl border border-slate-800 p-6 sm:p-8 mb-8 flex items-center gap-5 sm:gap-6">
      <span class="text-4xl sm:text-5xl">{{ categoryMeta[currentFilter]?.icon || '🔧' }}</span>
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-white">{{ categoryMeta[currentFilter]?.label || 'All Products' }}</h1>
        <p class="text-slate-400 mt-1 text-sm">{{ categoryMeta[currentFilter]?.desc }}</p>
        <p class="text-xs text-slate-500 mt-1 font-mono">{{ filteredProducts.length }} of {{ products.length }} products</p>
      </div>
    </div>

    <div class="flex flex-wrap items-end justify-between gap-4 mb-6">
      <router-link to="/counter" class="text-xs text-slate-500 hover:text-cyan-400 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-slate-800 hover:border-slate-700">
        <span>🔢</span> Counter
      </router-link>
      <button
        @click="showFilters = !showFilters"
        class="text-xs text-slate-500 hover:text-cyan-400 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-slate-800 hover:border-slate-700"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
        </svg>
        Filters
      </button>
    </div>

    <!-- Filter / search / sort -->
    <div class="flex flex-wrap gap-4 mb-6 items-center justify-between">
      <div class="flex gap-2 flex-wrap">
        <button @click="currentFilter = 'all'" :class="['filter-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all flex items-center gap-1.5', currentFilter === 'all' ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white']">
          <span>{{ categoryMeta.all.icon }}</span> All
          <span class="ml-0.5 text-[10px] opacity-60">({{ products.length }})</span>
        </button>
        <button @click="currentFilter = 'desktop'" :class="['filter-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all flex items-center gap-1.5', currentFilter === 'desktop' ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white']">
          <span>{{ categoryMeta.desktop.icon }}</span> Desktops
          <span class="ml-0.5 text-[10px] opacity-60">({{ products.filter(p => p.category === 'desktop').length }})</span>
        </button>
        <button @click="currentFilter = 'monitors'" :class="['filter-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all flex items-center gap-1.5', currentFilter === 'monitors' ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white']">
          <span>{{ categoryMeta.monitors.icon }}</span> Monitors
          <span class="ml-0.5 text-[10px] opacity-60">({{ products.filter(p => p.category === 'monitors').length }})</span>
        </button>
        <button @click="currentFilter = 'peripherals'" :class="['filter-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all flex items-center gap-1.5', currentFilter === 'peripherals' ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white']">
          <span>{{ categoryMeta.peripherals.icon }}</span> Peripherals
          <span class="ml-0.5 text-[10px] opacity-60">({{ products.filter(p => p.category === 'peripherals').length }})</span>
        </button>
      </div>
      <div class="flex gap-2">
        <input v-model="searchQuery" type="text" placeholder="Search by name..." class="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400 focus:outline-none w-36 sm:w-auto">
        <select v-model="currentSort" class="bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400 focus:outline-none">
          <option value="default">Sort by</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="name-asc">Name: A-Z</option>
        </select>
      </div>
    </div>

    <!-- Price range filter (collapsible) -->
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-48"
      leave-from-class="opacity-100 max-h-48"
      leave-to-class="opacity-0 max-h-0"
    >
      <div v-if="showFilters" class="mb-6 bg-slate-900 rounded-xl border border-slate-800 p-4">
        <div class="flex flex-wrap items-center gap-6">
          <div class="flex-1 min-w-[200px]">
            <label class="text-xs text-slate-500 font-medium mb-2 block">Price range</label>
            <div class="flex items-center gap-3">
              <span class="text-xs text-slate-400 font-mono w-16">${{ priceMin }}</span>
              <input
                type="range"
                :min="0"
                :max="maxPrice"
                step="10"
                v-model.number="priceMin"
                class="flex-1 h-1.5 bg-slate-700 rounded-full appearance-none cursor-pointer accent-cyan-500"
                aria-label="Minimum price"
              />
            </div>
            <div class="flex items-center gap-3 mt-2">
              <span class="text-xs text-slate-400 font-mono w-16">${{ priceMax }}</span>
              <input
                type="range"
                :min="0"
                :max="maxPrice"
                step="10"
                v-model.number="priceMax"
                class="flex-1 h-1.5 bg-slate-700 rounded-full appearance-none cursor-pointer accent-cyan-500"
                aria-label="Maximum price"
              />
            </div>
          </div>
          <div class="text-center">
            <div class="text-lg font-bold text-cyan-400 font-mono">${{ priceMin }} – ${{ priceMax }}</div>
            <button
              @click="resetFilters"
              class="mt-1 text-[10px] text-slate-600 hover:text-slate-400 transition-colors underline"
            >Reset filters</button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Products grid -->
    <div v-if="filteredProducts.length > 0" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
      <ProductCard v-for="product in filteredProducts" :key="product.id" :product="product" :show-full="true" v-memo="[product.id, product.price, product.rating, filteredProducts.length]" />
    </div>
    <EmptyState v-else icon="search" title="No products found" message="Try adjusting your search or filters." action-label="Clear Filters" @action="resetFilters" />
  </div>
</template>
