<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import EmptyState from '../components/EmptyState.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import { normalizeProduct, pick } from '../utils/product'

const route = useRoute()

const products = ref([])
const categories = ref([])
const loading = ref(true)
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = 12

async function loadProducts(page = 1) {
  loading.value = true
  try {
    const { api } = await import('../utils/api')
    const prodRes = await api.osimart.products({ limit: pageSize, page })
    const items = pick(prodRes)
    products.value = items.map(normalizeProduct).filter(p => p.price > 0)
    totalCount.value = prodRes.count || 0
    currentPage.value = page
  } catch (e) {
    console.error('Failed to load products', e)
  } finally {
    loading.value = false
  }
}

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

const paginatedPages = computed(() => {
  const total = totalPages.value
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const pages = []
  const cur = currentPage.value
  if (cur <= 4) {
    for (let i = 1; i <= Math.min(5, total); i++) pages.push(i)
    pages.push('...', total)
  } else if (cur >= total - 3) {
    pages.push(1, '...')
    for (let i = total - 4; i <= total; i++) pages.push(i)
  } else {
    pages.push(1, '...')
    for (let i = cur - 1; i <= cur + 1; i++) pages.push(i)
    pages.push('...', total)
  }
  return pages
})

function goToPage(page) {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  loadProducts(page)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  try {
    const { api } = await import('../utils/api')
    const catRes = await api.osimart.categories()
    categories.value = Array.isArray(catRes) ? catRes : (catRes.results || [])
    await loadProducts(1)
    if (route.query.category) currentFilter.value = route.query.category
    if (route.query.brand) currentBrand.value = route.query.brand
    if (route.query.collection) currentCollection.value = route.query.collection
    if (route.query.q) searchQuery.value = route.query.q
  } catch (e) {
    console.error('Failed to load Osimart data', e)
  } finally {
    loading.value = false
  }
})

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
      <div class="bg-gradient-to-br from-surface-850 to-surface-900 rounded-2xl border border-surface-700 p-6 sm:p-8 mb-8 flex items-center gap-5 sm:gap-6">
        <span class="text-4xl sm:text-5xl">{{ categoryMeta[currentFilter]?.icon || '🔧' }}</span>
        <div>
          <h1 class="text-2xl sm:text-3xl font-display font-bold text-surface-50">{{ categoryMeta[currentFilter]?.label || 'All Products' }}</h1>
          <p class="text-surface-400 mt-1 text-sm">{{ categoryMeta[currentFilter]?.desc }}</p>
          <p class="text-xs text-surface-500 mt-1 font-mono" aria-live="polite">{{ filteredProducts.length }} of {{ totalCount }} products</p>
        </div>
      </div>

      <div class="flex flex-wrap items-end justify-between gap-4 mb-6">
        <button
          @click="showFilters = !showFilters"
          class="text-xs text-surface-400 hover:text-gold-500 transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-surface-700 hover:border-surface-600"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"/>
          </svg>
          Filters
        </button>
      </div>

      <!-- Category filters -->
      <div class="flex flex-wrap gap-2 mb-6">
        <button
          v-for="[slug, meta] of Object.entries(categoryMeta)"
          :key="slug"
          @click="currentFilter = slug"
          :class="['px-4 py-1.5 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5 border', currentFilter === slug ? 'bg-gold-500 text-surface-950 border-gold-500 shadow-glow-gold' : 'bg-surface-800 text-surface-400 border-surface-700 hover:border-surface-600 hover:text-surface-200']"
        >
          <span>{{ meta.icon }}</span> {{ meta.label }}
          <span class="ml-0.5 text-[10px] opacity-60">({{ countInCategory(slug) }})</span>
        </button>
      </div>

      <!-- Search + Sort -->
      <div class="flex flex-wrap gap-3 mb-6 items-center justify-between">
        <input v-model="searchQuery" type="search" placeholder="Search by name..." class="bg-surface-800 border border-surface-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 focus:outline-none w-48 sm:w-auto text-surface-200 placeholder-surface-500" aria-label="Search products by name">
        <select v-model="currentSort" class="bg-surface-800 border border-surface-700 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-gold-500/50 focus:border-gold-500/50 focus:outline-none text-surface-200" aria-label="Sort products">
          <option value="default">Sort by</option>
          <option value="price-asc">Price: Low to High</option>
          <option value="price-desc">Price: High to Low</option>
          <option value="name-asc">Name: A-Z</option>
        </select>
      </div>

      <!-- Price range filter -->
      <transition
        enter-active-class="transition-all duration-200 ease-out"
        leave-active-class="transition-all duration-150 ease-in"
        enter-from-class="opacity-0 max-h-0"
        enter-to-class="opacity-100 max-h-48"
        leave-from-class="opacity-100 max-h-48"
        leave-to-class="opacity-0 max-h-0"
      >
        <div v-if="showFilters" class="mb-6 bg-surface-800/60 rounded-xl border border-surface-700 p-4">
          <div class="flex flex-wrap items-center gap-6">
            <div class="flex-1 min-w-[200px]">
              <label class="text-xs text-surface-500 font-medium mb-2 block">Price range</label>
              <div class="flex items-center gap-3">
                <span class="text-xs text-surface-400 font-mono w-16">${{ priceMin }}</span>
                <input type="range" :min="0" :max="maxPrice" step="10" v-model.number="priceMin"
                  class="flex-1 h-1.5 bg-surface-700 rounded-full appearance-none cursor-pointer accent-gold-500" aria-label="Minimum price" />
              </div>
              <div class="flex items-center gap-3 mt-2">
                <span class="text-xs text-surface-400 font-mono w-16">${{ priceMax }}</span>
                <input type="range" :min="0" :max="maxPrice" step="10" v-model.number="priceMax"
                  class="flex-1 h-1.5 bg-surface-700 rounded-full appearance-none cursor-pointer accent-gold-500" aria-label="Maximum price" />
              </div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-gold-500 font-mono">${{ priceMin }} – ${{ priceMax }}</div>
              <button @click="resetFilters" class="mt-1 text-[10px] text-surface-500 hover:text-surface-300 transition-colors underline">Reset filters</button>
            </div>
          </div>
        </div>
      </transition>

      <!-- Products grid -->
      <div v-if="filteredProducts.length > 0">
        <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          <div v-for="(product, i) in filteredProducts" :key="product.uuid" class="reveal-card" :style="{ animationDelay: i * 0.06 + 's' }">
            <ProductCard :product="product" :show-full="true" />
          </div>
        </div>

        <!-- Pagination -->
        <nav v-if="totalPages > 1" class="mt-10 flex items-center justify-center gap-1.5" aria-label="Product pagination">
          <button @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition disabled:opacity-30 disabled:cursor-not-allowed bg-surface-800 text-surface-400 hover:bg-surface-700 hover:text-surface-200 border border-surface-700">
            Prev
          </button>
          <template v-for="(p, i) in paginatedPages" :key="i">
            <span v-if="p === '...'" class="px-2 text-surface-600 select-none">…</span>
            <button v-else @click="goToPage(p)"
              :class="['px-3 py-1.5 rounded-lg text-sm font-medium transition border', p === currentPage ? 'bg-gold-500 text-surface-950 border-gold-500' : 'bg-surface-800 text-surface-400 border-surface-700 hover:bg-surface-700 hover:text-surface-200']">
              {{ p }}
            </button>
          </template>
          <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages"
            class="px-3 py-1.5 rounded-lg text-sm font-medium transition disabled:opacity-30 disabled:cursor-not-allowed bg-surface-800 text-surface-400 hover:bg-surface-700 hover:text-surface-200 border border-surface-700">
            Next
          </button>
        </nav>
      </div>
      <EmptyState v-else icon="search" title="No products found" message="Try adjusting your search or filters." action-label="Clear Filters" @action="resetFilters" />
    </template>
  </div>
</template>
