<script setup>
import { ref, computed, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import { normalizeProduct, pick } from '../utils/product'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'

const loading = ref(true)
const products = ref([])
const categories = ref([])
const storeName = ref('')
const { items: recentlyViewed } = useRecentlyViewed()

onMounted(async () => {
  try {
    const { api } = await import('../utils/api')
    const [prodRes, catRes, storeRes] = await Promise.allSettled([
      api.osimart.products({ limit: 50 }),
      api.osimart.categories(),
      api.osimart.store(),
    ])
    if (prodRes.status === 'fulfilled')
      products.value = pick(prodRes.value).map(normalizeProduct)
    if (catRes.status === 'fulfilled')
      categories.value = pick(catRes.value).slice(0, 8)
    if (storeRes.status === 'fulfilled')
      storeName.value = storeRes.value.name || ''
  } catch (e) {
    console.error('Home fetch failed', e)
  } finally {
    loading.value = false
  }
})

const featured = computed(() => products.value.slice(0, 6))
</script>

<template>
  <div>
    <!-- Hero Section -->
    <section class="relative text-center py-16 sm:py-24 overflow-hidden">
      <div class="hero-glow"></div>
      <div class="relative z-10">
        <div class="inline-flex items-center gap-2 bg-gold-500/10 border border-gold-500/20 rounded-full px-4 py-1.5 mb-6">
          <span class="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse"></span>
          <span class="text-xs font-medium text-gold-500 uppercase tracking-wider">High-Tier Hardware</span>
        </div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-surface-50 leading-tight">
          Peak Performance<br>
          <span class="text-gradient-gold">Hardware</span>
        </h1>
        <p class="text-surface-400 max-w-xl mx-auto mt-5 text-lg leading-relaxed">
          Precision-sourced components. Direct vendor supply chains. Custom-tuned systems built for silence and power.
        </p>
        <div class="flex justify-center gap-4 mt-8">
          <router-link to="/shop" class="bg-gold-500 text-surface-950 px-8 py-3 rounded-xl font-display font-semibold hover:bg-gold-400 transition-all active:scale-95 shadow-glow-gold">
            Shop Now
          </router-link>
          <router-link to="/about" class="border border-surface-700 text-surface-200 px-8 py-3 rounded-xl font-display font-semibold hover:border-surface-600 hover:bg-surface-800 transition-all">
            Learn More
          </router-link>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section v-if="categories.length" class="mb-16 sm:mb-20">
      <h2 class="text-xl sm:text-2xl font-display font-bold text-surface-50 mb-6">Shop by Category</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <router-link
          v-for="c in categories" :key="c.id || c.slugified_name"
          :to="'/shop?category=' + (c.slugified_name || c.name)"
          class="bg-surface-800/60 border border-surface-700 rounded-xl p-5 text-center hover:border-gold-500/30 hover:bg-surface-800 transition-all group"
        >
          <span class="text-3xl group-hover:scale-110 transition-transform inline-block">{{ c.icon || '📦' }}</span>
          <p class="text-sm text-surface-200 mt-2 font-medium">{{ c.name }}</p>
        </router-link>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="mb-16 sm:mb-20">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl sm:text-2xl font-display font-bold text-surface-50">{{ storeName || 'Featured' }} Picks</h2>
        <router-link to="/shop" class="text-sm text-gold-500 hover:text-gold-400 font-medium transition-colors">View All →</router-link>
      </div>
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="i in 3" :key="i" class="skeleton h-80 rounded-xl"></div>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <ProductCard v-for="product in featured" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- Recently Viewed -->
    <section v-if="recentlyViewed.length" class="mb-16 sm:mb-20">
      <h2 class="text-xl sm:text-2xl font-display font-bold text-surface-50 mb-6">Recently Viewed</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <router-link
          v-for="item in recentlyViewed" :key="item.id"
          :to="'/product/' + item.id"
          class="bg-surface-800/60 border border-surface-700 rounded-xl p-3 hover:border-gold-500/30 transition-all"
        >
          <OptimizedImage v-if="item.image" :src="item.image" :alt="item.name" wrapperClass="h-24 mb-2 rounded-lg overflow-hidden" imgClass="w-full h-full object-cover rounded-lg" />
          <p class="text-sm text-surface-200 truncate font-medium">{{ item.name }}</p>
        </router-link>
      </div>
    </section>
  </div>
</template>
