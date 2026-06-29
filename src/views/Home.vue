<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import AnimatedCounter from '../components/AnimatedCounter.vue'
import AbstractArt from '../components/AbstractArt.vue'
import { useCart } from '../composables/useCart'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'

const OSIMART_IMAGE_BASE = 'https://api.osimart.com'

const { addItem, addUpgrade, removeUpgrade, setMembership } = useCart()
const { items: recentlyViewed } = useRecentlyViewed()

const products = ref([])
const banners = ref([])
const hero = ref(null)
const store = ref(null)
const features = ref([])
const metrics = ref([])
const testimonials = ref([])
const categories = ref([])
const brands = ref([])
const collections = ref([])
const loading = ref(true)

const activeSlide = ref(0)
let slideTimer = null

onMounted(() => { startSlideTimer() })
onUnmounted(() => { clearInterval(slideTimer) })

function startSlideTimer() {
  slideTimer = setInterval(() => {
    if (banners.value.length) {
      activeSlide.value = (activeSlide.value + 1) % banners.value.length
    }
  }, 5000)
}

function setSlide(i) {
  activeSlide.value = i
  clearInterval(slideTimer)
  startSlideTimer()
}

watch(banners, () => {
  activeSlide.value = 0
  clearInterval(slideTimer)
  startSlideTimer()
})

function normalizeProduct(p) {
  const imgPath = p.main_image?.path
  return {
    id: p.slugified_name || p.id,
    uuid: p.id,
    name: p.name,
    category: p.categories?.[0]?.category?.slugified_name || 'uncategorized',
    price: parseFloat(p.price_range || '0'),
    image: imgPath ? `${OSIMART_IMAGE_BASE}/${imgPath}` : '/assets/placeholder.svg',
    description: stripHtml(p.description || ''),
    createdAt: p.created_at || p.date_created || null,
    rating: 4.5,
    stock: p.remaining_stock ?? p.stock ?? 0,
    specs: (p.sections || []).flatMap(s => (s.items || []).map(i => `${i.name}: ${i.value}`)),
  }
}

function stripHtml(html) {
  const d = document.createElement('div')
  d.innerHTML = html
  return d.textContent || d.innerText || ''
}

function pick(arr) {
  return Array.isArray(arr) ? arr : (arr?.results || [])
}

onMounted(async () => {
  try {
    const { api } = await import('../utils/api')
    const [prodRes, bannerRes, homeRes, storeRes, catRes, brandRes, collRes] = await Promise.allSettled([
      api.osimart.products({ limit: 50 }),
      api.osimart.banners(),
      api.osimart.home(),
      api.osimart.store(),
      api.osimart.categories(),
      api.osimart.brands(),
      api.osimart.collections(),
    ])
    if (prodRes.status === 'fulfilled') {
      const items = pick(prodRes.value)
      if (items.length > 0) {
        products.value = items.map(normalizeProduct)
      }
    }
    if (bannerRes.status === 'fulfilled') {
      banners.value = pick(bannerRes.value)
    }
    if (homeRes.status === 'fulfilled') {
      const h = homeRes.value
      if (h.hero) hero.value = h.hero
      if (h.features) features.value = Array.isArray(h.features) ? h.features : []
      if (h.metrics) metrics.value = Array.isArray(h.metrics) ? h.metrics : []
      if (h.testimonials) testimonials.value = Array.isArray(h.testimonials) ? h.testimonials : []
    }
    if (storeRes.status === 'fulfilled') {
      store.value = storeRes.value
      if (storeRes.value.metrics) {
        metrics.value = Array.isArray(storeRes.value.metrics) ? storeRes.value.metrics : []
      }
    }
    if (catRes.status === 'fulfilled') {
      categories.value = pick(catRes.value)
    }
    if (brandRes.status === 'fulfilled') {
      brands.value = pick(brandRes.value)
    }
    if (collRes.status === 'fulfilled') {
      collections.value = pick(collRes.value)
    }
  } catch (e) {
    console.error('Osimart fetch failed', e)
  } finally {
    loading.value = false
  }
})

// Countdown timer
const countdownSeconds = ref(300)
const countdownText = ref('05:00')
let intervalId = null

const upgradePrices = {
  'vip-build': 19.99,
  'laser-engraving': 14.99,
  'hardware-insurance': 2.99
}

function onUpgradeChange(event) {
  const id = event.target.id
  const name = event.target.labels?.[0]?.querySelector('strong')?.textContent?.trim() || id
  if (event.target.checked) {
    addUpgrade(id, name, upgradePrices[id])
  } else {
    removeUpgrade(id, name)
  }
}

const membershipPrices = { monthly: 9.99, annual: 79.99 }

function selectMembership(type) {
  const name = type === 'monthly' ? 'Monthly Membership' : 'Annual Membership'
  setMembership(type, name, membershipPrices[type])
}

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

onMounted(() => {
  countdownText.value = formatTime(countdownSeconds.value)
  intervalId = setInterval(() => {
    countdownSeconds.value--
    if (countdownSeconds.value <= 0) {
      countdownText.value = 'ALLOCATION EXPIRED'
      clearInterval(intervalId)
    } else {
      countdownText.value = formatTime(countdownSeconds.value)
    }
  }, 1000)
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const showMoreItems = ref(false)
const recentlyScrollRef = ref(null)

function scrollRecently(dir) {
  if (!recentlyScrollRef.value) return
  const amount = dir === 'left' ? -300 : 300
  recentlyScrollRef.value.scrollBy({ left: amount, behavior: 'smooth' })
}

// Dynamic product sections from Osimart data
const trendingProducts = computed(() => products.value.slice(0, 6))
const featuredProducts = computed(() => products.value.slice(0, 3))
const newArrivals = computed(() => {
  return [...products.value].sort((a, b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0)).slice(0, 6)
})
const otherProducts = computed(() => {
  const featuredIds = new Set(featuredProducts.value.map(p => p.id))
  const newIds = new Set(newArrivals.value.map(p => p.id))
  return products.value.filter(p => !featuredIds.has(p.id) && !newIds.has(p.id))
})

const showAllOther = ref(false)

// Bundles
const bundles = [
  { id: 'bundle-silent', name: 'Silent Operator Bundle', description: 'Vanguard Desktop + Cyber‑Pro Keyboard + Desk Mat', price: 2596, saved: 152, oldPrice: 2748 },
  { id: 'bundle-immersive', name: 'Immersive Vision Bundle', description: '34" QD‑OLED Monitor + VESA Arm + Bias Lighting Kit', price: 1299, saved: 93, oldPrice: 1392 }
]

function addBundleToCart(bundle) {
  addItem({ id: bundle.id, name: bundle.name, price: bundle.price })
}

function quickAdd(product) {
  addItem({ id: product.id, name: product.name, price: product.price })
}
</script>

<template>
  <div class="space-y-20 sm:space-y-28">
    <!-- Banners carousel -->
    <section v-if="banners.length" class="relative overflow-hidden rounded-xl" role="region" aria-label="Promotional banners">
      <div class="flex transition-transform duration-500" :style="{ transform: `translateX(-${activeSlide * 100}%)` }">
        <div v-for="(banner, i) in banners" :key="banner.id || i" class="min-w-full relative">
          <img :src="`https://api.osimart.com/${banner.image?.path || ''}`" :alt="banner.title || 'Banner'" class="w-full h-48 sm:h-72 object-cover" />
          <div v-if="banner.title" class="absolute inset-0 flex items-center justify-center bg-black/30">
            <h2 class="text-white text-2xl sm:text-4xl font-bold">{{ banner.title }}</h2>
          </div>
        </div>
      </div>
      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2" role="tablist" aria-label="Slide navigation">
        <button v-for="(banner, i) in banners" :key="i" @click="setSlide(i)" :aria-label="`Go to slide ${i + 1}`" :aria-selected="activeSlide === i" :class="['w-2.5 h-2.5 rounded-full transition-all', activeSlide === i ? 'bg-cyan-400 scale-125' : 'bg-slate-500/60 hover:bg-slate-400']"></button>
      </div>
    </section>

    <!-- Hero -->
    <section id="hero" class="relative flex flex-col items-center text-center py-12 sm:py-20 lg:py-24 overflow-hidden"
              role="region" aria-labelledby="hero-heading">
      <div class="hero-glow"></div>
      <AbstractArt variant="hero" class="absolute inset-0 w-full h-full" />
      <div class="relative max-w-3xl space-y-5 sm:space-y-7">
        <span class="inline-block bg-cyan-900/40 text-cyan-300 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider">{{ hero?.badge || 'SYSTEM_READY' }}</span>
        <h1 id="hero-heading" class="text-3xl sm:text-5xl md:text-6xl font-extrabold text-white leading-tight drop-shadow-lg">{{ hero?.title || 'Your Command Station Awaits' }}</h1>
        <p class="text-base sm:text-lg text-slate-400 max-w-xl mx-auto">{{ hero?.subtitle || 'Build the ultimate workspace from the comfort of your home. We ship the finest hardware, custom‑tuned for silence and power.' }}</p>
        <div class="flex flex-wrap justify-center gap-4 pt-4">
          <router-link :to="hero?.primary_cta?.link || '/shop'" class="bg-cyan-600 text-white px-6 sm:px-7 py-3 sm:py-3.5 rounded-md font-semibold shadow-lg shadow-cyan-900/30 hover:bg-cyan-500 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">{{ hero?.primary_cta?.label || 'Start Building' }}</router-link>
          <router-link :to="hero?.secondary_cta?.link || '/insights'" class="border border-slate-600 text-slate-300 px-6 sm:px-7 py-3 sm:py-3.5 rounded-md font-semibold hover:border-cyan-500 hover:text-cyan-400 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">{{ hero?.secondary_cta?.label || 'Explore Membership' }}</router-link>
        </div>
      </div>
    </section>

    <!-- Banners (static fallback if none from API) -->
    <section v-if="!banners.length" class="relative flex flex-col items-center text-center py-12 sm:py-16 overflow-hidden rounded-xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-800">
      <p class="text-slate-400 text-sm max-w-lg mx-auto px-4">Browse our latest collection — premium hardware sourced directly from verified vendors.</p>
    </section>

    <!-- Metrics -->
    <section id="metrics" class="grid grid-cols-2 md:grid-cols-4 gap-6 sm:gap-8 py-6" aria-label="Company metrics">
      <template v-if="metrics.length">
        <AnimatedCounter v-for="(m, i) in metrics" :key="i" :target="m.target" :suffix="m.suffix" :label="m.label" :duration="m.duration || 1800" :decimals="m.decimals" />
      </template>
      <template v-else>
        <AnimatedCounter :target="10" suffix="K+" label="Products Shipped" :duration="1800" />
        <AnimatedCounter :target="50" suffix="K+" label="Happy Customers" :duration="2000" />
        <AnimatedCounter :target="99.9" suffix="%" label="Uptime SLA" :decimals="1" :duration="2200" />
        <AnimatedCounter :target="24" suffix="/7" label="Support Response" :duration="1500" />
      </template>
    </section>

    <!-- Features -->
    <section id="features" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="features-heading">
      <h2 id="features-heading" class="text-2xl sm:text-3xl font-bold text-white text-center">{{ store?.name ? store.name + ' Features' : 'Why TechStore?' }}</h2>
      <div v-if="features.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
        <article v-for="(f, i) in features" :key="i" class="bg-slate-900 rounded-xl p-6 sm:p-7 border border-slate-800 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">{{ f.icon || '✦' }}</div>
          <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">{{ f.title }}</h3>
          <p class="text-slate-400 text-sm">{{ f.description }}</p>
        </article>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
        <article class="bg-slate-900 rounded-xl p-6 sm:p-7 border border-slate-800 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">⚡</div>
          <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Verified Performance</h3>
          <p class="text-slate-400 text-sm">Every component undergoes a 12‑hour stress test before it leaves the lab.</p>
        </article>
        <article class="bg-slate-900 rounded-xl p-6 sm:p-7 border border-slate-800 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📦</div>
          <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Direct Vendor Sourcing</h3>
          <p class="text-slate-400 text-sm">No middlemen. Authentic parts straight from the production line to your door.</p>
        </article>
        <article class="bg-slate-900 rounded-xl p-6 sm:p-7 border border-slate-800 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📊</div>
          <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Optimal Price-to-Quality</h3>
          <p class="text-slate-400 text-sm">Real‑time market analysis ensures you always get the best value per dollar.</p>
        </article>
      </div>
    </section>

    <!-- Categories -->
    <section v-if="categories.length" id="categories" class="space-y-6 sm:space-y-8" role="region" aria-labelledby="categories-heading">
      <div class="flex items-center justify-between">
        <h2 id="categories-heading" class="text-xl sm:text-2xl font-bold text-white">Shop by Category</h2>
        <router-link to="/shop" class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors">View all →</router-link>
      </div>
      <div class="flex flex-wrap gap-3">
        <router-link
          v-for="c in categories" :key="c.id || c.slugified_name"
          :to="'/shop?category=' + (c.slugified_name || c.name)"
          class="flex items-center gap-2 px-4 py-2.5 bg-slate-900 rounded-xl border border-slate-800 hover:border-cyan-700 hover:bg-slate-800/80 transition-all duration-200 group"
        >
          <span class="text-lg">{{ c.icon || '📦' }}</span>
          <span class="text-sm text-slate-300 group-hover:text-white font-medium">{{ c.name }}</span>
          <span class="text-xs text-slate-600">({{ c.product_count || c.products_count || 0 }})</span>
        </router-link>
      </div>
    </section>

    <!-- Brands -->
    <section v-if="brands.length" id="brands" class="space-y-6 sm:space-y-8" role="region" aria-labelledby="brands-heading">
      <div class="flex items-center justify-between">
        <h2 id="brands-heading" class="text-xl sm:text-2xl font-bold text-white">Featured Brands</h2>
        <router-link to="/shop" class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors">Browse all →</router-link>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <router-link
          v-for="b in brands" :key="b.id || b.slugified_name"
          :to="'/shop?brand=' + (b.slugified_name || b.name)"
          class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 hover:bg-slate-800/80 transition-all duration-200 text-center group"
        >
          <div v-if="b.logo?.path" class="h-12 flex items-center justify-center mb-2">
            <img :src="`https://api.osimart.com/${b.logo.path}`" :alt="b.name" class="max-h-full max-w-full object-contain opacity-70 group-hover:opacity-100 transition-opacity" />
          </div>
          <div v-else class="h-12 flex items-center justify-center mb-2">
            <div class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 text-lg">{{ (b.name || '?')[0] }}</div>
          </div>
          <span class="text-xs text-slate-400 group-hover:text-white font-medium block truncate">{{ b.name }}</span>
        </router-link>
      </div>
    </section>

    <!-- Collections -->
    <section v-if="collections.length" id="collections" class="space-y-6 sm:space-y-8" role="region" aria-labelledby="collections-heading">
      <div class="flex items-center justify-between">
        <h2 id="collections-heading" class="text-xl sm:text-2xl font-bold text-white">Curated Collections</h2>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="c in collections" :key="c.id || c.slugified_name"
          :to="'/shop?collection=' + (c.slugified_name || c.name)"
          class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl p-5 border border-slate-800 hover:border-cyan-700 hover:-translate-y-0.5 transition-all duration-200 group"
        >
          <h3 class="text-white font-semibold group-hover:text-cyan-400 transition-colors">{{ c.name }}</h3>
          <p v-if="c.description" class="text-xs text-slate-500 mt-1 line-clamp-2">{{ c.description }}</p>
          <p class="text-xs text-cyan-400 mt-3">View collection →</p>
        </router-link>
      </div>
    </section>

    <!-- Testimonials -->
    <section id="testimonials" class="space-y-8 sm:space-y-10" role="region" aria-labelledby="testimonials-heading">
      <h2 id="testimonials-heading" class="text-2xl sm:text-3xl font-bold text-white text-center">{{ store?.testimonials_heading || 'Trusted by Builders' }}</h2>
      <div v-if="testimonials.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="(t, i) in testimonials" :key="i" class="bg-slate-900 rounded-xl p-5 border border-slate-800 space-y-3 hover:border-slate-700 transition-all duration-300">
          <div class="flex items-center gap-2 text-yellow-400 text-sm">{{ '★★★★★'.slice(0, t.rating || 5) }}{{ '☆☆☆☆☆'.slice(0, 5 - (t.rating || 5)) }}</div>
          <p class="text-sm text-slate-400 leading-relaxed">"{{ t.text || t.content }}"</p>
          <div class="flex items-center gap-2 pt-2 border-t border-slate-800">
            <div class="w-7 h-7 rounded-full flex items-center justify-center text-cyan-400 text-xs font-mono font-bold" :class="t.initials_bg || 'bg-cyan-900/40'">{{ (t.initials || (t.name || '').split(' ').map(w => w[0]).join('').slice(0, 2) || '??') }}</div>
            <div><p class="text-xs text-white font-medium">{{ t.name }}</p><p class="text-[10px] text-slate-500">{{ t.role || 'Verified Buyer' }}</p></div>
          </div>
        </div>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-slate-900 rounded-xl p-5 border border-slate-800 space-y-3 hover:border-slate-700 transition-all duration-300">
          <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★★</div>
          <p class="text-sm text-slate-400 leading-relaxed">"The Vanguard desktop is an absolute beast. Silent, cool, and rips through 4K rendering like nothing."</p>
          <div class="flex items-center gap-2 pt-2 border-t border-slate-800">
            <div class="w-7 h-7 rounded-full bg-cyan-900/40 flex items-center justify-center text-cyan-400 text-xs font-mono font-bold">MK</div>
            <div><p class="text-xs text-white font-medium">Marcus K.</p><p class="text-[10px] text-slate-500">Verified Buyer</p></div>
          </div>
        </div>
        <div class="bg-slate-900 rounded-xl p-5 border border-slate-800 space-y-3 hover:border-slate-700 transition-all duration-300">
          <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★★</div>
          <p class="text-sm text-slate-400 leading-relaxed">"Quick shipping, well-packaged, and the QD-OLED monitor exceeded every expectation. Colors are unreal."</p>
          <div class="flex items-center gap-2 pt-2 border-t border-slate-800">
            <div class="w-7 h-7 rounded-full bg-fuchsia-900/40 flex items-center justify-center text-fuchsia-400 text-xs font-mono font-bold">SL</div>
            <div><p class="text-xs text-white font-medium">Sarah L.</p><p class="text-[10px] text-slate-500">Verified Buyer</p></div>
          </div>
        </div>
        <div class="bg-slate-900 rounded-xl p-5 border border-slate-800 space-y-3 hover:border-slate-700 transition-all duration-300 sm:col-span-2 lg:col-span-1">
          <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★☆</div>
          <p class="text-sm text-slate-400 leading-relaxed">"Great selection of components. The market insights helped me time my GPU purchase perfectly. Saved $200."</p>
          <div class="flex items-center gap-2 pt-2 border-t border-slate-800">
            <div class="w-7 h-7 rounded-full bg-emerald-900/40 flex items-center justify-center text-emerald-400 text-xs font-mono font-bold">DJ</div>
            <div><p class="text-xs text-white font-medium">Daemon J.</p><p class="text-[10px] text-slate-500">Insights Member</p></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Recently Viewed -->
    <section v-if="recentlyViewed.length > 0" id="recently-viewed" class="space-y-6 sm:space-y-8" role="region" aria-labelledby="recently-viewed-heading">
      <!-- ... (unchanged) ... -->
      <h2 id="recently-viewed-heading" class="text-lg sm:text-xl font-semibold text-white flex items-center gap-2">
        <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Recently Viewed
      </h2>
      <div class="relative group/scroll">
        <button @click="scrollRecently('left')" aria-label="Scroll left" class="absolute left-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-slate-900/90 border border-slate-700 rounded-full flex items-center justify-center text-slate-400 hover:text-cyan-400 hover:border-cyan-700 transition-all opacity-0 group-hover/scroll:opacity-100 -ml-4">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
        </button>
        <button @click="scrollRecently('right')" aria-label="Scroll right" class="absolute right-0 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-slate-900/90 border border-slate-700 rounded-full flex items-center justify-center text-slate-400 hover:text-cyan-400 hover:border-cyan-700 transition-all opacity-0 group-hover/scroll:opacity-100 -mr-4">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </button>
        <div ref="recentlyScrollRef" class="flex gap-4 overflow-x-auto pb-2 snap-x snap-mandatory scrollbar-thin scrollbar-thumb-cyan-800 scrollbar-track-slate-900">
          <router-link
            v-for="item in recentlyViewed"
            :key="item.id"
            :to="`/product/${item.id}`"
            class="flex-shrink-0 w-40 sm:w-44 bg-slate-900 rounded-lg border border-slate-800 overflow-hidden hover:border-cyan-700 hover:-translate-y-0.5 transition-all duration-200 snap-start group"
          >
            <div class="h-24 bg-slate-800 overflow-hidden">
              <img :src="item.image" :alt="item.name" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            </div>
            <div class="p-2.5 space-y-1">
              <p class="text-xs text-slate-200 truncate font-medium">{{ item.name }}</p>
              <p class="text-cyan-400 text-xs font-mono">${{ item.price.toFixed(2) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- Products (featured) -->
    <section id="products" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="products-heading">
      <div class="text-center space-y-3">
        <h2 id="products-heading" class="text-2xl sm:text-3xl font-bold text-white">Core Systems & Gear</h2>
        <p class="text-slate-400 text-sm sm:text-base flex items-center justify-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <strong>Next Verified Allocation Drop:</strong>
          <span class="text-cyan-300 font-mono" aria-live="polite">{{ countdownText }}</span>
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
        <ProductCard v-for="product in featuredProducts" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- Bundles (unchained) -->
    <section id="bundles" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="bundles-heading">
      <!-- ... unchanged ... -->
      <div class="text-center space-y-3">
        <h2 id="bundles-heading" class="text-2xl sm:text-3xl font-bold text-white">Complete Your Spacestation</h2>
        <p class="text-slate-400 max-w-xl mx-auto text-sm sm:text-base">Hand‑picked combos that save you money. Bundle pricing adjusts with demand.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl p-6 border border-slate-700 flex flex-col space-y-5 hover:border-cyan-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-900/20 transition-all duration-300">
          <div class="flex items-center gap-3">
            <span class="bg-cyan-600 text-black text-xs px-3 py-1 rounded-full font-bold">SAVE $152</span>
            <span class="text-slate-400 text-sm line-through">$2,748</span>
          </div>
          <h3 class="text-xl font-bold text-white">Silent Operator Bundle</h3>
          <p class="text-slate-400 text-sm">Vanguard Desktop + Cyber‑Pro Keyboard + Desk Mat</p>
          <div class="flex items-center gap-4">
            <span class="text-2xl sm:text-3xl font-bold text-cyan-400">$2,596</span>
            <small class="text-slate-500">One‑time purchase</small>
          </div>
          <button @click="addBundleToCart(bundles[0])" class="mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
        </div>
        <div class="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl p-6 border border-slate-700 flex flex-col space-y-5 hover:border-cyan-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-900/20 transition-all duration-300">
          <div class="flex items-center gap-3">
            <span class="bg-cyan-600 text-black text-xs px-3 py-1 rounded-full font-bold">SAVE $93</span>
            <span class="text-slate-400 text-sm line-through">$1,392</span>
          </div>
          <h3 class="text-xl font-bold text-white">Immersive Vision Bundle</h3>
          <p class="text-slate-400 text-sm">34" QD‑OLED Monitor + VESA Arm + Bias Lighting Kit</p>
          <div class="flex items-center gap-4">
            <span class="text-2xl sm:text-3xl font-bold text-cyan-400">$1,299</span>
            <small class="text-slate-500">Free shipping</small>
          </div>
          <button @click="addBundleToCart(bundles[1])" class="mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
        </div>
      </div>
    </section>

    <!-- Micro-upgrades -->
    <section id="micro-upgrades" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="upgrades-heading">
      <!-- ... unchanged ... -->
      <div class="text-center space-y-3">
        <h2 id="upgrades-heading" class="text-2xl sm:text-3xl font-bold text-white">Personalize & Protect</h2>
        <p class="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">Small add‑ons that make your rig truly yours. They're so affordable you'll want them all.</p>
      </div>
      <form id="upgrades-form" @submit.prevent>
        <fieldset class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          <legend class="sr-only">Optional hardware upgrades and services</legend>
          <!-- VIP Build -->
          <div class="relative bg-slate-900 rounded-xl p-5 border border-slate-800 flex gap-3 items-start transition-all duration-200 has-[:checked]:border-cyan-500 has-[:checked]:bg-cyan-950/20">
            <input type="checkbox" id="vip-build" value="vip-build" class="peer mt-1 h-4 w-4 rounded border-slate-700 bg-slate-800 text-cyan-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 accent-cyan-500" @change="onUpgradeChange">
            <label for="vip-build" class="space-y-2 cursor-pointer flex-1 select-none">
              <strong class="text-white block transition-colors peer-checked:text-cyan-400">Priority VIP Assembly & Test</strong>
              <p class="text-slate-400 text-sm">Skip the queue. 24‑hour build + stress test.</p>
              <span class="text-cyan-400 font-semibold text-sm">+$19.99</span>
            </label>
          </div>
          <!-- Laser Engraving -->
          <div class="relative bg-slate-900 rounded-xl p-5 border border-slate-800 flex gap-3 items-start transition-all duration-200 has-[:checked]:border-cyan-500 has-[:checked]:bg-cyan-950/20">
            <input type="checkbox" id="laser-engraving" value="laser-engraving" class="peer mt-1 h-4 w-4 rounded border-slate-700 bg-slate-800 text-cyan-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 accent-cyan-500" @change="onUpgradeChange">
            <label for="laser-engraving" class="space-y-2 cursor-pointer flex-1 select-none">
              <strong class="text-white block transition-colors peer-checked:text-cyan-400">Bespoke Laser Engraving</strong>
              <p class="text-slate-400 text-sm">Your handle etched into the chassis.</p>
              <span class="text-cyan-400 font-semibold text-sm">+$14.99</span>
              <div class="max-h-0 overflow-hidden transition-all duration-300 peer-checked:max-h-24 peer-checked:mt-3">
                <span id="custom-engraving-text-label" class="text-xs text-slate-500 font-bold block">Engraving Text:</span>
                <input type="text" id="custom-engraving-text" value="jxne" placeholder=" " required minlength="3" aria-labelledby="custom-engraving-text-label" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-slate-200 font-mono focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 [&:not(:placeholder-shown):invalid]:border-pink-500 [&:not(:placeholder-shown):invalid]:ring-pink-500/30 [&:not(:placeholder-shown):valid]:border-emerald-500 [&:not(:placeholder-shown):valid]:ring-emerald-500/30 transition-colors">
              </div>
            </label>
          </div>
          <!-- Insurance -->
          <div class="relative bg-slate-900 rounded-xl p-5 border border-slate-800 flex gap-3 items-start transition-all duration-200 has-[:checked]:border-cyan-500 has-[:checked]:bg-cyan-950/20">
            <input type="checkbox" id="hardware-insurance" value="insurance" class="peer mt-1 h-4 w-4 rounded border-slate-700 bg-slate-800 text-cyan-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 accent-cyan-500" @change="onUpgradeChange">
            <label for="hardware-insurance" class="space-y-2 cursor-pointer flex-1 select-none">
              <strong class="text-white block transition-colors peer-checked:text-cyan-400">Overvoltage Protection Plan</strong>
              <p class="text-slate-400 text-sm">12‑month accidental damage coverage.</p>
              <span class="text-cyan-400 font-semibold text-sm">+$2.99/mo</span>
            </label>
          </div>
        </fieldset>
      </form>

      <!-- Trending items -->
      <div id="impulse-checkout-counter" class="bg-slate-900 rounded-xl p-5 sm:p-6 border border-slate-800" role="group" aria-labelledby="trending-heading">
        <h3 id="trending-heading" class="text-lg sm:text-xl font-semibold text-white mb-5 flex items-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          ⚡ Trending Now!!!
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="product in trendingProducts" :key="product.uuid || product.id" class="group flex items-center justify-between bg-slate-800 rounded-lg p-3 transition-colors hover:bg-slate-700/80">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 overflow-hidden rounded bg-slate-700 shrink-0">
                <img :src="product.image" :alt="product.name" loading="lazy" class="w-full h-full object-cover transition-transform duration-500 ease-out group-hover:scale-105 group-hover:rotate-1">
              </div>
              <div>
                <span class="text-slate-200 text-sm block">{{ product.name }}</span>
                <span class="text-cyan-400 text-xs">{{ product.description }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-slate-300 text-sm font-bold">${{ product.price.toFixed(2) }}</span>
              <button @click="quickAdd(product)" class="bg-cyan-600 text-white text-xs px-3 py-1.5 rounded-md group-hover:bg-cyan-500 group-hover:shadow-md group-hover:shadow-cyan-500/30 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Quick Add</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Insights Preview (locked) -->
    <section id="insights-preview" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="insights-preview-heading">
      <!-- ... unchanged ... -->
      <div class="text-center space-y-3">
        <h2 id="insights-preview-heading" class="text-2xl sm:text-3xl font-bold text-white flex items-center justify-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          Market Pulse Preview
        </h2>
        <p class="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">Live component pricing, demand trends, and allocation forecasts — locked for members only. <br class="hidden sm:block">Subscribe to see the full data stream.</p>
      </div>
      <div class="relative group max-w-3xl mx-auto">
        <div class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/60 backdrop-blur-[2px] rounded-xl border border-dashed border-cyan-800/50 transition-all duration-300 group-hover:bg-slate-950/70">
          <span class="text-4xl mb-2">🔒</span>
          <p class="text-white font-semibold text-sm sm:text-base mb-4">Unlock Real‑Time Market Data</p>
          <router-link to="/insights" class="bg-cyan-600 text-white px-5 py-2.5 rounded-md font-semibold text-sm hover:bg-cyan-500 active:scale-95 transition-all duration-150 shadow-lg shadow-cyan-900/30 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Subscribe to Unlock →</router-link>
        </div>
        <div class="bg-slate-900 rounded-xl p-6 border border-slate-800 opacity-40 blur-sm select-none pointer-events-none">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
            <div class="space-y-1">
              <span class="text-xs text-slate-500 uppercase tracking-wider">RTX 5070 Stock</span>
              <div class="text-2xl font-mono font-bold text-cyan-400">142 <span class="text-sm text-cyan-500">▲ +12%</span></div>
            </div>
            <div class="space-y-1">
              <span class="text-xs text-slate-500 uppercase tracking-wider">Avg Price Trend</span>
              <div class="text-2xl font-mono font-bold text-emerald-400">$1,249 <span class="text-sm text-emerald-500">▼ -2.4%</span></div>
            </div>
            <div class="space-y-1">
              <span class="text-xs text-slate-500 uppercase tracking-wider">Demand Score</span>
              <div class="text-2xl font-mono font-bold text-fuchsia-400">87/100 <span class="text-sm text-fuchsia-500">HIGH</span></div>
            </div>
          </div>
          <div class="mt-6 h-16 bg-slate-800 rounded-lg flex items-center justify-center">
            <span class="text-xs text-slate-600 font-mono tracking-widest">▲ ■ ▲ ■ ▼ ▲ ■ ▼ ▼ ■ ▲ ▼ ■ ▲ ■ ▼ ▲</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Insights Membership Tiers -->
    <section id="insights-membership" class="space-y-10 sm:space-y-12" role="region" aria-labelledby="membership-heading">
      <!-- ... unchanged ... -->
      <div class="text-center space-y-3">
        <h2 id="membership-heading" class="text-2xl sm:text-3xl font-bold text-white">Insights Membership</h2>
        <p class="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">Know when to buy. Live market data, price alerts, and benchmarking tools.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 max-w-4xl mx-auto">
        <div class="bg-slate-900 rounded-xl p-6 border border-slate-800 flex flex-col space-y-4 hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg transition-all duration-300">
          <h3 class="text-lg sm:text-xl font-semibold text-white">Monthly Pass</h3>
          <p class="text-slate-400 text-sm">Perfect for a one‑time build optimization.</p>
          <span class="text-2xl sm:text-3xl font-bold text-cyan-400">$9.99<span class="text-lg font-normal text-slate-500">/mo</span></span>
          <ul class="space-y-2 text-sm text-slate-400 list-disc list-inside">
            <li>Real‑time price tracking</li>
            <li>Efficiency score tools</li>
            <li>Stock alerts</li>
          </ul>
          <button @click="selectMembership('monthly')" class="mt-auto bg-cyan-600 text-white py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150">Subscribe Monthly</button>
        </div>
        <div class="relative p-[2px] rounded-xl bg-gradient-to-br from-cyan-400 via-blue-600 to-fuchsia-500 md:scale-105 shadow-xl shadow-cyan-950/40 z-10 hover:shadow-2xl hover:shadow-cyan-900/50 transition-all duration-300">
          <div class="h-full w-full bg-slate-900 rounded-[10px] p-6 flex flex-col space-y-4 relative">
            <span class="absolute -top-3 right-4 bg-cyan-600 text-black text-xs px-3 py-1 rounded-full font-bold">BEST VALUE</span>
            <h3 class="text-lg sm:text-xl font-semibold text-white">Annual Pro</h3>
            <p class="text-slate-400 text-sm">For enthusiasts who upgrade continuously.</p>
            <span class="text-2xl sm:text-3xl font-bold text-cyan-400">$79.99<span class="text-lg font-normal text-slate-500">/yr</span></span>
            <ul class="space-y-2 text-sm text-slate-400 list-disc list-inside">
              <li>Everything in Monthly</li>
              <li>Historical price charts</li>
              <li>Priority drop alerts</li>
              <li>Save 30% vs. monthly</li>
            </ul>
            <button @click="selectMembership('annual')" class="mt-auto bg-cyan-600 text-white py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150">Subscribe Annually</button>
          </div>
        </div>
      </div>
    </section>

    <!-- New Arrivals -->
    <section id="new-arrivals" class="space-y-8 sm:space-y-10" role="region" aria-labelledby="new-arrivals-heading">
      <div class="text-center space-y-3">
        <span class="inline-block bg-emerald-900/40 text-emerald-300 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider">Just Landed</span>
        <h2 id="new-arrivals-heading" class="text-2xl sm:text-3xl font-bold text-white">New Arrivals</h2>
        <p class="text-slate-400 max-w-xl mx-auto text-sm sm:text-base">Fresh gear added to the catalogue. Verified and ready to ship.</p>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <ProductCard v-for="product in newArrivals" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- All Other Products -->
    <section id="all-products" class="space-y-8 sm:space-y-10" role="region" aria-labelledby="all-products-heading">
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h2 id="all-products-heading" class="text-2xl sm:text-3xl font-bold text-white">Complete Catalogue</h2>
          <p class="text-slate-400 text-sm sm:text-base mt-1">Every product we carry, from cables to complete systems.</p>
        </div>
        <button
          v-if="otherProducts.length > 3"
          @click="showAllOther = !showAllOther"
          class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors font-medium flex items-center gap-1"
        >
          {{ showAllOther ? 'Show less' : `Show all (${otherProducts.length})` }}
          <svg class="w-3 h-3" :class="{ 'rotate-180': showAllOther }" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <ProductCard v-for="product in (showAllOther ? otherProducts : otherProducts.slice(0, 3))" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>
  </div>
</template>
