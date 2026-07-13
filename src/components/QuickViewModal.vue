<script setup>
import { computed } from 'vue'
import { useOsimartCart } from '../composables/useOsimartCart'
import OptimizedImage from './OptimizedImage.vue'

const props = defineProps({
  product: { type: Object, default: null }
})

const emit = defineEmits(['close'])

const { addItem, isInCart } = useOsimartCart()
const quantity = ref(1)
const modalRef = ref(null)
const previousFocus = ref(null)

import { ref, watch, nextTick } from 'vue'

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

async function handleAddToCart() {
  if (!props.product) return
  await addItem({ id: props.product.id, uuid: props.product.uuid, variantId: props.product.variantId, name: props.product.name, price: props.product.price, image: props.product.image }, quantity.value)
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
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
        @click="handleBackdropClick"
        @keydown="handleKeydown"
      >
        <div
          ref="modalRef"
          role="dialog"
          aria-modal="true"
          :aria-label="`Quick view: ${product.name}`"
          tabindex="-1"
          class="bg-surface-850 rounded-2xl border border-surface-700 w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-elevated focus:outline-none"
          @click.stop
        >
          <!-- Close button -->
          <button
            @click="onClose"
            class="absolute top-3 right-3 z-10 p-2 rounded-xl bg-surface-800/90 text-surface-400 hover:text-surface-100 hover:bg-surface-700 transition-colors"
            aria-label="Close quick view"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>

          <div class="grid md:grid-cols-2 gap-0">
            <!-- Image -->
            <div class="bg-surface-900 flex items-center justify-center p-6 min-h-[250px] relative rounded-t-2xl md:rounded-l-2xl md:rounded-tr-none">
              <OptimizedImage :src="product.image" :alt="product.name" wrapperClass="w-full h-full max-h-[300px]" imgClass="object-contain" />
              <div
                v-if="isInCart(product.uuid || product.id)"
                class="absolute top-2.5 right-2.5 bg-success-500 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg shadow-lg flex items-center gap-1"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                In Cart
              </div>
            </div>

            <!-- Details -->
            <div class="p-6 flex flex-col">
              <span class="text-xs font-mono text-gold-500 uppercase tracking-wider bg-gold-500/10 px-2.5 py-1 rounded-lg self-start">{{ product.category }}</span>
              <h2 class="text-xl font-display font-bold text-surface-50 mt-3">{{ product.name }}</h2>

              <div class="flex items-center gap-2 mt-2">
                <span class="text-warn-400 text-sm" aria-hidden="true">{{ '★'.repeat(Math.floor(product.rating)) }}{{ '☆'.repeat(5 - Math.floor(product.rating)) }}</span>
                <span class="text-xs text-surface-500">{{ product.rating }}</span>
              </div>

              <p class="text-surface-400 text-sm mt-4 leading-relaxed">{{ product.description }}</p>

              <div class="mt-4">
                <h3 class="text-sm font-semibold text-surface-300 mb-2">Specifications</h3>
                <ul class="space-y-1.5">
                  <li v-for="spec in product.specs" :key="spec" class="text-xs text-surface-400 font-mono flex items-center gap-2">
                    <span class="w-1 h-1 rounded-full bg-gold-500 shrink-0"></span>
                    {{ spec }}
                  </li>
                </ul>
              </div>

              <div class="mt-auto pt-4 border-t border-surface-700">
                <div class="text-2xl font-bold text-gold-500 font-mono">${{ Number(product.price || 0).toFixed(2) }}</div>

                <div class="flex items-center gap-3 mt-3">
                  <div class="flex items-center gap-2">
                    <button
                      @click="quantity > 1 && quantity--"
                      class="w-8 h-8 rounded-lg bg-surface-700 text-surface-300 hover:bg-surface-600 transition-colors flex items-center justify-center text-sm font-bold"
                      aria-label="Decrease quantity"
                    >−</button>
                    <span class="w-8 text-center text-sm font-mono text-surface-200">{{ quantity }}</span>
                    <button
                      @click="quantity++"
                      class="w-8 h-8 rounded-lg bg-surface-700 text-surface-300 hover:bg-surface-600 transition-colors flex items-center justify-center text-sm font-bold"
                      aria-label="Increase quantity"
                    >+</button>
                  </div>
                  <button
                    v-if="!isInCart(product.uuid || product.id)"
                    @click="handleAddToCart"
                    class="flex-1 bg-gold-500 hover:bg-gold-400 text-surface-950 py-2.5 rounded-xl text-sm font-semibold transition-all active:scale-95"
                  >
                    Add to Cart
                  </button>
                  <button
                    v-else
                    disabled
                    class="flex-1 bg-success-600 text-white py-2.5 rounded-xl text-sm font-semibold cursor-default flex items-center justify-center gap-2"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                    In Cart
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
