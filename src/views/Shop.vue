<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import EmptyState from '../components/EmptyState.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import { resolveImage } from '../utils/images'
const route = useRoute()

const products = ref([])
const categories = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { api } = await import('../utils/api')
    const [prodRes, catRes] = await Promise.all([
      api.osimart.products({ limit: 50 }),
      api.osimart.categories(),
    ])
    products.value = (prodRes.results || prodRes || []).map(normalizeProduct)
    categories.value = Array.isArray(catRes) ? catRes : (catRes.results || [])
    if (route.query.category) {
      currentFilter.value = route.query.category
    }
    if (route.query.brand) {
      currentBrand.value = route.query.brand
    }
    if (route.query.collection) {
      currentCollection.value = route.query.collection
    }
  } catch (e) {
    console.error('Failed to load Osimart data', e)
  } finally {
    loading.value = false
  }
})

function normalizeProduct(p) {
  return {
    id: p.slugified_name || p.id,
    uuid: p.id,
    name: p.name,
    category: p.categories?.[0]?.category?.slugified_name || 'uncategorized',
    brand: p.brand?.slugified_name || p.brand?.name || null,
    collection: p.collections?.[0]?.slugified_name || p.collections?.[0]?.name || null,
    price: parseFloat(p.price_range || '0'),
    image: resolveImage(p.main_image),
    description: stripHtml(p.description || ''),
    rating: 4.5,
    stock: p.remaining_stock ?? p.stock ?? 0,
    specs: [],
    badge: null,
    badgeColor: null,
  }
}

function stripHtml(html) {
  const d = document.createElement('div')
  d.innerHTML = html
  return d.textContent || d.innerText || ''
}

const currentFilter = ref('all')
const currentBrand = ref(null)
const currentCollection = ref(null)
const currentSort = ref('default')
const searchQuery = ref('')
const priceMin = ref(0)
const priceMax = ref(3000)
const showFilters = ref(false)

const maxPrice = computed(() => Math.max(...products.value.map(p => p.price), 0))

const filteredProducts = computed(() => {
  let list = products.value.filter(p => {
    if (currentFilter.value !== 'all' && p.category !== currentFilter.value) return false
    if (currentBrand.value && p.brand !== currentBrand.value) return false
    if (currentCollection.value && p.collection !== currentCollection.value) return false
    if (searchQuery.value && !p.name.toLowerCase().includes(searchQuery.value.toLowerCase())) return false
    if (p.price < priceMin.value || p.price > priceMax.value) return false
    return true
  })
  if (currentSort.value === 'price-asc') list.sort((a, b) => a.price - b.price)
  else if (currentSort.value === 'price-desc') list.sort((a, b) => b.price - a.price)
  else if (currentSort.value === 'name-asc') list.sort((a, b) => a.name.localeCompare(b.name))
  return list
})

const categoryMeta = computed(() => {
  const meta = { all: { label: 'All Products', icon: '🔧', desc: 'Every product in the catalogue.' } }
  for (const c of categories.value) {
    meta[c.slugified_name] = { label: c.name, icon: c.icon || '📦', desc: '' }
  }
  return meta
})

function resetFilters() {
  currentFilter.value = 'all'
  currentBrand.value = null
  currentCollection.value = null
  currentSort.value = 'default'
  searchQuery.value = ''
  priceMin.value = 0
  priceMax.value = maxPrice.value
}

function countInCategory(catSlug) {
  if (catSlug === 'all') return products.value.length
  return products.value.filter(p => p.category === catSlug).length
}
</script>

<template>
  <div>
    <Breadcrumbs :crumbs="[{ label: 'Shop' }]" />

    <SkeletonLoader v-if="loading" type="list" />

    <template v-else>
      <!-- Category hero banner -->
      <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl border border-slate-800 p-6 sm:p-8 mb-8 flex items-center gap-5 sm:gap-6">
        <span class="text-4xl sm:text-5xl">{{ categoryMeta[currentFilter]?.icon || '🔧' }}</span>
        <div>
          <h1 class="text-2xl sm:text-3xl font-bold text-white">{{ categoryMeta[currentFilter]?.label || 'All Products' }}</h1>
          <p class="text-slate-400 mt-1 text-sm">{{ categoryMeta[currentFilter]?.desc }}</p>
          <p class="text-xs text-slate-500 mt-1 font-mono" aria-live="polite">{{ filteredProducts.length }} of {{ products.length }} products</p>
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
          <button
            v-for="[slug, meta] of Object.entries(categoryMeta)"
            :key="slug"
            @click="currentFilter = slug"
            :class="['filter-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all flex items-center gap-1.5', currentFilter === slug ? 'bg-cyan-600 text-white shadow-sm' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white']"
          >
            <span>{{ meta.icon }}</span> {{ meta.label }}
            <span class="ml-0.5 text-[10px] opacity-60">({{ countInCategory(slug) }})</span>
          </button>
        </div>
        <div class="flex gap-2">
          <input v-model="searchQuery" type="search" placeholder="Search by name..." class="bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400 focus:outline-none w-36 sm:w-auto" aria-label="Search products by name">
          <select v-model="currentSort" class="bg-slate-800 border border-slate-700 rounded px-3 py-1.5 text-sm focus:ring-2 focus:ring-cyan-400 focus:outline-none" aria-label="Sort products">
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
        <ProductCard v-for="product in filteredProducts" :key="product.uuid" :product="product" :show-full="true" />
      </div>
      <EmptyState v-else icon="search" title="No products found" message="Try adjusting your search or filters." action-label="Clear Filters" @action="resetFilters" />
    </template>
  </div>
</template>
