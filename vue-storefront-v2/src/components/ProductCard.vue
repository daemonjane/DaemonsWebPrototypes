<script setup>
/**
 * Reusable product card with image, rating, price, specs (expandable on hover),
 * quick-view modal trigger, favorites toggle, and add-to-cart.
 *
 * @component
 * @prop {Object} product - The product data object from products.js
 * @prop {boolean} [showFull=false] - If true, shows specs + quantity selector on hover
 */
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'
import { useFavorites } from '../composables/useFavorites'
import QuickViewModal from './QuickViewModal.vue'

const props = defineProps({
  product: { type: Object, required: true },
  showFull: { type: Boolean, default: false }
})

const { addItem } = useCart()

const badge = computed(() => {
  const newIds = ['stream-deck', 'gaming-chair', 'cpu-cooler', 'nvme-ssd', 'sleeved-cables', 'microphone']
  const bestSellerIds = ['vanguard-desktop', 'ultrawide-monitor', 'gaming-mouse', 'wireless-headset']
  if (newIds.includes(props.product.id)) return { label: 'NEW', class: 'bg-emerald-600 text-white' }
  if (bestSellerIds.includes(props.product.id)) return { label: 'BEST SELLER', class: 'bg-amber-600 text-white' }
  if (props.product.price > 1000) return { label: 'PREMIUM', class: 'bg-fuchsia-600 text-white' }
  return null
})

const stockLevel = computed(() => {
  const s = props.product.stock
  if (s === 0) return { level: 'out', label: 'Out of Stock', dot: 'bg-red-500', bar: 'w-0 bg-red-500' }
  if (s <= 5) return { level: 'low', label: 'Low Stock', dot: 'bg-amber-400', bar: 'w-1/3 bg-amber-400' }
  if (s <= 20) return { level: 'medium', label: `${s} in stock`, dot: 'bg-yellow-500', bar: 'w-2/3 bg-yellow-500' }
  return { level: 'full', label: 'In Stock', dot: 'bg-emerald-400', bar: 'w-full bg-emerald-400' }
})
const { toggle: toggleFavorite, isFavorite } = useFavorites()
const router = useRouter()
const quantity = ref(1)
const quickViewProduct = ref(null)
const addingToCart = ref(false)

function increment() { quantity.value++ }
function decrement() { if (quantity.value > 1) quantity.value-- }

function handleAddToCart() {
  addingToCart.value = true
  addItem({ id: props.product.id, name: props.product.name, price: props.product.price }, quantity.value)
  setTimeout(() => { addingToCart.value = false }, 600)
  quantity.value = 1
}

function navigateToProduct() {
  router.push(`/product/${props.product.id}`)
}

function openQuickView() {
  quickViewProduct.value = props.product
}

function closeQuickView() {
  quickViewProduct.value = null
}
</script>

<template>
  <div
    class="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 flex flex-col group transition-all duration-300 hover:border-slate-700 hover:-translate-y-1 hover:shadow-xl hover:shadow-cyan-950/20"
    role="button"
    :aria-label="`View ${product.name}`"
    tabindex="0"
    @click="navigateToProduct"
    @keydown.enter.prevent="navigateToProduct"
  >
    <!-- Product image (clickable area inside the card) -->
    <router-link :to="`/product/${product.id}`" class="block h-48 w-full bg-slate-800 overflow-hidden relative" @click.stop>
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
        loading="lazy"
      />
      <span
        v-if="badge"
        class="absolute top-2 left-2 text-[10px] font-bold px-2 py-0.5 rounded-md shadow-lg"
        :class="badge.class"
      >{{ badge.label }}</span>
      <!-- Stock level dots -->
      <div class="absolute bottom-2 left-2 flex items-center gap-1.5 bg-slate-900/80 rounded-full px-2 py-1 backdrop-blur-sm">
        <span class="w-2 h-2 rounded-full" :class="stockLevel.dot"></span>
        <span class="text-[10px] text-slate-300 font-medium">{{ stockLevel.label }}</span>
      </div>
    </router-link>

    <div class="p-5 flex flex-col flex-1">
      <div class="flex justify-between items-start gap-2">
        <h3 class="text-lg font-bold text-white leading-snug">{{ product.name }}</h3>
        <div class="flex items-center gap-1.5 shrink-0">
          <button
            @click.stop="toggleFavorite(product.id)"
            class="p-1 rounded-md hover:bg-slate-800 transition-colors"
            :aria-label="isFavorite(product.id) ? 'Remove from favorites' : 'Add to favorites'"
          >
            <svg
              class="w-4 h-4 transition-colors"
              :class="isFavorite(product.id) ? 'text-pink-400 fill-pink-400' : 'text-slate-500 hover:text-pink-400'"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
          <div class="star-rating text-yellow-400 text-sm whitespace-nowrap" aria-hidden="true">
            {{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}
          </div>
        </div>
      </div>
      <p class="text-slate-400 text-sm mt-1 line-clamp-2">{{ product.description }}</p>
      <div class="mt-2 text-2xl font-bold text-cyan-400">${{ product.price.toFixed(2) }}</div>

      <!-- Expandable section (shop page) -->
      <div
        v-if="showFull"
        class="extra-content mt-3 space-y-3 opacity-0 max-h-0 overflow-hidden group-hover:opacity-100 group-hover:max-h-60 transition-all duration-300 ease-in-out"
      >
        <div class="border-t border-slate-700 pt-2">
          <p class="text-xs text-slate-400 font-semibold mb-1">Technical specs:</p>
          <ul class="text-xs text-slate-300 list-disc list-inside space-y-0.5">
            <li v-for="spec in product.specs" :key="spec">{{ spec }}</li>
          </ul>
        </div>
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <button
              @click.stop="decrement"
              class="bg-slate-700 px-2 py-1 rounded text-sm"
              aria-label="Decrease quantity"
            >-</button>
            <span class="text-sm w-6 text-center">{{ quantity }}</span>
            <button
              @click.stop="increment"
              class="bg-slate-700 px-2 py-1 rounded text-sm"
              aria-label="Increase quantity"
            >+</button>
          </div>
          <div class="flex gap-1.5">
            <button
              @click.stop="openQuickView"
              class="px-2 py-1 rounded text-xs bg-slate-700 text-slate-400 hover:bg-slate-600 hover:text-cyan-400 transition-colors"
              aria-label="Quick view"
              title="Quick view"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
            </button>
            <button
              @click.stop="handleAddToCart"
              class="bg-cyan-600 text-white px-4 py-1.5 rounded-md text-sm font-semibold hover:bg-cyan-500 transition-colors flex items-center gap-1.5"
            >
              <svg v-if="addingToCart" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              <span v-else class="w-3.5 h-3.5"></span>
              {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Compact add-to-cart (other pages) -->
      <div v-else class="mt-auto pt-4 border-t border-slate-800 flex items-center justify-between gap-2">
        <span class="text-lg font-bold text-white">${{ product.price.toFixed(2) }}</span>
        <div class="flex gap-1.5">
          <button
            @click.stop="openQuickView"
            class="px-2.5 py-2 rounded-md text-xs font-medium bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-cyan-400 transition-colors"
            aria-label="Quick view"
            title="Quick view"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
          </button>
          <button
            @click.stop="handleAddToCart"
            class="bg-cyan-600 text-white px-4 py-2 rounded-md text-sm font-semibold hover:bg-cyan-500 active:scale-95 transition-all flex items-center gap-1.5"
          >
            <svg v-if="addingToCart" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <span v-else class="w-3.5 h-3.5"></span>
            {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <QuickViewModal :product="quickViewProduct" @close="closeQuickView" />
</template>

<style scoped>
.extra-content {
  transition: max-height 0.3s ease-out, opacity 0.2s ease;
}
.group:hover .extra-content {
  max-height: 200px;
  opacity: 1;
}
</style>