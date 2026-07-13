<script setup>
import { computed, ref } from 'vue'
import { useOsimartCart } from '../composables/useOsimartCart'
import { useFavorites } from '../composables/useFavorites'
import { useToast } from '../composables/useToast'
import QuickViewModal from './QuickViewModal.vue'
import OptimizedImage from './OptimizedImage.vue'

const props = defineProps({
  product: { type: Object, required: true },
})

const { addItem, isInCart } = useOsimartCart()
const { addToast } = useToast()
const { toggle: toggleFavorite, isFavorite } = useFavorites()

const quantity = ref(1)
const quickViewProduct = ref(null)
const addingToCart = ref(false)

const badge = computed(() => {
  const p = props.product
  if (!p.price || p.price <= 0) return { label: 'COMING SOON', class: 'bg-surface-600 text-surface-200' }
  if (p.price > 1000) return { label: 'PREMIUM', class: 'bg-danger-500/90 text-white' }
  return null
})

const stockLevel = computed(() => {
  const s = Number(props.product.stock ?? 0)
  if (s === 0) return { label: 'Out of Stock', dot: 'bg-danger-500' }
  if (s <= 5) return { label: `Only ${s} left`, dot: 'bg-warn-400' }
  return { label: `${s} in stock`, dot: 'bg-success-400' }
})

async function handleAddToCart() {
  addingToCart.value = true
  await addItem({
    id: props.product.id,
    uuid: props.product.uuid,
    variantId: props.product.variantId,
    name: props.product.name,
    price: props.product.price,
    image: props.product.image,
  }, quantity.value)
  addToast(`${props.product.name} added to cart`, 2000, 'success')
  setTimeout(() => { addingToCart.value = false }, 600)
}

function openQuickView() { quickViewProduct.value = props.product }
function closeQuickView() { quickViewProduct.value = null }
</script>

<template>
  <div v-spotlight class="bg-surface-800/60 rounded-2xl overflow-hidden border border-surface-700/80 flex flex-col group transition-all duration-300 hover:border-gold-500/20 hover:-translate-y-1 hover:shadow-card-hover">
    <!-- Image -->
    <router-link :to="`/product/${product.uuid || product.id}`" class="block relative h-52 w-full overflow-hidden bg-surface-850">
      <OptimizedImage
        :src="product.image"
        :alt="product.name"
        wrapperClass="h-full w-full"
        imgClass="group-hover:scale-105 transition-transform duration-500 ease-out"
      />
      <span
        v-if="badge"
        class="absolute top-3 left-3 text-[10px] font-bold px-2.5 py-1 rounded-lg shadow-lg backdrop-blur-sm"
        :class="badge.class"
      >{{ badge.label }}</span>
      <div
        v-if="isInCart(product.uuid || product.id)"
        class="absolute top-3 right-3 bg-success-500/90 backdrop-blur-sm text-white text-[10px] font-bold px-2.5 py-1 rounded-lg shadow-lg flex items-center gap-1"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
        In Cart
      </div>
      <!-- Stock indicator -->
      <div class="absolute bottom-3 left-3 flex items-center gap-1.5 bg-surface-900/80 rounded-full px-2.5 py-1 backdrop-blur-sm border border-surface-700/50">
        <span class="w-1.5 h-1.5 rounded-full stock-pulse" :class="stockLevel.dot"></span>
        <span class="text-[10px] text-surface-200 font-medium">{{ stockLevel.label }}</span>
      </div>
    </router-link>

    <!-- Info -->
    <div class="p-4 flex flex-col flex-1">
      <div class="flex justify-between items-start gap-2">
        <router-link :to="`/product/${product.uuid || product.id}`" class="min-w-0">
          <h3 class="text-sm font-semibold text-surface-50 leading-snug line-clamp-2 group-hover:text-gold-400 transition-colors">{{ product.name }}</h3>
        </router-link>
        <button
          @click.stop="toggleFavorite(product.id)"
          class="p-1 rounded-lg hover:bg-surface-700 transition-colors shrink-0"
          :aria-label="isFavorite(product.id) ? 'Remove from favorites' : 'Add to favorites'"
        >
          <svg
            class="w-4 h-4 transition-all duration-200"
            :class="isFavorite(product.id) ? 'text-danger-400 fill-danger-400 scale-110' : 'text-surface-500 hover:text-danger-400'"
            fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </button>
      </div>

      <div class="mt-auto pt-3 border-t border-surface-700/50 flex items-center justify-between gap-2">
        <div class="flex items-baseline gap-1.5">
          <span v-if="product.price > 0" class="text-lg font-bold text-gold-500 price-glow font-mono">${{ Number(product.price).toFixed(2) }}</span>
          <span v-else class="text-xs text-surface-500 font-mono">Price TBD</span>
        </div>
        <div class="flex gap-1.5">
          <button
            @click.stop="openQuickView"
            class="p-2 rounded-lg text-surface-400 bg-surface-700/80 hover:bg-surface-600 hover:text-gold-500 transition-colors"
            aria-label="Quick view"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
          </button>
          <button
            v-if="!isInCart(product.uuid || product.id)"
            @click.stop="handleAddToCart"
            class="bg-gold-500 text-surface-950 px-3.5 py-2 rounded-lg text-xs font-semibold hover:bg-gold-400 active:scale-95 transition-all flex items-center gap-1.5 shadow-glow-gold"
          >
            <svg v-if="addingToCart" class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <span aria-live="polite">{{ addingToCart ? 'Adding...' : 'Add' }}</span>
          </button>
          <button
            v-else
            disabled
            class="bg-success-600/90 text-white px-3.5 py-2 rounded-lg text-xs font-semibold cursor-default flex items-center gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
            In Cart
          </button>
        </div>
      </div>
    </div>
  </div>

  <QuickViewModal :product="quickViewProduct" @close="closeQuickView" />
</template>
