<script setup>
import { ref, computed, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import { normalizeProduct, pick } from '../utils/product'
import { resolveImage } from '../utils/images'
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
    <section class="text-center py-20">
      <h1 class="text-5xl font-bold text-white">Your Command Station Awaits</h1>
      <p class="text-slate-400 max-w-2xl mx-auto mt-4">Premium hardware, custom-tuned for silence and power.</p>
      <div class="flex justify-center gap-4 mt-8">
        <router-link to="/shop" class="bg-cyan-600 text-white px-8 py-3 rounded-md font-semibold hover:bg-cyan-500">Shop Now</router-link>
      </div>
    </section>

    <section v-if="categories.length" class="mb-20">
      <h2 class="text-2xl font-bold text-white mb-6">Shop by Category</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <router-link
          v-for="c in categories" :key="c.id || c.slugified_name"
          :to="'/shop?category=' + (c.slugified_name || c.name)"
          class="bg-slate-800/80 rounded-xl p-5 text-center hover:bg-slate-700/80"
        >
          <span class="text-3xl">{{ c.icon || '📦' }}</span>
          <p class="text-sm text-slate-300 mt-2">{{ c.name }}</p>
        </router-link>
      </div>
    </section>

    <section class="mb-20">
      <h2 class="text-2xl font-bold text-white mb-6">{{ storeName || 'Featured' }} Picks</h2>
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="skeleton h-80 rounded-xl"></div>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <ProductCard v-for="product in featured" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <section v-if="recentlyViewed.length" class="mb-20">
      <h2 class="text-2xl font-bold text-white mb-6">Recently Viewed</h2>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <router-link
          v-for="item in recentlyViewed" :key="item.id"
          :to="'/product/' + item.id"
          class="bg-slate-800/80 rounded-lg p-3"
        >
          <OptimizedImage v-if="item.image" :src="item.image" :alt="item.name" wrapperClass="h-24 mb-2" imgClass="w-full h-full object-cover rounded" />
          <p class="text-sm text-slate-300">{{ item.name }}</p>
        </router-link>
      </div>
    </section>
  </div>
</template>
