<script setup>
import { ref } from 'vue'
import { useCart } from '../composables/useCart'

const { cart, totalItems, totalPrice, updateQuantity, removeItem } = useCart()
const mobileMenuOpen = ref(false)
const cartDropdownOpen = ref(false)

function toggleMobileMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

function closeMobileMenu() {
  mobileMenuOpen.value = false
}

function toggleCartDropdown() {
  cartDropdownOpen.value = !cartDropdownOpen.value
}

function closeCartDropdown() {
  cartDropdownOpen.value = false
}
</script>

<template>
  <header id="main-header" class="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/75 backdrop-blur-md">
    <div class="grid grid-cols-1 lg:grid-cols-3 items-center gap-4 px-4 sm:px-6 py-4 max-w-7xl mx-auto">
      <!-- Brand & mobile toggle -->
      <div class="flex items-center justify-between">
        <router-link to="/" id="brand-logo" class="text-cyan-400 font-bold text-xl sm:text-2xl tracking-widest select-none">TECHSTORE</router-link>
        <button @click="toggleMobileMenu" class="lg:hidden text-slate-400 hover:text-cyan-400 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 rounded p-1"
                aria-label="Toggle navigation menu" :aria-expanded="mobileMenuOpen">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <!-- Search -->
      <div id="header-search" class="flex items-center justify-start lg:justify-center gap-2 w-full">
        <label for="catalog-search" class="text-sm text-slate-400 hidden sm:inline shrink-0">Find Gear:</label>
        <input type="text" id="catalog-search" list="hardware-suggestions" placeholder="Search components..."
               class="w-full max-w-md mx-auto lg:max-w-xs bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 focus-visible:border-cyan-400 transition-colors">
        <datalist id="hardware-suggestions">
            <option value="Vanguard Prebuilt Rig"></option>
            <option value="RTX 5070 Graphics Card"></option>
            <option value="Cyber-Pro Keyboard"></option>
            <option value="QD-OLED Ultrawide Panel"></option>
            <option value="Thermal Matrix Compound"></option>
        </datalist>
      </div>

      <!-- Desktop nav -->
      <nav :class="['lg:flex flex-wrap lg:justify-end gap-5 text-sm font-medium w-full', mobileMenuOpen ? 'flex flex-col absolute top-full left-0 w-full bg-slate-900 p-4 border-t border-slate-800 space-y-3 z-40' : 'hidden']"
           role="navigation" aria-label="Main navigation">
        <router-link to="/" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded">Home</router-link>
        <router-link to="/shop" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded">Shop</router-link>
        <router-link to="/contact" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded">Contact</router-link>
        <router-link to="/about" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded">About</router-link>
        <router-link to="/insights" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded">Insights</router-link>

        <!-- Cart trigger -->
        <div class="relative inline-flex items-center">
          <button @click.stop="toggleCartDropdown" class="text-cyan-400 font-semibold relative pr-2 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 rounded"
                  :aria-expanded="cartDropdownOpen" aria-label="Shopping cart" aria-haspopup="true">
            Cart
            <span v-if="totalItems > 0" class="absolute -top-1 -right-2 bg-cyan-500 text-black text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-bold">
              {{ totalItems }}
            </span>
          </button>

          <!-- Cart dropdown -->
          <div v-if="cartDropdownOpen" class="absolute right-0 top-full mt-1 w-80 bg-slate-900 border border-slate-700 rounded-lg shadow-2xl p-4 z-50 space-y-3">
            <h3 class="text-sm font-semibold text-slate-300 uppercase tracking-wider">Your Cart</h3>
            <ul v-if="cart.length > 0" class="space-y-2 max-h-48 overflow-y-auto text-sm">
              <li v-for="item in cart" :key="item.id" class="flex flex-col gap-1 border-b border-slate-700 pb-2">
                <div class="flex justify-between items-center">
                  <span class="font-medium">{{ item.name }}</span>
                  <span class="text-cyan-400">${{ (item.price * item.quantity).toFixed(2) }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <button @click.stop="updateQuantity(item.id, -1)" class="bg-slate-700 px-2 rounded text-xs">-</button>
                    <span class="text-xs">{{ item.quantity }}</span>
                    <button @click.stop="updateQuantity(item.id, 1)" class="bg-slate-700 px-2 rounded text-xs">+</button>
                  </div>
                  <button @click.stop="removeItem(item.id)" class="text-red-400 text-xs">Remove</button>
                </div>
              </li>
            </ul>
            <p v-else class="text-slate-500 text-sm">Your cart is empty.</p>
            <div class="flex items-center justify-between border-t border-slate-700 pt-2">
              <span class="text-slate-400 text-xs">Total:</span>
              <span class="text-cyan-400 font-bold text-lg">${{ totalPrice.toFixed(2) }}</span>
            </div>
            <router-link to="/checkout" @click="closeCartDropdown" class="block w-full bg-cyan-600 text-white py-2 rounded-md text-sm font-semibold text-center hover:bg-cyan-500 transition-colors">
              Checkout
            </router-link>
          </div>
        </div>

        <router-link to="/login" @click="closeMobileMenu" class="text-slate-400 hover:text-cyan-400 transition-colors">Login</router-link>
      </nav>
    </div>

    <!-- Backdrop to close cart when clicking outside -->
    <div v-if="cartDropdownOpen" class="fixed inset-0 z-30" @click="closeCartDropdown"></div>
  </header>
</template>