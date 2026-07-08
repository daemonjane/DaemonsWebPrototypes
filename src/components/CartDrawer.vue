<script setup>
import { useCart } from '../composables/useCart'
import OptimizedImage from './OptimizedImage.vue'

defineProps({ open: Boolean })
const emit = defineEmits(['close', 'update:open'])
const { cart, totalItems, totalPrice, updateQuantity, removeItem } = useCart()

function close() { emit('update:open', false) }
</script>

<template>
  <Teleport to="body">
    <transition name="drawer">
      <div v-if="open" class="fixed inset-0 z-50 flex justify-end" role="dialog" aria-modal="true" aria-label="Shopping cart">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="close" @keydown.escape="close"></div>

        <!-- Panel -->
        <div class="relative w-full max-w-md bg-slate-950 border-l border-slate-800 shadow-2xl flex flex-col h-full">
          <!-- Header -->
          <div class="flex items-center justify-between px-5 py-4 border-b border-slate-800">
            <h2 class="text-lg font-semibold text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
              </svg>
              Cart <span class="text-slate-400 font-normal">({{ totalItems }})</span>
            </h2>
            <button @click="close" class="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-md transition-colors focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Close cart">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <!-- Items -->
          <div v-if="cart.length === 0" class="flex-1 flex flex-col items-center justify-center text-slate-500 px-6 text-center">
            <svg class="w-16 h-16 mb-4 text-slate-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/>
            </svg>
            <p class="text-sm">Your cart is empty</p>
            <p class="text-xs mt-1">Add some gear to get started.</p>
            <button @click="close" class="mt-4 text-sm text-cyan-400 hover:text-cyan-300 font-medium transition-colors">Continue Shopping →</button>
          </div>

          <div v-else class="flex-1 overflow-y-auto px-5 py-4 space-y-3">
            <div v-for="item in cart" :key="item.id" class="group flex gap-3 bg-slate-900/70 rounded-lg p-3 border border-slate-800/80 hover:border-slate-700 transition-colors">
              <div class="w-16 h-16 shrink-0 rounded-md overflow-hidden">
                <OptimizedImage :src="item.image" :alt="item.name" wrapperClass="h-full w-full" />
              </div>
              <div class="flex-1 min-w-0 space-y-1">
                <p class="text-sm text-slate-200 font-medium truncate">{{ item.name }}</p>
                <p class="text-cyan-400 text-sm font-mono">${{ (Number(item.price || 0) * (item.quantity || 0)).toFixed(2) }}</p>
                <div class="flex items-center gap-2 pt-1">
                  <button @click="updateQuantity(item.id, -1)" class="w-7 h-7 flex items-center justify-center rounded bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors text-sm font-medium focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Decrease quantity">−</button>
                  <span class="text-sm text-white font-mono min-w-[1.5rem] text-center" aria-live="polite">{{ item.quantity }}</span>
                  <button @click="updateQuantity(item.id, 1)" class="w-7 h-7 flex items-center justify-center rounded bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors text-sm font-medium focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Increase quantity">+</button>
                </div>
              </div>
              <button @click="removeItem(item.id)" class="self-start p-1 text-slate-600 hover:text-pink-400 opacity-0 group-hover:opacity-100 transition-all focus-visible:opacity-100 focus-visible:outline-2 focus-visible:outline-cyan-400" aria-label="Remove {{ item.name }} from cart">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </div>
          </div>

          <!-- Footer -->
          <div v-if="cart.length > 0" class="border-t border-slate-800 px-5 py-4 space-y-3">
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-400">Subtotal</span>
              <span class="text-white font-semibold font-mono">${{ Number(totalPrice || 0).toFixed(2) }}</span>
            </div>
            <router-link
              to="/checkout"
              @click="close"
              class="block w-full text-center bg-cyan-600 text-white py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-[0.98] transition-all duration-150 focus-visible:outline-2 focus-visible:outline-cyan-400"
            >
              View Cart & Checkout
            </router-link>
            <button @click="close" class="block w-full text-center text-sm text-slate-400 hover:text-white py-2 transition-colors focus-visible:outline-2 focus-visible:outline-cyan-400">
              Continue Shopping
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<style scoped>
.drawer-enter-active { transition: all 0.25s ease-out; }
.drawer-leave-active { transition: all 0.2s ease-in; }
.drawer-enter-from { opacity: 0; }
.drawer-leave-to { opacity: 0; }
.drawer-enter-from > div:last-child { transform: translateX(100%); }
.drawer-leave-to > div:last-child { transform: translateX(100%); }
</style>
