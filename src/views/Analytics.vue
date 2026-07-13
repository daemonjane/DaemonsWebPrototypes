<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUser } from '../composables/useUser'

const { user, isStaff, refresh } = useUser()

const storeData = ref(null)
const homeData = ref(null)
const allProducts = ref([])
const allCategories = ref([])
const allBrands = ref([])
const allCollections = ref([])
const pending = ref(true)

onMounted(async () => {
  await refresh()
  try {
    const { api } = await import('../utils/api')
    const [prodRes, catRes, brandRes, collRes, storeRes, homeRes] = await Promise.allSettled([
      api.osimart.products({ limit: 100 }),
      api.osimart.categories(),
      api.osimart.brands(),
      api.osimart.collections(),
      api.osimart.store(),
      api.osimart.home(),
    ])
    if (prodRes.status === 'fulfilled') allProducts.value = prodRes.value?.results || prodRes.value || []
    if (catRes.status === 'fulfilled') allCategories.value = Array.isArray(catRes.value) ? catRes.value : (catRes.value?.results || [])
    if (brandRes.status === 'fulfilled') allBrands.value = Array.isArray(brandRes.value) ? brandRes.value : (brandRes.value?.results || [])
    if (collRes.status === 'fulfilled') allCollections.value = Array.isArray(collRes.value) ? collRes.value : (collRes.value?.results || [])
    if (storeRes.status === 'fulfilled') storeData.value = storeRes.value
    if (homeRes.status === 'fulfilled') homeData.value = homeRes.value
  } catch (e) {
    console.error('Analytics fetch error', e)
  } finally {
    pending.value = false
  }
})

const avgPrice = computed(() => {
  if (!allProducts.value.length) return 0
  const total = allProducts.value.reduce((s, p) => s + parseFloat(p.price_range || 0), 0)
  return (total / allProducts.value.length).toFixed(2)
})

const priceRange = computed(() => {
  const prices = allProducts.value.map(p => parseFloat(p.price_range || 0)).filter(Boolean)
  if (!prices.length) return { min: 0, max: 0 }
  return { min: Math.min(...prices), max: Math.max(...prices) }
})

const categoryBreakdown = computed(() => {
  const map = {}
  for (const p of allProducts.value) {
    const cat = p.categories?.[0]?.category?.name || 'Uncategorized'
    map[cat] = (map[cat] || 0) + 1
  }
  return Object.entries(map).sort((a, b) => b[1] - a[1])
})

const brandedProducts = computed(() => {
  return allProducts.value.filter(p => p.brand?.name).length
})
</script>

<template>
  <div class="space-y-8">
    <div>
      <h1 class="text-2xl sm:text-3xl font-bold text-surface-50 font-display">Store Analytics</h1>
      <p class="text-surface-400 text-sm mt-1">Metrics and insights about your store.</p>
    </div>

    <div v-if="pending" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-electric-500 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-surface-500 text-sm mt-3">Loading analytics...</p>
    </div>

    <template v-else>
      <!-- Store Info -->
      <div v-if="storeData" class="bg-gradient-to-br from-surface-900 to-surface-800 rounded-xl p-6 border border-surface-700">
        <h2 class="text-lg font-semibold text-surface-50 font-display mb-2">{{ storeData.name || 'My Store' }}</h2>
        <p class="text-sm text-surface-400">{{ storeData.description || storeData.tagline || '' }}</p>
        <div v-if="storeData.metrics" class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4">
          <div v-for="(val, key) in storeData.metrics" :key="key" class="bg-surface-800/50 rounded-lg p-3 text-center">
            <p class="text-xs text-surface-500 uppercase tracking-wider">{{ key.replace(/_/g, ' ') }}</p>
            <p class="text-lg font-bold text-electric-500 mt-0.5">{{ val }}</p>
          </div>
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Total Products</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ allProducts.length }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Categories</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ allCategories.length }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Brands</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ allBrands.length }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Collections</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ allCollections.length }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Avg Price</p>
          <p class="text-2xl font-bold text-electric-500 mt-1">${{ avgPrice }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Price Range</p>
          <p class="text-lg font-bold text-surface-50 mt-1">${{ priceRange.min }} – ${{ priceRange.max }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Branded Products</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ brandedProducts }}</p>
        </div>
        <div class="bg-surface-900 rounded-xl p-4 border border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Unbranded</p>
          <p class="text-2xl font-bold text-surface-50 mt-1">{{ allProducts.length - brandedProducts }}</p>
        </div>
      </div>

      <!-- Category Breakdown -->
      <section v-if="categoryBreakdown.length" class="space-y-4">
        <h2 class="text-lg font-semibold text-surface-50 font-display">Products by Category</h2>
        <div class="bg-surface-900 rounded-xl p-5 border border-surface-700 space-y-3">
          <div v-for="[cat, count] in categoryBreakdown" :key="cat" class="flex items-center gap-3">
            <span class="text-sm text-surface-200 w-32 sm:w-40 truncate">{{ cat }}</span>
            <div class="flex-1 h-4 bg-surface-800 rounded-full overflow-hidden">
              <div class="h-full bg-electric-500 rounded-full transition-all duration-500" :style="{ width: (count / allProducts.length * 100) + '%' }"></div>
            </div>
            <span class="text-xs text-surface-500 font-mono w-8 text-right">{{ count }}</span>
          </div>
        </div>
      </section>

      <!-- Brands list -->
      <section v-if="allBrands.length" class="space-y-4">
        <h2 class="text-lg font-semibold text-surface-50 font-display">Brands</h2>
        <div class="flex flex-wrap gap-2">
          <span v-for="b in allBrands" :key="b.id || b.name"
            class="px-3 py-1.5 bg-surface-900 rounded-lg border border-surface-700 text-xs text-surface-200">
            {{ b.name }}
          </span>
        </div>
      </section>

      <!-- Collections list -->
      <section v-if="allCollections.length" class="space-y-4">
        <h2 class="text-lg font-semibold text-surface-50 font-display">Collections</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="c in allCollections" :key="c.id || c.name" class="bg-surface-900 rounded-xl p-4 border border-surface-700">
            <p class="text-sm text-surface-50 font-medium">{{ c.name }}</p>
            <p v-if="c.description" class="text-xs text-surface-500 mt-1">{{ c.description }}</p>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
