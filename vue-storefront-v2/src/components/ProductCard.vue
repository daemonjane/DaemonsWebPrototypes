<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCart } from '../composables/useCart'

const props = defineProps({
  product: { type: Object, required: true },
  showFull: { type: Boolean, default: false }
})

const { addItem } = useCart()
const router = useRouter()
const quantity = ref(1)

function increment() { quantity.value++ }
function decrement() { if (quantity.value > 1) quantity.value-- }

function handleAddToCart() {
  addItem({ id: props.product.id, name: props.product.name, price: props.product.price }, quantity.value)
  quantity.value = 1
}

function navigateToProduct() {
  router.push(`/product/${props.product.id}`)
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
    <router-link :to="`/product/${product.id}`" class="block h-48 w-full bg-slate-800 overflow-hidden" @click.stop>
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
        loading="lazy"
      />
    </router-link>

    <div class="p-5 flex flex-col flex-1">
      <div class="flex justify-between items-start">
        <h3 class="text-lg font-bold text-white leading-snug">{{ product.name }}</h3>
        <div class="star-rating text-yellow-400 text-sm whitespace-nowrap ml-2" aria-hidden="true">
          {{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}
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
          <button
            @click.stop="handleAddToCart"
            class="bg-cyan-600 text-white px-4 py-1.5 rounded-md text-sm font-semibold hover:bg-cyan-500 transition-colors"
          >
            Add to Cart
          </button>
        </div>
      </div>

      <!-- Compact add-to-cart (other pages) -->
      <div v-else class="mt-auto pt-4 border-t border-slate-800 flex items-center justify-between">
        <span class="text-lg font-bold text-white">${{ product.price.toFixed(2) }}</span>
        <button
          @click.stop="handleAddToCart"
          class="bg-cyan-600 text-white px-4 py-2 rounded-md text-sm font-semibold hover:bg-cyan-500 active:scale-95 transition-all"
        >
          Add to Cart
        </button>
      </div>
    </div>
  </div>
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