<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { products } from '../data/products'
import { useCart } from '../composables/useCart'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'
import { useFavorites } from '../composables/useFavorites'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'

const route = useRoute()
const productId = route.params.id
const product = computed(() => products.find(p => p.id === productId))

const loading = ref(true)
const addingToCart = ref(false)
const addons = ref([])
const selectedAddons = ref([])

const { addItem } = useCart()

async function fetchAddons() {
  try {
    const { api } = await import('../utils/api')
    const data = await api.addons.list(productId)
    addons.value = data.addons || []
  } catch {
    addons.value = []
  }
}

function toggleAddon(addon) {
  const idx = selectedAddons.value.findIndex(a => a.id === addon.id)
  if (idx >= 0) {
    selectedAddons.value.splice(idx, 1)
  } else {
    selectedAddons.value.push({ id: addon.id, name: addon.name, price: addon.price })
  }
}

function handleAddItem(product) {
  addingToCart.value = true
  addItem({ id: product.id, name: product.name, price: product.price })
  for (const addon of selectedAddons.value) {
    addItem({ id: `addon-${addon.id}`, name: addon.name, price: addon.price })
  }
  selectedAddons.value = []
  setTimeout(() => { addingToCart.value = false }, 600)
}
const { visit } = useRecentlyViewed()
const { toggle: toggleFavorite, isFavorite } = useFavorites()

const notifyEmail = ref('')
const notifySubmitted = ref(false)

const BACK_IN_STOCK_KEY = 'back_in_stock_requests'
const existingRequests = JSON.parse(localStorage.getItem(BACK_IN_STOCK_KEY) || '[]')

function submitNotifyRequest() {
  if (!notifyEmail.value.trim() || !product.value) return
  const requests = JSON.parse(localStorage.getItem(BACK_IN_STOCK_KEY) || '[]')
  requests.push({ productId: product.value.id, email: notifyEmail.value.trim(), timestamp: Date.now() })
  localStorage.setItem(BACK_IN_STOCK_KEY, JSON.stringify(requests))
  notifySubmitted.value = true
  notifyEmail.value = ''
}

function shareProduct() {
  if (!product.value) return
  const url = `${window.location.origin}/product/${product.value.id}`
  if (navigator.share) {
    navigator.share({ title: product.value.name, url })
  } else {
    navigator.clipboard.writeText(url)
      .then(() => { alert('Link copied to clipboard!') })
      .catch(() => { prompt('Copy this link:', url) })
  }
}

onMounted(() => {
  if (product.value) {
    visit(product.value.id)
    fetchAddons()
  }
  setTimeout(() => { loading.value = false }, 600)
})
</script>

<template>
  <SkeletonLoader v-if="loading" type="detail" />
  <div v-else-if="product" class="max-w-7xl mx-auto px-4 py-12 pb-24 sm:pb-12">
    <Breadcrumbs :crumbs="[{ label: 'Shop', to: '/shop' }, { label: product.name }]" />
    <div class="grid md:grid-cols-2 gap-8">
      <div class="relative">
        <div class="overflow-hidden rounded-xl group">
          <img :src="product.image" :alt="product.name" loading="lazy" class="w-full h-72 sm:h-96 object-cover transition-transform duration-500 ease-out group-hover:scale-110" />
        </div>
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

        <!-- Stock status -->
        <div v-if="product.stock !== undefined" class="mt-3">
          <span v-if="product.stock === 0"
                class="inline-flex items-center gap-1.5 bg-red-950/30 text-red-400 text-xs font-mono px-3 py-1.5 rounded-full border border-red-800/50">
            <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span>
            Out of Stock
          </span>
          <span v-else-if="product.stock <= 5"
                class="inline-flex items-center gap-1.5 bg-amber-950/30 text-amber-400 text-xs font-mono px-3 py-1.5 rounded-full border border-amber-800/50">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
            Only {{ product.stock }} left in stock
          </span>
          <span v-else
                class="inline-flex items-center gap-1.5 bg-emerald-950/30 text-emerald-400 text-xs font-mono px-3 py-1.5 rounded-full border border-emerald-800/50">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            In Stock
          </span>
        </div>

        <!-- Back-in-stock notification -->
        <div v-if="product.stock === 0 && !notifySubmitted" class="mt-4 p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
          <p class="text-sm text-slate-300 font-medium mb-2">Notify me when back in stock</p>
          <div class="flex gap-2">
            <input
              v-model="notifyEmail"
              type="email"
              placeholder="your@email.com"
              class="flex-1 bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400"
            >
            <button @click="submitNotifyRequest"
                    class="bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold px-4 py-2 rounded-md transition-all active:scale-95">
              Notify
            </button>
          </div>
        </div>
        <div v-else-if="notifySubmitted" class="mt-4 text-sm text-emerald-400 font-medium">
          ✓ We'll email you when this product is back in stock.
        </div>

        <div class="flex items-center gap-3 mt-4">
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
          <button
            @click="shareProduct"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm bg-slate-800 text-slate-400 border border-slate-700 hover:border-cyan-800/50 hover:text-cyan-400 transition-colors"
            aria-label="Share product"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/>
            </svg>
            Share
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
        <!-- Add-ons / Micro-transactions -->
        <div v-if="addons.length" class="mt-6 p-4 bg-slate-900/50 border border-slate-800 rounded-lg">
          <h3 class="text-white font-semibold text-sm mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Add-ons &amp; Extras
          </h3>
          <div class="space-y-2">
            <label
              v-for="addon in addons"
              :key="addon.id"
              class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors"
              :class="selectedAddons.find(a => a.id === addon.id) ? 'bg-cyan-950/20 border border-cyan-800/40' : 'bg-slate-800/30 border border-slate-800 hover:border-slate-700'"
            >
              <input
                type="checkbox"
                :checked="selectedAddons.find(a => a.id === addon.id)"
                @change="toggleAddon(addon)"
                class="w-4 h-4 rounded border-slate-600 bg-slate-800 text-cyan-500 focus:ring-cyan-400 focus:ring-offset-0"
              />
              <div class="flex-1 min-w-0">
                <span class="text-sm text-slate-200 font-medium">{{ addon.name }}</span>
                <p v-if="addon.description" class="text-xs text-slate-500 truncate">{{ addon.description }}</p>
              </div>
              <span class="text-sm text-cyan-400 font-mono font-medium shrink-0">+${{ addon.price.toFixed(2) }}</span>
            </label>
          </div>
        </div>

        <button v-if="product.stock !== 0" @click="handleAddItem(product)" 
                class="mt-8 w-full sm:w-auto bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 px-10 rounded-lg transition-all active:scale-95 flex items-center justify-center gap-2">
          <svg v-if="addingToCart" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
        </button>
        <button v-else disabled
                class="mt-8 w-full sm:w-auto bg-slate-700 text-slate-500 font-semibold py-3 px-10 rounded-lg cursor-not-allowed flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          Out of Stock
        </button>
      </div>
    </div>

    <!-- Sticky mobile add-to-cart bar -->
    <div class="fixed bottom-0 left-0 right-0 z-30 bg-slate-900/95 backdrop-blur border-t border-slate-800 p-3 sm:hidden">
      <div class="flex items-center justify-between gap-3">
        <div class="min-w-0">
          <p class="text-sm text-white truncate font-medium">{{ product.name }}</p>
          <p class="text-cyan-400 font-mono font-bold">
            ${{ (product.price + selectedAddons.reduce((s, a) => s + a.price, 0)).toFixed(2) }}
          </p>
        </div>
        <button
          v-if="product.stock !== 0"
          @click="addItem({ id: product.id, name: product.name, price: product.price })"
          class="bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-2.5 px-6 rounded-lg transition-all active:scale-95 shrink-0 flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          Add to Cart
        </button>
        <button v-else disabled
                class="bg-slate-700 text-slate-500 font-semibold py-2.5 px-6 rounded-lg cursor-not-allowed shrink-0 flex items-center gap-2">
          Out of Stock
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