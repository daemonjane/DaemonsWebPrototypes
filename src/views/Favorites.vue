<script setup>
import { useFavorites } from '../composables/useFavorites'
import ProductCard from '../components/ProductCard.vue'
import EmptyState from '../components/EmptyState.vue'

const { items, count, clear } = useFavorites()
</script>

<template>
  <div>
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

    <div v-if="items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard v-for="product in items" :key="product.id" :product="product" v-memo="[product.id, product.price, product.rating]" />
    </div>

    <EmptyState v-else icon="heart" title="No favorites yet" message="Click the heart icon on any product to save it here." action-label="Browse Products" action-to="/shop" />
  </div>
</template>
