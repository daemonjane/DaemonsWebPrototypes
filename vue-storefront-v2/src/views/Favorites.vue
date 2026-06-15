<script setup>
import { useFavorites } from '../composables/useFavorites'
import ProductCard from '../components/ProductCard.vue'

const { items, count, clear } = useFavorites()
</script>

<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
      <div>
        <h1 class="text-3xl font-bold text-white">Favorites</h1>
        <p class="text-slate-400 mt-1">{{ count }} saved {{ count === 1 ? 'item' : 'items' }}</p>
      </div>
      <button
        v-if="count > 0"
        @click="clear"
        class="text-sm text-slate-500 hover:text-pink-400 transition-colors px-3 py-1.5 rounded-md border border-slate-800 hover:border-pink-900/50"
      >
        Clear all
      </button>
    </div>

    <div v-if="items.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <ProductCard v-for="product in items" :key="product.id" :product="product" />
    </div>

    <div v-else class="text-center py-20">
      <p class="text-4xl mb-4">♡</p>
      <p class="text-slate-400 text-lg">No favorites yet</p>
      <p class="text-slate-500 text-sm mt-1">Click the heart icon on any product to save it here.</p>
      <router-link to="/shop" class="mt-6 inline-block bg-cyan-600 text-white px-6 py-2.5 rounded-lg font-semibold hover:bg-cyan-500 transition-colors">
        Browse Products
      </router-link>
    </div>
  </div>
</template>
