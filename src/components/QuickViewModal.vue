<script setup>
/**
 * Quick View modal that shows product details, specs, and add-to-cart.
 * Uses Teleport to body, includes keyboard focus trap and Escape-to-close.
 *
 * @component
 * @prop {Object|null} product - The product to display (null = hidden)
 * @emit {void} close - Emitted when modal is dismissed
 */
import { ref, watch, nextTick } from 'vue'
import { useCart } from '../composables/useCart'

const props = defineProps({
  product: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const { addItem } = useCart()
const quantity = ref(1)
const modalRef = ref(null)
const previousFocus = ref(null)

watch(() => props.product, async (val) => {
  if (val) {
    quantity.value = 1
    previousFocus.value = document.activeElement
    await nextTick()
    modalRef.value?.focus()
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

function onClose() {
  document.body.style.overflow = ''
  emit('close')
  previousFocus.value?.focus()
}

function handleKeydown(e) {
  if (e.key === 'Escape') onClose()
  if (e.key === 'Tab') trapFocus(e)
}

function trapFocus(e) {
  if (!modalRef.value) return
  const focusable = modalRef.value.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  if (focusable.length === 0) return
  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  if (e.shiftKey && document.activeElement === first) {
    e.preventDefault()
    last.focus()
  } else if (!e.shiftKey && document.activeElement === last) {
    e.preventDefault()
    first.focus()
  }
}

function handleBackdropClick(e) {
  if (e.target === e.currentTarget) onClose()
}

function handleAddToCart() {
  if (!props.product) return
  addItem({ id: props.product.id, uuid: props.product.uuid, variantId: props.product.variantId, name: props.product.name, price: props.product.price }, quantity.value)
  quantity.value = 1
}
</script>

<template>
  <Teleport to="body">
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="product"
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm"
        @click="handleBackdropClick"
        @keydown="handleKeydown"
      >
        <div
          ref="modalRef"
          role="dialog"
          aria-modal="true"
          :aria-label="`Quick view: ${product.name}`"
          tabindex="-1"
          class="bg-slate-900 rounded-xl border border-slate-700 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl shadow-cyan-950/30 focus:outline-none"
          @click.stop
        >
          <!-- Close button -->
          <button
            @click="onClose"
            class="absolute top-3 right-3 z-10 p-1.5 rounded-md bg-slate-800/80 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors"
            aria-label="Close quick view"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>

          <div class="grid md:grid-cols-2 gap-0">
            <!-- Image -->
            <div class="bg-slate-800 flex items-center justify-center p-6 min-h-[250px]">
              <img :src="product.image" :alt="product.name" loading="lazy" class="w-full h-full object-contain max-h-[300px]">
            </div>

            <!-- Details -->
            <div class="p-6 flex flex-col">
              <span class="text-xs font-mono text-cyan-500 uppercase tracking-wider bg-cyan-950/30 px-2 py-1 rounded self-start">{{ product.category }}</span>
              <h2 class="text-xl font-bold text-white mt-2">{{ product.name }}</h2>

              <div class="flex items-center gap-2 mt-2">
                <span class="text-yellow-400 text-sm" aria-hidden="true">{{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}</span>
                <span class="text-xs text-slate-500">{{ product.rating }}</span>
              </div>

              <p class="text-slate-400 text-sm mt-4 leading-relaxed">{{ product.description }}</p>

              <div class="mt-4">
                <h3 class="text-sm font-semibold text-slate-300 mb-2">Specifications</h3>
                <ul class="space-y-1.5">
                  <li v-for="spec in product.specs" :key="spec" class="text-xs text-slate-400 font-mono flex items-center gap-2">
                    <span class="w-1 h-1 rounded-full bg-cyan-500 shrink-0"></span>
                    {{ spec }}
                  </li>
                </ul>
              </div>

              <div class="mt-auto pt-4 border-t border-slate-800">
                <div class="text-2xl font-bold text-cyan-400 font-mono">${{ product.price.toFixed(2) }}</div>

                <div class="flex items-center gap-3 mt-3">
                  <div class="flex items-center gap-2">
                    <button
                      @click="quantity > 1 && quantity--"
                      class="w-8 h-8 rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors flex items-center justify-center text-sm font-bold"
                      aria-label="Decrease quantity"
                    >-</button>
                    <span class="w-8 text-center text-sm font-mono">{{ quantity }}</span>
                    <button
                      @click="quantity++"
                      class="w-8 h-8 rounded-md bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors flex items-center justify-center text-sm font-bold"
                      aria-label="Increase quantity"
                    >+</button>
                  </div>
                  <button
                    @click="handleAddToCart"
                    class="flex-1 bg-cyan-600 hover:bg-cyan-500 text-white py-2.5 rounded-lg text-sm font-semibold transition-all active:scale-95"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>
