<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOsimartCart } from '../composables/useOsimartCart'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'
import { useFavorites } from '../composables/useFavorites'
import Breadcrumbs from '../components/Breadcrumbs.vue'
import OptimizedImage from '../components/OptimizedImage.vue'
import SkeletonLoader from '../components/SkeletonLoader.vue'
import ProductCard from '../components/ProductCard.vue'
import { normalizeProductDetail } from '../utils/product'
import { resolveImage } from '../utils/images'

const route = useRoute()
const productId = route.params.id

const product = ref(null)
const loading = ref(true)
const addingToCart = ref(false)
const addons = ref([])
const selectedAddons = ref([])
const quantity = ref(1)
const selectedImage = ref(0)
const relatedProducts = ref([])
const { addItem, isInCart } = useOsimartCart()

const bisEmail = ref('')
const bisPending = ref(false)
const bisMsg = ref('')
const bisMsgClass = ref('')
const bisSubscribed = ref(false)

async function subscribeBIS() {
  if (!bisEmail.value) return
  bisPending.value = true
  bisMsg.value = ''
  try {
    const { api } = await import('../utils/api')
    const data = await api.backInStock.subscribe({ product_slug: productId, email: bisEmail.value, product_name: product.name })
    bisMsg.value = data?.message || 'Subscribed!'
    bisMsgClass.value = 'text-success-400'
    bisSubscribed.value = true
  } catch (e) {
    bisMsg.value = e.message
    bisMsgClass.value = 'text-danger-400'
  } finally {
    bisPending.value = false
  }
}

async function fetchProduct() {
  try {
    const { api } = await import('../utils/api')
    const data = await api.osimart.productDetail(productId)
    if (data) {
      product.value = normalizeProductDetail(data)
    }
  } catch (e) {
    console.warn('Product fetch failed', e)
  }
}

async function fetchAddons() {
  try {
    const { api } = await import('../utils/api')
    const data = await api.addons.list(productId)
    addons.value = data.addons || []
  } catch {
    addons.value = []
  }
}

async function fetchRelated() {
  try {
    const { api } = await import('../utils/api')
    const cat = product.value?.category
    const data = await api.osimart.products({ limit: 20 })
    const items = data.results || data || []
    if (items.length > 0) {
      const sameCategory = cat && cat !== 'uncategorized'
        ? items.filter(p => {
            const pcats = p.categories || []
            return pcats.some(c => (c.category?.slugified_name || c.slugified_name || c.name) === cat)
          })
        : []
      const pool = sameCategory.length >= 4 ? sameCategory : items
      relatedProducts.value = pool
        .filter(p => p.id !== product.value?.uuid && p.slugified_name !== product.value?.id)
        .slice(0, 4)
        .map(normalizeProductDetail)
    }
  } catch {
    relatedProducts.value = []
  }
}

function toggleAddon(addon) {
  const idx = selectedAddons.value.findIndex(a => a.id === addon.id)
  if (idx >= 0) { selectedAddons.value.splice(idx, 1) }
  else { selectedAddons.value.push({ id: addon.id, name: addon.name, price: addon.price }) }
}

async function handleAddItem() {
  if (!product.value) return
  addingToCart.value = true
  await addItem(
    { id: product.value.uuid || product.value.id, uuid: product.value.uuid, variantId: product.value.variantId, name: product.value.name, price: product.value.price, image: product.value.image },
    quantity.value
  )
  for (const addon of selectedAddons.value) {
    await addItem({ id: `addon-${addon.id}`, name: addon.name, price: addon.price })
  }
  selectedAddons.value = []
  addingToCart.value = false
}

const totalPrice = computed(() => {
  if (!product.value) return 0
  return (product.value.price + selectedAddons.value.reduce((s, a) => s + a.price, 0)) * quantity.value
})
const { visit } = useRecentlyViewed()
const { toggle: toggleFavorite, isFavorite } = useFavorites()

const selectedVariant = ref(null)

function selectVariant(v) { selectedVariant.value = v }

function variantStock(v) {
  if (!v) return 0
  let s = Number(v.tracked_stock ?? v.stock ?? v.quantity ?? 0)
  if (s <= 0 && Array.isArray(v.locations_stock)) {
    for (const loc of v.locations_stock) {
      s += Number(loc.stock ?? 0)
    }
  }
  return s
}

const stockDisplay = computed(() => {
  if (selectedVariant.value) return variantStock(selectedVariant.value)
  return product.value?.stock ?? 0
})

function shareProduct() {
  if (!product.value) return
  const url = `${window.location.origin}/product/${product.value.uuid || product.value.id}`
  if (navigator.share) { navigator.share({ title: product.value.name, url }) }
  else { navigator.clipboard.writeText(url).then(() => alert('Link copied!')).catch(() => prompt('Copy this link:', url)) }
}


onMounted(async () => {
  await fetchProduct()
  if (product.value) {
    visit({ id: product.value.uuid || product.value.id, name: product.value.name, price: product.value.price, image: product.value.image })
    fetchAddons()
    fetchRelated()
  }
  loading.value = false
})
</script>

<template>
  <SkeletonLoader v-if="loading" type="detail" />
  <div v-else-if="product" class="max-w-7xl mx-auto px-4 py-12 pb-24 sm:pb-12">
    <Breadcrumbs :crumbs="[
      { label: 'Shop', to: '/shop' },
      ...(product.category ? [{ label: product.categoryName || product.category, to: '/shop?category=' + product.category }] : []),
      { label: product.name }
    ]" />

    <div class="grid md:grid-cols-2 gap-8 lg:gap-12">
      <!-- Image gallery -->
      <div>
        <div class="overflow-hidden rounded-2xl bg-surface-900 border border-surface-700 relative">
          <OptimizedImage
            :src="product.images.length ? resolveImage(product.images[selectedImage]) : product.image"
            :alt="product.name"
            wrapperClass="w-full h-72 sm:h-96"
            imgClass="hover:scale-105 transition-transform duration-500"
            :priority="true"
          />
          <div
            v-if="isInCart(product.uuid || product.id)"
            class="absolute top-3 right-3 bg-success-500 text-surface-50 text-xs font-bold px-3 py-1 rounded-full shadow-lg flex items-center gap-1.5"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
            In Cart
          </div>
        </div>
        <div v-if="product.images.length > 1" class="flex gap-2 mt-3 overflow-x-auto pb-1">
          <button v-for="(img, i) in product.images" :key="i" @click="selectedImage = i"
                  :class="['w-16 h-16 rounded-lg border-2 overflow-hidden shrink-0 transition-all', selectedImage === i ? 'border-gold-500' : 'border-surface-700 hover:border-surface-600']">
            <OptimizedImage :src="resolveImage(img)" :alt="'View ' + (i + 1)" wrapperClass="h-full w-full" />
          </button>
        </div>
      </div>

      <!-- Product info -->
      <div>
        <div class="flex flex-wrap items-center gap-2 mb-2">
          <span class="text-xs font-mono text-gold-500 uppercase tracking-wider bg-gold-500/10 px-2 py-1 rounded">{{ product.categoryName || product.category }}</span>
          <router-link v-if="product.brand" :to="'/shop?brand=' + (product.brand.slugified_name || product.brand.name)"
                       class="text-xs font-mono text-surface-400 hover:text-gold-500 bg-surface-800 px-2 py-1 rounded transition-colors">
            {{ product.brand.name }}
          </router-link>
          <router-link v-for="col in product.collections" :key="col.id || col.name"
                       :to="'/shop?collection=' + (col.slugified_name || col.name)"
                       class="text-xs font-mono text-surface-300 hover:text-surface-200 bg-surface-700 px-2 py-1 rounded transition-colors">
            {{ col.name }}
          </router-link>
        </div>

        <h1 class="text-3xl sm:text-4xl font-bold text-surface-50 font-display">{{ product.name }}</h1>

        <!-- Rating -->
        <div class="flex items-center gap-2 mt-2">
          <span class="text-yellow-400 text-sm">{{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}</span>
          <span class="text-xs text-surface-500">{{ product.rating }}</span>
        </div>

        <p class="text-3xl text-gold-500 mt-4 font-mono font-bold">${{ Number(totalPrice || 0).toFixed(2) }}</p>

        <!-- Stock status -->
        <div v-if="stockDisplay >= 0" class="mt-3" aria-live="polite">
          <span v-if="stockDisplay === 0" class="inline-flex items-center gap-1.5 bg-danger-500/10 text-danger-400 text-xs font-mono px-3 py-1.5 rounded-full border border-danger-500/30">
            <span class="w-1.5 h-1.5 rounded-full bg-danger-500 animate-pulse"></span> Out of Stock
          </span>
          <span v-else-if="stockDisplay <= 5" class="inline-flex items-center gap-1.5 bg-warn-500/10 text-warn-400 text-xs font-mono px-3 py-1.5 rounded-full border border-warn-500/30">
            <span class="w-1.5 h-1.5 rounded-full bg-warn-500"></span> Only {{ stockDisplay }} left
          </span>
          <span v-else class="inline-flex items-center gap-1.5 bg-success-500/10 text-success-400 text-xs font-mono px-3 py-1.5 rounded-full border border-success-500/30">
            <span class="w-1.5 h-1.5 rounded-full bg-success-500"></span> In Stock
          </span>
        </div>

        <!-- Variants -->
        <div v-if="product.variants.length" class="mt-5">
          <h3 class="text-sm text-surface-400 font-medium mb-2">Options</h3>
          <div class="flex flex-wrap gap-2">
            <button v-for="v in product.variants" :key="v.id || v.name"
                    @click="selectVariant(v)"
                    :class="['px-4 py-2 rounded-lg text-sm border transition-all', selectedVariant?.id === v.id || selectedVariant?.name === v.name ? 'bg-gold-500/10 border-gold-500 text-gold-400' : 'bg-surface-800 border-surface-700 text-surface-200 hover:border-surface-600']">
              {{ v.name || v.value }}
              <span class="ml-1.5 inline-flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full" :class="variantStock(v) === 0 ? 'bg-danger-500' : variantStock(v) <= 5 ? 'bg-warn-400' : 'bg-success-400'"></span>
                <span class="text-[10px]" :class="variantStock(v) === 0 ? 'text-danger-400' : 'text-success-400'">{{ variantStock(v) }}</span>
              </span>
            </button>
          </div>
        </div>

        <!-- Quantity -->
        <div class="mt-5 flex items-center gap-3">
          <span class="text-sm text-surface-400 font-medium">Qty:</span>
          <div class="flex items-center border border-surface-700 rounded-lg overflow-hidden">
            <button @click="quantity = Math.max(1, quantity - 1)" class="px-3 py-2 text-surface-400 hover:text-surface-50 hover:bg-surface-700 transition-colors text-lg" :disabled="quantity <= 1" :aria-label="'Decrease quantity'">−</button>
            <span class="px-4 py-2 text-surface-50 font-mono text-sm min-w-[3rem] text-center border-x border-surface-700">{{ quantity }}</span>
            <button @click="quantity = Math.min(stockDisplay || 99, quantity + 1)" class="px-3 py-2 text-surface-400 hover:text-surface-50 hover:bg-surface-700 transition-colors text-lg" :disabled="quantity >= (stockDisplay || 99)" :aria-label="'Increase quantity'">+</button>
          </div>
        </div>

        <!-- Back-in-stock (API) -->
        <div v-if="stockDisplay === 0 && !bisSubscribed" class="mt-4 p-4 bg-surface-800/60 border border-surface-700 rounded-lg">
          <p class="text-sm text-surface-200 font-medium mb-2">Notify me when back in stock</p>
          <div class="flex gap-2">
            <input v-model="bisEmail" type="email" placeholder="your@email.com" class="flex-1 bg-surface-800 border border-surface-700 rounded-md px-3 py-2 text-sm text-surface-100 placeholder-surface-500 focus:outline-none focus:ring-2 focus:ring-gold-500" :disabled="bisPending" />
            <button @click="subscribeBIS" :disabled="bisPending || !bisEmail" class="bg-gold-500 hover:bg-gold-400 disabled:opacity-50 text-surface-900 text-sm font-semibold px-4 py-2 rounded-md transition-all active:scale-95">Notify</button>
          </div>
        </div>
        <p v-if="bisMsg" class="mt-2 text-sm" :class="bisMsgClass" aria-live="polite">{{ bisMsg }}</p>
        <div v-else-if="bisSubscribed" class="mt-4 text-sm text-success-400 font-medium" aria-live="polite">✓ We'll email you when back in stock.</div>

        <!-- Action buttons -->
        <div class="flex flex-wrap items-center gap-3 mt-4">
          <button @click="toggleFavorite(product.uuid || product.id)" :class="['flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm transition-colors', isFavorite(product.uuid || product.id) ? 'bg-danger-500/10 text-danger-400 border border-danger-500/30' : 'bg-surface-800 text-surface-400 border border-surface-700 hover:border-danger-500/30 hover:text-danger-400']" :aria-label="isFavorite(product.uuid || product.id) ? 'Remove from favorites' : 'Add to favorites'">
            <svg class="w-4 h-4" :class="isFavorite(product.uuid || product.id) ? 'fill-danger-400' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            {{ isFavorite(product.uuid || product.id) ? 'Favorited' : 'Favorite' }}
          </button>
          <button @click="shareProduct" class="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm bg-surface-800 text-surface-400 border border-surface-700 hover:border-gold-500/30 hover:text-gold-500 transition-colors" aria-label="Share product">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
            Share
          </button>
        </div>

        <!-- Description -->
        <div class="mt-5 text-surface-400 leading-relaxed text-sm">{{ product.description }}</div>

        <!-- Specs by section -->
        <div v-if="product.sections.length" class="mt-6 space-y-4">
          <h3 class="text-surface-50 font-semibold flex items-center gap-2">
            <svg class="w-4 h-4 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            Technical Specs
          </h3>
          <div v-for="(section, si) in product.sections" :key="si">
            <p v-if="section.name" class="text-xs text-surface-500 font-medium uppercase tracking-wider mb-2">{{ section.name }}</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div v-for="item in (section.items || [])" :key="item.name || item" class="bg-surface-800/60 border border-surface-700/50 rounded-lg px-3 py-2 text-sm">
                <span class="text-surface-500 text-xs">{{ item.name || item.label }}:</span>
                <span class="text-surface-100 font-mono ml-1">{{ item.value || item.description || item }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Add-ons -->
        <div v-if="addons.length" class="mt-6 p-4 bg-surface-800/60 border border-surface-700 rounded-lg">
          <h3 class="text-surface-50 font-semibold text-sm mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
            Add-ons &amp; Extras
          </h3>
          <div class="space-y-2">
            <label v-for="addon in addons" :key="addon.id" class="flex items-center gap-3 px-3 py-2 rounded-lg cursor-pointer transition-colors" :class="selectedAddons.find(a => a.id === addon.id) ? 'bg-gold-500/10 border border-gold-500/30' : 'bg-surface-800/60 border border-surface-700 hover:border-surface-600'">
              <input type="checkbox" :checked="selectedAddons.find(a => a.id === addon.id)" @change="toggleAddon(addon)" class="w-4 h-4 rounded border-surface-600 bg-surface-800 text-gold-500 focus:ring-gold-500 focus:ring-offset-0" :aria-label="'Add ' + addon.name + ' for $' + parseFloat(addon.price || 0).toFixed(2)" />
              <div class="flex-1 min-w-0">
                <span class="text-sm text-surface-100 font-medium">{{ addon.name }}</span>
                <p v-if="addon.description" class="text-xs text-surface-500 truncate">{{ addon.description }}</p>
              </div>
              <span class="text-sm text-gold-500 font-mono font-medium shrink-0">+${{ parseFloat(addon.price || 0).toFixed(2) }}</span>
            </label>
          </div>
        </div>

        <!-- Add to cart -->
        <template v-if="product.stock !== 0">
          <button v-if="!isInCart(product.uuid || product.id)" @click="handleAddItem" class="mt-8 w-full sm:w-auto bg-gold-500 hover:bg-gold-400 text-surface-900 font-semibold py-3 px-10 rounded-lg transition-all active:scale-95 flex items-center justify-center gap-2">
            <svg v-if="addingToCart" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
            {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
          </button>
          <button v-else disabled class="mt-8 w-full sm:w-auto bg-success-600 text-surface-50 font-semibold py-3 px-10 rounded-lg cursor-default flex items-center justify-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
            In Cart
          </button>
        </template>
        <button v-else disabled class="mt-8 w-full sm:w-auto bg-surface-700 text-surface-500 font-semibold py-3 px-10 rounded-lg cursor-not-allowed flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
          Out of Stock
        </button>
      </div>
    </div>

    <!-- Related products -->
    <section v-if="relatedProducts.length" class="mt-16 space-y-6">
      <h2 class="text-xl sm:text-2xl font-bold text-surface-50 font-display">Related Products</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
        <ProductCard v-for="rp in relatedProducts" :key="rp.uuid || rp.id" :product="rp" />
      </div>
    </section>

    <!-- Mobile bar -->
    <div class="fixed bottom-0 left-0 right-0 z-30 bg-surface-900/95 backdrop-blur border-t border-surface-750 p-3 sm:hidden">
      <div class="flex items-center justify-between gap-3">
        <div class="min-w-0">
          <p class="text-sm text-surface-50 truncate font-medium">{{ product.name }}</p>
          <p class="text-gold-500 font-mono font-bold">${{ Number(totalPrice || 0).toFixed(2) }}</p>
        </div>
        <button v-if="stockDisplay > 0" @click="handleAddItem" :disabled="addingToCart" class="bg-gold-500 hover:bg-gold-400 text-surface-900 font-semibold py-2.5 px-6 rounded-lg transition-all active:scale-95 shrink-0 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed">
          <svg v-if="addingToCart" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
          {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
        </button>
        <button v-else disabled class="bg-surface-700 text-surface-500 font-semibold py-2.5 px-6 rounded-lg cursor-not-allowed shrink-0">Out of Stock</button>
      </div>
    </div>
  </div>
  <div v-else class="text-center py-20">
    <p class="text-4xl mb-4">🔍</p>
    <p class="text-surface-400 text-lg">Product not found.</p>
    <router-link to="/shop" class="mt-4 inline-block text-gold-500 hover:underline">Browse all products</router-link>
  </div>
</template>
