<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOsimartCart } from '../composables/useOsimartCart'
import { useFavorites } from '../composables/useFavorites'
import { useTheme } from '../composables/useTheme'
import { useUser } from '../composables/useUser'
import { resolveImage } from '../utils/images'
import CartDrawer from './CartDrawer.vue'
import OptimizedImage from './OptimizedImage.vue'

const route = useRoute()
const router = useRouter()
const { totalItems, init: initCart } = useOsimartCart()
const { init: initFavs } = useFavorites()
const { isDark, toggle: toggleTheme } = useTheme()
const { user, isAuthenticated, isStaff, refresh, logout } = useUser()

onMounted(async () => {
  await refresh()
  if (user.value) {
    await Promise.allSettled([initCart(), initFavs()])
  }
})

async function handleLogout() {
  await logout()
  if (route.path !== '/') router.push('/')
}

function themedToggle() {
  document.documentElement.classList.add('theme-transitioning')
  setTimeout(() => document.documentElement.classList.remove('theme-transitioning'), 400)
  toggleTheme()
}

const cartOpen = ref(false)
const mobileMenuOpen = ref(false)
const searchQuery = ref('')
const searchFocused = ref(false)

const searchResults = ref({ grouped: {}, total: 0 })
let searchTimer = null

watch(searchQuery, (val) => {
  clearTimeout(searchTimer)
  if (!val.trim()) {
    searchResults.value = { grouped: {}, total: 0 }
    return
  }
  searchTimer = setTimeout(async () => {
    try {
      const { api } = await import('../utils/api')
      const res = await api.osimart.products({ search: val, limit: 12 })
      const items = Array.isArray(res) ? res : (res?.results || [])
      const grouped = {}
      items.forEach(p => {
        const cat = p.categories?.[0]?.category?.slugified_name || 'other'
        if (!grouped[cat]) grouped[cat] = []
        if (grouped[cat].length < 4) {
          grouped[cat].push({
            id: p.slugified_name || p.id,
            name: p.name,
            price: parseFloat(p.price_range || '0'),
            image: resolveImage(p.main_image),
          })
        }
      })
      searchResults.value = { grouped, total: items.length }
    } catch {
      searchResults.value = { grouped: {}, total: 0 }
    }
  }, 300)
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
    class="sticky top-0 z-40 bg-dark-bg/80 border-b border-charcoal-700"
    role="banner"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between h-16 gap-4">

        <!-- Logo -->
        <router-link
          to="/"
          class="font-display text-xl font-bold text-gold-400 tracking-wide shrink-0 hover:text-gold-300 transition-colors"
          aria-label="Golden Glow Home"
        >
          Golden Glow
        </router-link>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center gap-1" aria-label="Main navigation">
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            :class="[
              'px-3 py-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-gold-400',
              route.path === link.path
                ? 'text-gold-400 bg-gold-500/15'
                : 'text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50'
            ]"
          >
            {{ link.label }}
          </router-link>
          <router-link
            v-if="isAuthenticated()"
            to="/dashboard"
            class="px-3 py-2 rounded-md text-sm font-medium transition-colors text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50 flex items-center gap-1"
          >
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
            Dashboard
          </router-link>
        </nav>

        <!-- Search + Cart + Mobile Toggle -->
        <div class="flex items-center gap-3">

          <!-- Search (desktop) -->
          <div class="hidden sm:relative sm:block" role="search">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-40 lg:w-56 bg-charcoal-700 border border-charcoal-600 rounded-md px-3 py-1.5 text-sm text-dark-text placeholder-charcoal-500 focus:outline-none focus:ring-2 focus:ring-gold-400 focus:border-transparent transition-all"
              @focus="searchFocused = true"
              @blur="closeSearch"
              @keydown.enter="searchQuery.trim() && (router.push('/shop?q=' + encodeURIComponent(searchQuery.trim())), searchQuery = '', searchFocused = false)"
              aria-label="Search products"
              autocomplete="off"
            >
            <div
              v-if="searchFocused && searchResults.total > 0"
              class="absolute top-full mt-1 left-0 right-0 bg-dark-card border border-charcoal-600 rounded-md shadow-xl overflow-y-auto max-h-96 z-50"
            >
              <div v-for="(items, category) in searchResults.grouped" :key="category">
                <p class="px-3 pt-2 pb-1 text-[10px] font-bold text-charcoal-500 uppercase tracking-widest">{{ category }}</p>
                <router-link
                  v-for="result in items"
                  :key="result.id"
                  :to="`/product/${result.id}`"
                  class="flex items-center gap-3 px-3 py-2 hover:bg-charcoal-700 transition-colors text-sm"
                  @click="searchQuery = ''; searchFocused = false"
                >
                  <div class="w-8 h-8 rounded shrink-0 overflow-hidden">
                    <OptimizedImage :src="result.image" :alt="result.name" wrapperClass="h-full w-full rounded" />
                  </div>
                  <div class="min-w-0">
                    <p class="text-dark-text truncate">{{ result.name }}</p>
                    <p class="text-gold-400 text-xs">${{ Number(result.price || 0).toFixed(2) }}</p>
                  </div>
                </router-link>
              </div>
              <p class="px-3 py-2 text-xs text-charcoal-500 border-t border-charcoal-700">{{ searchResults.total }} result{{ searchResults.total !== 1 ? 's' : '' }} — press Enter to search all</p>
            </div>
          </div>

          <!-- Profile / Auth -->
          <router-link
            v-if="isAuthenticated()"
            to="/profile"
            class="hidden md:inline-flex text-sm font-medium items-center gap-1 text-charcoal-600 hover:text-gold-400 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            Profile
          </router-link>
          <router-link
            v-if="isAuthenticated()"
            to="/orders"
            class="hidden md:inline-flex text-sm font-medium items-center gap-1 text-charcoal-600 hover:text-gold-400 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            Orders
          </router-link>
          <button
            v-if="isAuthenticated()"
            @click="handleLogout"
            class="hidden md:inline-flex text-sm font-medium text-rose-400 hover:text-rose-300 hover:bg-rose-500/15 px-3 py-1.5 rounded-md transition-colors cursor-pointer"
          >
            Logout
          </button>
          <template v-if="!isAuthenticated()">
            <router-link
              to="/guest-login"
              class="hidden md:inline-flex text-sm font-medium text-charcoal-500 hover:text-gold-400 transition-colors"
            >
              Guest
            </router-link>
            <router-link
              to="/login"
              class="hidden md:inline-flex text-sm font-medium text-gold-400 hover:text-gold-300 transition-colors"
            >
              Sign In
            </router-link>
            <router-link
              to="/staff-login"
              class="hidden md:inline-flex text-sm font-medium text-charcoal-500 hover:text-gold-400 transition-colors"
            >
              Staff
            </router-link>
          </template>

          <!-- Theme toggle -->
          <button
            @click="themedToggle"
            class="p-2 text-charcoal-600 hover:text-gold-400 transition-colors"
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
          <button
            @click="cartOpen = true"
            class="relative p-2 text-charcoal-600 hover:text-gold-400 transition-colors"
            aria-label="Open cart"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z" />
            </svg>
            <span
              v-if="totalItems > 0"
              class="absolute -top-0.5 -right-0.5 bg-emerald-500 text-dark-bg text-[10px] font-bold rounded-full h-4 min-w-[16px] flex items-center justify-center px-1 badge-bounce"
              aria-live="polite"
            >
              {{ totalItems }}
            </span>
          </button>

          <!-- Mobile menu toggle -->
          <button
            class="md:hidden p-2 text-charcoal-600 hover:text-dark-text transition-colors"
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
      <nav v-if="mobileMenuOpen" class="md:hidden border-t border-charcoal-700 bg-dark-bg overflow-hidden" aria-label="Mobile navigation">
        <div class="px-4 py-3 space-y-1">
          <!-- Mobile search -->
          <div class="sm:hidden mb-2">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-full bg-charcoal-700 border border-charcoal-600 rounded-md px-3 py-2 text-sm text-dark-text placeholder-charcoal-500 focus:outline-none focus:ring-2 focus:ring-gold-400"
              @keydown.enter="searchQuery.trim() && (router.push('/shop?q=' + encodeURIComponent(searchQuery.trim())), searchQuery = '', mobileMenuOpen = false)"
              aria-label="Search products"
              autocomplete="off"
            >
          </div>
          <router-link
            v-for="link in navLinks"
            :key="link.path"
            :to="link.path"
            :class="[
              'block px-3 py-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-gold-400',
              route.path === link.path
                ? 'text-gold-400 bg-gold-500/15'
                : 'text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50'
            ]"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </router-link>
          <hr class="border-charcoal-700 my-2">
          <router-link
            v-if="isAuthenticated()"
            to="/dashboard"
            class="block px-3 py-2 rounded-md text-sm font-medium text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50 transition-colors"
            @click="mobileMenuOpen = false"
          >
            Dashboard
          </router-link>
          <template v-if="isAuthenticated()">
            <router-link
              to="/profile"
              class="block px-3 py-2 rounded-md text-sm font-medium text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50 transition-colors"
              @click="mobileMenuOpen = false"
            >
              Profile
            </router-link>
            <router-link
              to="/orders"
              class="block px-3 py-2 rounded-md text-sm font-medium text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50 transition-colors"
              @click="mobileMenuOpen = false"
            >
              Orders
            </router-link>
            <button
              @click="handleLogout; mobileMenuOpen = false"
              class="block w-full text-left px-3 py-2 rounded-md text-sm font-medium text-rose-400 hover:text-rose-300 hover:bg-rose-500/15 transition-colors cursor-pointer"
              aria-label="Logout"
            >
              Logout
            </button>
          </template>
          <template v-if="!isAuthenticated()">
            <router-link
              to="/guest-login"
              class="block px-3 py-2 rounded-md text-sm font-medium text-charcoal-600 hover:text-dark-text hover:bg-charcoal-700/50 transition-colors"
              @click="mobileMenuOpen = false"
            >
              Guest
            </router-link>
            <router-link
              to="/login"
              class="block px-3 py-2 rounded-md text-sm font-medium text-gold-400 hover:text-gold-300 transition-colors"
              @click="mobileMenuOpen = false"
            >
              Sign In
            </router-link>
            <router-link
              to="/staff-login"
              class="block px-3 py-2 rounded-md text-sm font-medium text-charcoal-500 hover:text-gold-400 transition-colors"
              @click="mobileMenuOpen = false"
            >
              Staff Login
            </router-link>
          </template>
        </div>
      </nav>
    </transition>

    <CartDrawer v-model:open="cartOpen" />
  </header>
</template>
