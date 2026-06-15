<script setup>
/**
 * Site-wide navigation header.
 * Includes: logo, desktop + mobile nav, global search with dropdown, cart badge with count.
 * @component
 */
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCart } from '../composables/useCart'
import { useTheme } from '../composables/useTheme'
import { products } from '../data/products'

const route = useRoute()
const { totalItems } = useCart()
const { isDark, toggle: toggleTheme } = useTheme()

const mobileMenuOpen = ref(false)
const searchQuery = ref('')
const searchFocused = ref(false)

const searchResults = computed(() => {
  if (!searchQuery.value.trim()) return []
  const q = searchQuery.value.toLowerCase()
  return products
    .filter(p => p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q))
    .slice(0, 5)
})

const navLinks = [
  { path: '/', label: 'Home' },
  { path: '/shop', label: 'Shop' },
  { path: '/favorites', label: 'Favorites' },
  { path: '/insights', label: 'Insights' },
  { path: '/faq', label: 'FAQ' },
  { path: '/about', label: 'About' },
  { path: '/contact', label: 'Contact' },
]

function closeSearch() {
  setTimeout(() => { searchFocused.value = false }, 200)
}
</script>

<template>
  <header
    id="main-header"
    class="sticky top-0 z-40 bg-slate-950/80 border-b border-slate-800"
    role="banner"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-16 gap-4">

        <!-- Logo -->
        <router-link
          to="/"
          class="text-lg sm:text-xl font-bold text-white tracking-tight hover:text-cyan-400 transition-colors shrink-0"
          aria-label="TechStore Home"
        >
          <span class="text-cyan-400">&lt;</span>TECH<span class="text-cyan-400">/</span>STORE<span class="text-cyan-400">&gt;</span>
        </router-link>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center gap-1" aria-label="Main navigation">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            :class="[
              'px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === link.path
                ? 'text-cyan-400 bg-cyan-950/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            ]"
          >
            {{ link.label }}
          </router-link>
        </nav>

        <!-- Search + Cart + Mobile Toggle -->
        <div class="flex items-center gap-3">

          <!-- Search (desktop) -->
          <div class="hidden sm:relative sm:block">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-40 lg:w-56 bg-slate-800 border border-slate-700 rounded-md px-3 py-1.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 focus:border-transparent transition-all"
              @focus="searchFocused = true"
              @blur="closeSearch"
              aria-label="Search products"
              autocomplete="off"
            >
            <div
              v-if="searchFocused && searchResults.length > 0"
              class="absolute top-full mt-1 left-0 right-0 bg-slate-900 border border-slate-700 rounded-md shadow-xl overflow-hidden z-50"
            >
              <router-link
                v-for="result in searchResults"
                :key="result.id"
                :to="`/product/${result.id}`"
                class="flex items-center gap-3 px-3 py-2 hover:bg-slate-800 transition-colors text-sm"
                @click="searchQuery = ''; searchFocused = false"
              >
                <div class="w-8 h-8 rounded bg-slate-700 shrink-0 overflow-hidden">
                  <img :src="result.image" :alt="result.name" loading="lazy" class="w-full h-full object-cover">
                </div>
                <div class="min-w-0">
                  <p class="text-slate-200 truncate">{{ result.name }}</p>
                  <p class="text-cyan-400 text-xs">${{ result.price.toFixed(2) }}</p>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Theme toggle -->
          <button
            @click="toggleTheme"
            class="p-2 text-slate-400 hover:text-cyan-400 transition-colors"
            :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
            :title="isDark ? 'Light mode' : 'Dark mode'"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>

          <!-- Cart -->
          <router-link
            to="/checkout"
            class="relative p-2 text-slate-400 hover:text-cyan-400 transition-colors"
            aria-label="View cart"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
            </svg>
            <span
              v-if="totalItems > 0"
              class="absolute -top-0.5 -right-0.5 bg-cyan-500 text-black text-[10px] font-bold rounded-full h-4 min-w-[16px] flex items-center justify-center px-1"
              aria-live="polite"
            >
              {{ totalItems }}
            </span>
          </router-link>

          <!-- Mobile menu toggle -->
          <button
            class="md:hidden p-2 text-slate-400 hover:text-white transition-colors"
            @click="mobileMenuOpen = !mobileMenuOpen"
            :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
            :aria-expanded="mobileMenuOpen"
          >
            <svg v-if="!mobileMenuOpen" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition
      enter-active-class="transition-all duration-200 ease-out"
      leave-active-class="transition-all duration-150 ease-in"
      enter-from-class="opacity-0 max-h-0"
      enter-to-class="opacity-100 max-h-96"
      leave-from-class="opacity-100 max-h-96"
      leave-to-class="opacity-0 max-h-0"
    >
      <nav v-if="mobileMenuOpen" class="md:hidden border-t border-slate-800 bg-slate-950 overflow-hidden" aria-label="Mobile navigation">
        <div class="px-4 py-3 space-y-1">
          <!-- Mobile search -->
          <div class="sm:hidden mb-2">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-full bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400"
              aria-label="Search products"
              autocomplete="off"
            >
          </div>
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            :class="[
              'block px-3 py-2 rounded-md text-sm font-medium transition-colors',
              route.path === link.path
                ? 'text-cyan-400 bg-cyan-950/30'
                : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
            ]"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </router-link>
        </div>
      </nav>
    </transition>
  </header>
</template>
