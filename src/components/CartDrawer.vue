<script setup>
import { computed } from 'vue'
import { useOsimartCart } from '../composables/useOsimartCart'
import OptimizedImage from './OptimizedImage.vue'

defineProps({ open: Boolean })
const emit = defineEmits(['close', 'update:open'])
const { cart, totalItems, totalPrice, updateQuantity, removeItem } = useOsimartCart()

function close() { emit('update:open', false) }
</script>

<template>
  <Teleport to="body">
    <transition name="drawer-backdrop">
      <div v-if="open" class="fixed inset-0 z-50 bg-surface-950/60 backdrop-blur-sm" @click="close" @keydown.escape="close"></div>
    </transition>
    <transition name="drawer-panel">
      <div v-if="open" class="fixed top-0 right-0 z-50 h-full w-full max-w-md bg-surface-900 border-l border-surface-750 shadow-elevated flex flex-col" role="dialog" aria-modal="true" aria-label="Shopping cart">
        <div class="flex items-center justify-between px-5 py-4 border-b border-surface-750">
          <h2 class="text-lg font-display font-semibold text-surface-50 flex items-center gap-2">
            <svg class="w-5 h-5 text-gold-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
            </svg>
            Cart <span class="text-surface-500 font-normal badge-bounce">({{ totalItems }})</span>
          </h2>
          <button @click="close" class="p-2 text-surface-400 hover:text-surface-100 hover:bg-surface-800 rounded-xl transition-colors" aria-label="Close cart">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <div v-if="cart.length === 0" class="flex-1 flex flex-col items-center justify-center text-surface-500 px-6 text-center">
          <svg class="w-16 h-16 mb-4 text-surface-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
          </svg>
          <p class="text-sm font-medium">Your cart is empty</p>
          <p class="text-xs mt-1">Add some gear to get started.</p>
          <button @click="close" class="mt-4 text-sm text-gold-500 hover:text-gold-400 font-medium transition-colors">Continue Shopping →</button>
        </div>

        <div v-else class="flex-1 overflow-y-auto px-5 py-4 space-y-3">
          <div v-for="item in cart" :key="item.id" class="group flex gap-3 bg-surface-800/60 rounded-xl p-3 border border-surface-700/80 hover:border-surface-600 transition-colors">
            <div class="w-16 h-16 shrink-0 rounded-lg overflow-hidden bg-surface-850">
              <OptimizedImage :src="item.image" :alt="item.name" wrapperClass="h-full w-full rounded-lg" />
            </div>
            <div class="flex-1 min-w-0 space-y-1">
              <p class="text-sm text-surface-100 font-medium truncate">{{ item.name }}</p>
              <p class="text-gold-500 text-sm font-mono price-glow">${{ (Number(item.price || 0) * (item.quantity || 0)).toFixed(2) }}</p>
              <div class="flex items-center gap-2 pt-1">
                <button @click="updateQuantity(item.id, -1)" class="w-7 h-7 flex items-center justify-center rounded-lg bg-surface-700 text-surface-400 hover:text-surface-100 hover:bg-surface-600 transition-colors text-sm font-medium" aria-label="Decrease quantity">−</button>
                <span class="text-sm text-surface-200 font-mono min-w-[1.5rem] text-center" aria-live="polite">{{ item.quantity }}</span>
                <button @click="updateQuantity(item.id, 1)" class="w-7 h-7 flex items-center justify-center rounded-lg bg-surface-700 text-surface-400 hover:text-surface-100 hover:bg-surface-600 transition-colors text-sm font-medium" aria-label="Increase quantity">+</button>
              </div>
            </div>
            <button @click="removeItem(item.id)" class="self-start p-1 text-surface-500 hover:text-danger-400 opacity-0 group-hover:opacity-100 transition-all" :aria-label="'Remove ' + item.name + ' from cart'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>

        <div v-if="cart.length > 0" class="border-t border-surface-750 px-5 py-4 space-y-3">
          <div class="flex items-center justify-between text-sm">
            <span class="text-surface-400">Subtotal</span>
            <span class="text-surface-100 font-semibold font-mono">${{ Number(totalPrice || 0).toFixed(2) }}</span>
          </div>
          <router-link to="/checkout" @click="close" class="block w-full text-center bg-gold-500 text-surface-950 py-3 rounded-xl font-semibold hover:bg-gold-400 active:scale-[0.98] transition-all duration-150 shadow-glow-gold">
            View Cart & Checkout
          </router-link>
          <button @click="close" class="block w-full text-center text-sm text-surface-400 hover:text-surface-200 py-2 transition-colors">
            Continue Shopping
          </button>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<style scoped>
.drawer-backdrop-enter-active { transition: opacity 0.25s ease-out; }
.drawer-backdrop-leave-active { transition: opacity 0.2s ease-in; }
.drawer-backdrop-enter-from { opacity: 0; }
.drawer-backdrop-leave-to { opacity: 0; }

.drawer-panel-enter-active { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.drawer-panel-leave-active { transition: transform 0.2s ease-in; }
.drawer-panel-enter-from { transform: translateX(100%); }
.drawer-panel-leave-to { transform: translateX(100%); }
</style>
