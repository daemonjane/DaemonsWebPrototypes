<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import { normalizeProduct, pick } from '../utils/product'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'

const loading = ref(true)
const products = ref([])
const categories = ref([])
const storeName = ref('')
const { items: recentlyViewed } = useRecentlyViewed()

const stats = [
  { value: '500+', label: 'Products' },
  { value: '24h', label: 'Fast Shipping' },
  { value: '99%', label: 'Satisfaction' },
  { value: '24/7', label: 'Support' },
]

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
    <section class="relative text-center py-20 sm:py-28 lg:py-36 overflow-hidden">
      <div class="hero-glow"></div>
      <div class="relative z-10 max-w-3xl mx-auto px-4">
        <div class="inline-flex items-center gap-2 bg-gold-500/10 border border-gold-500/20 rounded-full px-4 py-1.5 mb-8 backdrop-blur-sm">
          <span class="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse"></span>
          <span class="text-xs font-medium text-gold-400 uppercase tracking-widest">High-Tier Hardware</span>
        </div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-display font-bold text-surface-50 leading-[1.1] tracking-tight">
          Peak Performance<br>
          <span class="text-gradient-gold">Hardware</span>
        </h1>
        <p class="text-surface-400 max-w-lg mx-auto mt-6 text-base sm:text-lg leading-relaxed">
          Precision-sourced components. Direct vendor supply chains. Custom-tuned systems built for silence and power.
        </p>
        <div class="flex justify-center gap-4 mt-10">
          <router-link
            to="/shop"
            class="bg-gold-500 text-surface-950 px-8 py-3.5 rounded-xl font-display font-semibold hover:bg-gold-400 transition-all active:scale-95 shadow-glow-gold text-sm sm:text-base"
          >
            Shop Now
          </router-link>
          <router-link
            to="/about"
            class="border border-surface-600 text-surface-300 px-8 py-3.5 rounded-xl font-display font-semibold hover:border-gold-500/30 hover:text-surface-100 hover:bg-surface-800/50 transition-all text-sm sm:text-base"
          >
            Learn More
          </router-link>
        </div>
        <!-- Stats bar -->
        <div class="flex justify-center gap-8 sm:gap-12 mt-14 pt-8 border-t border-surface-700/50">
          <div v-for="stat in stats" :key="stat.label" class="text-center">
            <p class="text-lg sm:text-xl font-bold text-gold-500 font-mono">{{ stat.value }}</p>
            <p class="text-xs text-surface-500 mt-0.5">{{ stat.label }}</p>
          </div>
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
          class="bg-surface-800/60 border border-surface-700/80 rounded-2xl p-5 sm:p-6 text-center hover:border-gold-500/30 hover:bg-surface-800 transition-all duration-300 group"
        >
          <span class="text-3xl group-hover:scale-110 transition-transform duration-300 inline-block">{{ c.icon || '📦' }}</span>
          <p class="text-sm text-surface-200 mt-3 font-medium group-hover:text-surface-50 transition-colors">{{ c.name }}</p>
        </router-link>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="mb-16 sm:mb-20">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl sm:text-2xl font-display font-bold text-surface-50">{{ storeName || 'Featured' }} Picks</h2>
        <router-link to="/shop" class="text-sm text-gold-500 hover:text-gold-400 font-medium transition-colors flex items-center gap-1">
          View All
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </router-link>
      </div>
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div v-for="i in 3" :key="i" class="skeleton h-80 rounded-2xl"></div>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
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
          class="bg-surface-800/60 border border-surface-700/80 rounded-2xl p-3 hover:border-gold-500/20 hover:-translate-y-0.5 transition-all duration-300"
        >
          <OptimizedImage v-if="item.image" :src="item.image" :alt="item.name" wrapperClass="h-28 mb-2.5 rounded-xl overflow-hidden" imgClass="w-full h-full object-cover" />
          <p class="text-sm text-surface-200 truncate font-medium">{{ item.name }}</p>
        </router-link>
      </div>
    </section>

    <!-- Trust Bar -->
    <section class="mb-16 sm:mb-20">
      <div class="bg-surface-800/40 border border-surface-700/50 rounded-2xl p-8 sm:p-10 grid grid-cols-1 sm:grid-cols-3 gap-6 sm:gap-8 text-center">
        <div class="space-y-2">
          <div class="w-10 h-10 rounded-xl bg-gold-500/10 flex items-center justify-center mx-auto">
            <svg class="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          </div>
          <h3 class="font-display font-semibold text-surface-50">Verified Authentic</h3>
          <p class="text-xs text-surface-400">Direct from authorized distributors. No gray market.</p>
        </div>
        <div class="space-y-2">
          <div class="w-10 h-10 rounded-xl bg-gold-500/10 flex items-center justify-center mx-auto">
            <svg class="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </div>
          <h3 class="font-display font-semibold text-surface-50">Fast Fulfillment</h3>
          <p class="text-xs text-surface-400">Same-day processing on in-stock items.</p>
        </div>
        <div class="space-y-2">
          <div class="w-10 h-10 rounded-xl bg-gold-500/10 flex items-center justify-center mx-auto">
            <svg class="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          </div>
          <h3 class="font-display font-semibold text-surface-50">Buyer Protection</h3>
          <p class="text-xs text-surface-400">Secure checkout. Full refund guarantee.</p>
        </div>
      </div>
    </section>
  </div>
</template>
