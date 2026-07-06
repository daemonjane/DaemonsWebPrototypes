<script setup>
import { ref, onMounted } from 'vue'
import { useFavorites } from '../composables/useFavorites'
import ProductCard from '../components/ProductCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { normalizeProduct, pick } from '../utils/product'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const { ids, count, clear } = useFavorites()

const items = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { api } = await import('../utils/api')
    const res = await api.osimart.products({ limit: 100 })
    const all = pick(res)
    items.value = ids.value
      .map(slug => {
        const match = all.find(p => (p.slugified_name || p.id) === slug)
        return match ? normalizeProduct(match) : null
      })
      .filter(Boolean)
  } catch {
    items.value = []
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <Breadcrumbs :crumbs="[{ label: 'Favorites' }]" />
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-white">Favorites</h1>
        <p class="text-slate-400 mt-1" aria-live="polite">{{ count }} saved {{ count === 1 ? 'item' : 'items' }}</p>
      </div>
      <button
        v-if="count > 0"
        @click="clear"
        class="text-sm text-slate-500 hover:text-pink-400 transition-colors px-3 py-1.5 rounded-md border border-slate-800 hover:border-pink-900/50"
        aria-label="Clear all favorites"
      >
        Clear all
      </button>
    </div>

    <div v-if="!loading && items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard v-for="product in items" :key="product.id" :product="product" />
    </div>

    <div v-else-if="!loading && items.length === 0">
      <EmptyState icon="heart" title="No favorites yet" message="Click the heart icon on any product to save it here." action-label="Browse Products" action-to="/shop" />
    </div>

    <div v-else class="text-center py-12">
      <p class="text-slate-400">Loading favorites...</p>
    </div>
  </div>
</template>
