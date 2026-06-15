<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { products } from '../data/products'
import { useCart } from '../composables/useCart'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'
import { useFavorites } from '../composables/useFavorites'

const route = useRoute()
const productId = route.params.id
const product = computed(() => products.find(p => p.id === productId))

const { addItem } = useCart()
const { visit } = useRecentlyViewed()
const { toggle: toggleFavorite, isFavorite } = useFavorites()

onMounted(() => {
  if (product.value) visit(product.value.id)
})
</script>

<template>
  <div v-if="product" class="max-w-7xl mx-auto px-4 py-12">
    <router-link to="/shop" class="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-cyan-400 mb-6 transition-colors">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
      </svg>
      Back to Shop
    </router-link>
    <div class="grid md:grid-cols-2 gap-8">
      <div class="relative">
        <img :src="product.image" :alt="product.name" class="w-full rounded-xl object-cover h-96" />
        <div class="absolute top-3 right-3">
          <span class="inline-flex items-center gap-1 bg-slate-900/80 text-yellow-400 text-xs px-2 py-1 rounded-md font-mono">
            {{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}
            <span class="text-slate-400 ml-1">{{ product.rating }}</span>
          </span>
        </div>
      </div>
      <div>
        <span class="text-xs font-mono text-cyan-500 uppercase tracking-wider bg-cyan-950/30 px-2 py-1 rounded">{{ product.category }}</span>
        <h1 class="text-3xl sm:text-4xl font-bold text-white mt-2">{{ product.name }}</h1>
        <p class="text-2xl text-cyan-400 mt-4 font-mono">${{ product.price.toFixed(2) }}</p>
        <div class="flex items-center gap-3 mt-2">
          <button
            @click="toggleFavorite(product.id)"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm transition-colors"
            :class="isFavorite(product.id) ? 'bg-pink-950/30 text-pink-400 border border-pink-800/50' : 'bg-slate-800 text-slate-400 border border-slate-700 hover:border-pink-800/50 hover:text-pink-400'"
            :aria-label="isFavorite(product.id) ? 'Remove from favorites' : 'Add to favorites'"
          >
            <svg
              class="w-4 h-4"
              :class="isFavorite(product.id) ? 'fill-pink-400' : ''"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
            {{ isFavorite(product.id) ? 'Favorited' : 'Favorite' }}
          </button>
        </div>
        <p class="text-slate-400 mt-4 leading-relaxed">{{ product.description }}</p>
        <div class="mt-6">
          <h3 class="text-white font-semibold mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Technical Specs
          </h3>
          <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <li v-for="spec in product.specs" :key="spec" class="bg-slate-800/50 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-slate-300 font-mono flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-cyan-500 shrink-0"></span>
              {{ spec }}
            </li>
          </ul>
        </div>
        <button @click="addItem({ id: product.id, name: product.name, price: product.price })" 
                class="mt-8 w-full sm:w-auto bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 px-10 rounded-lg transition-all active:scale-95 flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          Add to Cart
        </button>
      </div>
    </div>
  </div>
  <div v-else class="text-center py-20">
    <p class="text-4xl mb-4">🔍</p>
    <p class="text-slate-400 text-lg">Product not found.</p>
    <router-link to="/shop" class="mt-4 inline-block text-cyan-400 hover:underline">Browse all products</router-link>
  </div>
</template>