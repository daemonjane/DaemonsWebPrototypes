<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import AnimatedCounter from '../components/AnimatedCounter.vue'
import AbstractArt from '../components/AbstractArt.vue'
import { useCart } from '../composables/useCart'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'
import { useScrollReveal } from '../composables/useScrollReveal'
import { resolveImage } from '../utils/images'
import OptimizedImage from '../components/OptimizedImage.vue'
import { normalizeProduct, pick } from '../utils/product'

const { observe } = useScrollReveal(0.06)

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
const categoryCounts = ref({})
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
    } else {
      console.warn('Osimart products fetch failed')
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
      categories.value = pick(catRes.value).filter(c => c.featured || c.slugified_name).slice(0, 8)
    }
    const counts = {}
    for (const p of products.value) {
      const cat = p.category
      counts[cat] = (counts[cat] || 0) + 1
    }
    categoryCounts.value = counts
    if (brandRes.status === 'fulfilled') {
      brands.value = pick(brandRes.value)
    }
    if (collRes.status === 'fulfilled') {
      collections.value = pick(collRes.value)
    }
    buildShowcase()
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
const comingSoonProducts = computed(() => products.value.filter(p => p.comingSoon))
const otherProducts = computed(() => {
  const featuredIds = new Set(featuredProducts.value.map(p => p.id))
  const newIds = new Set(newArrivals.value.map(p => p.id))
  return products.value.filter(p => !featuredIds.has(p.id) && !newIds.has(p.id))
})

const showAllOther = ref(false)

const showcaseItems = ref([])
const showcaseIndex = ref(0)
const currentShowcase = computed(() => showcaseItems.value[showcaseIndex.value] || null)
let showcaseTimer = null

function buildShowcase() {
  const items = []
  for (const b of brands.value) {
    items.push({ type: 'brand', name: b.name, logo: b.logo, id: b.id || b.name })
  }
  for (const p of products.value.slice(0, 12)) {
    if (!items.some(i => i.type === 'product' && i.id === p.id)) {
      items.push({ type: 'product', name: p.name, image: p.image, price: p.price, id: p.id })
    }
  }
  showcaseItems.value = items.sort(() => Math.random() - 0.5)
  clearInterval(showcaseTimer)
  showcaseTimer = setInterval(() => {
    if (showcaseItems.value.length) {
      showcaseIndex.value = (showcaseIndex.value + 1) % showcaseItems.value.length
    }
  }, 1800)
}

onUnmounted(() => { clearInterval(showcaseTimer) })

// Bundles
const bundles = [
  { id: 'bundle-silent', name: 'Silent Operator Bundle', description: 'Vanguard Desktop + Cyber‑Pro Keyboard + Desk Mat', price: 2596, saved: 152, oldPrice: 2748 },
  { id: 'bundle-immersive', name: 'Immersive Vision Bundle', description: '34" QD‑OLED Monitor + VESA Arm + Bias Lighting Kit', price: 1299, saved: 93, oldPrice: 1392 }
]

function addBundleToCart(bundle) {
  addItem({ id: bundle.id, name: bundle.name, price: bundle.price })
}

function quickAdd(product) {
  addItem({ id: product.id, uuid: product.uuid, variantId: product.variantId, name: product.name, price: product.price })
}

// ───── Hero cursor spotlight ─────
function onHeroMouse(e) {
  const hero = document.getElementById('hero')
  if (!hero) return
  const rect = hero.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  hero.style.setProperty('--spot-x', `${x}%`)
  hero.style.setProperty('--spot-y', `${y}%`)
}

// ───── Ripple effect on buttons ─────
function onRipple(e) {
  const btn = e.currentTarget
  const rect = btn.getBoundingClientRect()
  const ripple = document.createElement('span')
  ripple.className = 'ripple'
  ripple.style.left = `${e.clientX - rect.left}px`
  ripple.style.top = `${e.clientY - rect.top}px`
  btn.appendChild(ripple)
  ripple.addEventListener('animationend', () => ripple.remove())
}

// ───── Card spotglow effect ─────
function onSpotglowMove(e) {
  const card = e.currentTarget
  const rect = card.getBoundingClientRect()
  const x = ((e.clientX - rect.left) / rect.width) * 100
  const y = ((e.clientY - rect.top) / rect.height) * 100
  card.style.setProperty('--sx', `${x}%`)
  card.style.setProperty('--sy', `${y}%`)
}

// ───── Parallax on hero ─────
const heroY = ref(0)
let parallaxRaf = null

function onHeroScroll() {
  const heroEl = document.getElementById('hero')
  if (!heroEl) return
  const rect = heroEl.getBoundingClientRect()
  const speed = 0.15
  heroY.value = rect.top * speed
}

onMounted(() => {
  window.addEventListener('scroll', onHeroScroll, { passive: true })
})
onUnmounted(() => {
  window.removeEventListener('scroll', onHeroScroll)
})

// ───── Tilt effect on category cards ─────
function onTilt(e) {
  const card = e.currentTarget
  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  const rotateX = ((y - centerY) / centerY) * -6
  const rotateY = ((x - centerX) / centerX) * 6
  card.style.setProperty('--rx', `${rotateX}deg`)
  card.style.setProperty('--ry', `${rotateY}deg`)
}

function onTiltLeave(e) {
  const card = e.currentTarget
  card.style.setProperty('--rx', '0deg')
  card.style.setProperty('--ry', '0deg')
}

// ───── Magnetic effect on buttons ─────
function onMagneticMove(e) {
  const btn = e.currentTarget
  const rect = btn.getBoundingClientRect()
  const x = e.clientX - rect.left - rect.width / 2
  const y = e.clientY - rect.top - rect.height / 2
  const strength = 0.3
  btn.style.setProperty('--mx', `${x * strength}px`)
  btn.style.setProperty('--my', `${y * strength}px`)
}
function onMagneticLeave(e) {
  const btn = e.currentTarget
  btn.style.setProperty('--mx', '0px')
  btn.style.setProperty('--my', '0px')
}
</script>

<template>
  <div>
    <!-- ───── Banners carousel ───── -->
    <section v-if="banners.length" class="relative overflow-hidden rounded-xl mb-20 sm:mb-28" role="region" aria-label="Promotional banners">
      <div class="flex transition-transform duration-700 ease-out" :style="{ transform: `translateX(-${activeSlide * 100}%)` }">
        <div v-for="(banner, i) in banners" :key="banner.id || i" class="min-w-full relative">
          <OptimizedImage :src="resolveImage(banner.image)" :alt="banner.title || 'Banner'" wrapperClass="w-full h-48 sm:h-72" :priority="i === 0" />
          <div v-if="banner.title" class="absolute inset-0 flex items-center justify-center bg-black/30">
            <h2 class="text-white text-2xl sm:text-4xl font-bold reveal" :class="{ revealed: true }" data-reveal-delay="200">{{ banner.title }}</h2>
          </div>
        </div>
      </div>
      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2" role="tablist" aria-label="Slide navigation">
        <button v-for="(banner, i) in banners" :key="i" @click="setSlide(i)" :aria-label="`Go to slide ${i + 1}`" :aria-selected="activeSlide === i" :class="['w-2.5 h-2.5 rounded-full transition-all', activeSlide === i ? 'bg-cyan-400 scale-125' : 'bg-slate-500/60 hover:bg-slate-400']"></button>
      </div>
    </section>

    <!-- Banners (static fallback) -->
    <section v-if="!banners.length" class="relative flex flex-col items-center text-center py-12 sm:py-16 mb-20 sm:mb-28 overflow-hidden rounded-xl bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-800">
      <p class="text-slate-400 text-sm max-w-lg mx-auto px-4">Browse our latest collection — premium hardware sourced directly from verified vendors.</p>
    </section>

    <!-- ───── Loading skeleton ───── -->
    <template v-if="loading">
      <section class="mb-20 sm:mb-28">
        <div class="max-w-4xl mx-auto text-center space-y-6 py-12 sm:py-20 lg:py-28">
          <div class="skeleton w-32 h-6 mx-auto"></div>
          <div class="skeleton w-3/4 h-14 mx-auto"></div>
          <div class="skeleton w-2/3 h-6 mx-auto"></div>
          <div class="flex justify-center gap-4 pt-4">
            <div class="skeleton w-36 h-12"></div>
            <div class="skeleton w-36 h-12"></div>
          </div>
        </div>
      </section>
      <section class="mb-20 sm:mb-28">
        <div class="max-w-5xl mx-auto">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-8 sm:gap-12">
            <div v-for="i in 4" :key="i" class="text-center space-y-2">
              <div class="skeleton w-20 h-8 mx-auto"></div>
              <div class="skeleton w-24 h-4 mx-auto"></div>
            </div>
          </div>
        </div>
      </section>
      <section class="mb-20 sm:mb-28 max-w-5xl mx-auto">
        <div class="text-center space-y-3 mb-10">
          <div class="skeleton w-16 h-6 mx-auto"></div>
          <div class="skeleton w-48 h-10 mx-auto"></div>
          <div class="skeleton w-72 h-5 mx-auto"></div>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
          <div v-for="i in 3" :key="i" class="skeleton h-48"></div>
        </div>
      </section>
      <section class="mb-20 sm:mb-28">
        <div class="flex items-center justify-between mb-8">
          <div><div class="skeleton w-16 h-6 mb-2"></div><div class="skeleton w-48 h-8"></div></div>
          <div class="skeleton w-20 h-5"></div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
          <div v-for="i in 6" :key="i" class="skeleton h-32"></div>
        </div>
      </section>
    </template>

    <template v-if="!loading">
    <!-- ───── Hero ───── -->
    <section id="hero" @mousemove="onHeroMouse" class="relative flex flex-col items-center text-center py-12 sm:py-20 lg:py-28 overflow-hidden mb-20 sm:mb-28"
              role="region" aria-labelledby="hero-heading">
      <div class="hero-glow"></div>
      <div class="hero-spotlight" :style="{ background: `radial-gradient(600px circle at var(--spot-x, 50%) var(--spot-y, 50%), rgba(6,182,212,0.08), transparent 60%)` }"></div>
      <AbstractArt variant="hero" class="absolute inset-0 w-full h-full" />
      <div :ref="(el) => el && observe(el)" class="relative max-w-4xl space-y-6 sm:space-y-8 reveal" data-reveal-stagger="120" :style="{ transform: `translateY(${heroY}px)` }">
        <span class="inline-block bg-cyan-900/40 text-cyan-300 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider border border-cyan-800/30">{{ hero?.badge || 'SYSTEM_READY' }}</span>
        <h1 id="hero-heading" class="text-4xl sm:text-5xl md:text-7xl font-extrabold text-white leading-tight drop-shadow-lg tracking-tight">{{ hero?.title || 'Your Command Station Awaits' }}</h1>
        <p class="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">{{ hero?.subtitle || 'Build the ultimate workspace from the comfort of your home. We ship the finest hardware, custom‑tuned for silence and power.' }}</p>
        <div class="flex flex-wrap justify-center gap-4 pt-4">
          <router-link :to="hero?.primary_cta?.link || '/shop'" @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple" class="magnetic-btn ripple-btn bg-cyan-600 text-white px-8 sm:px-10 py-3.5 sm:py-4 rounded-md font-semibold shadow-lg shadow-cyan-900/30 hover:bg-cyan-500 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">{{ hero?.primary_cta?.label || 'Start Building' }}</router-link>
          <router-link :to="hero?.secondary_cta?.link || '/insights'" @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple" class="magnetic-btn ripple-btn border border-slate-600 text-slate-300 px-8 sm:px-10 py-3.5 sm:py-4 rounded-md font-semibold hover:border-cyan-500 hover:text-cyan-400 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">{{ hero?.secondary_cta?.label || 'Explore Membership' }}</router-link>
        </div>
      </div>
    </section>

    <!-- ───── Full-bleed Metrics bar ───── -->
    <section id="metrics" class="relative -mx-4 sm:-mx-8 px-4 sm:px-8 py-12 sm:py-16 bg-gradient-to-r from-slate-900 via-slate-900/90 to-slate-900 border-y border-slate-800/60 mb-20 sm:mb-28" aria-label="Company metrics">
      <div class="max-w-5xl mx-auto reveal" data-reveal-delay="0">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 sm:gap-12">
          <template v-if="metrics.length">
            <AnimatedCounter v-for="(m, i) in metrics" :key="i" :target="m.target" :suffix="m.suffix" :label="m.label" :duration="m.duration || 1800" :decimals="m.decimals" />
          </template>
          <template v-else>
            <AnimatedCounter :target="10" suffix="K+" label="Products Shipped" :duration="1800" />
            <AnimatedCounter :target="50" suffix="K+" label="Happy Customers" :duration="2000" />
            <AnimatedCounter :target="99.9" suffix="%" label="Uptime SLA" :decimals="1" :duration="2200" />
            <AnimatedCounter :target="24" suffix="/7" label="Support Response" :duration="1500" />
          </template>
        </div>
      </div>
    </section>

    <!-- ───── Features ───── -->
    <section id="features" class="max-w-5xl mx-auto mb-20 sm:mb-28" role="region" aria-labelledby="features-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Why Us</span>
        <h2 id="features-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">{{ store?.name ? store.name : 'TechStore' }}</h2>
        <p class="text-slate-400 max-w-lg mx-auto">Every component sourced, tested, and tuned for peak performance.</p>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8 reveal" data-reveal-stagger="100">
        <template v-if="features.length">
          <article v-for="(f, i) in features" :key="i" @mousemove="onSpotglowMove" class="spotglow bg-slate-900/70 rounded-xl p-7 sm:p-8 border border-slate-800/80 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
            <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">{{ f.icon || '✦' }}</div>
            <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">{{ f.title }}</h3>
            <p class="text-slate-400 text-sm leading-relaxed">{{ f.description }}</p>
          </article>
        </template>
        <template v-else>
          <article @mousemove="onSpotglowMove" class="spotglow bg-slate-900/70 rounded-xl p-7 sm:p-8 border border-slate-800/80 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
            <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">⚡</div>
            <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Verified Performance</h3>
            <p class="text-slate-400 text-sm leading-relaxed">Every component undergoes a 12‑hour stress test before it leaves the lab.</p>
          </article>
          <article @mousemove="onSpotglowMove" class="spotglow bg-slate-900/70 rounded-xl p-7 sm:p-8 border border-slate-800/80 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
            <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📦</div>
            <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Direct Vendor Sourcing</h3>
            <p class="text-slate-400 text-sm leading-relaxed">No middlemen. Authentic parts straight from the production line to your door.</p>
          </article>
          <article @mousemove="onSpotglowMove" class="spotglow bg-slate-900/70 rounded-xl p-7 sm:p-8 border border-slate-800/80 space-y-4 text-center hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-950/20 transition-all duration-300">
            <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📊</div>
            <h3 class="text-lg sm:text-xl font-semibold text-cyan-400">Optimal Price-to-Quality</h3>
            <p class="text-slate-400 text-sm leading-relaxed">Real‑time market analysis ensures you always get the best value per dollar.</p>
          </article>
        </template>
      </div>
    </section>

    <!-- ───── Divider ───── -->
    <div class="section-divider mb-20 sm:mb-28 max-w-xl mx-auto"></div>

    <!-- ───── Categories ───── -->
    <section v-if="categories.length" id="categories" class="mb-20 sm:mb-28" role="region" aria-labelledby="categories-heading">
      <div class="flex items-center justify-between mb-8 sm:mb-10 reveal" data-reveal-delay="0">
        <div>
          <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30 mb-3">Browse</span>
          <h2 id="categories-heading" class="text-2xl sm:text-3xl font-bold text-gradient-cyan">Shop by Category</h2>
        </div>
        <router-link to="/shop" class="link-underline text-sm text-cyan-400 hover:text-cyan-300 transition-colors font-medium">View all →</router-link>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 reveal" data-reveal-stagger="60">
        <router-link
          v-for="c in categories" :key="c.id || c.slugified_name"
          :to="'/shop?category=' + (c.slugified_name || c.name)"
          @mousemove="onTilt; onSpotglowMove($event)" @mouseleave="onTiltLeave"
          class="tilt-card spotglow bg-slate-900/70 rounded-xl p-5 border border-slate-800/80 hover:border-cyan-700 hover:bg-slate-800/80 transition-all duration-200 text-center group"
        >
          <div class="w-10 h-10 mx-auto bg-cyan-900/20 rounded-xl flex items-center justify-center text-cyan-400 text-xl mb-3 group-hover:scale-110 transition-transform duration-200">{{ c.icon || '📦' }}</div>
          <span class="text-sm text-slate-300 group-hover:text-white font-medium block">{{ c.name }}</span>
          <span class="text-xs text-slate-600 mt-1 block">{{ categoryCounts[c.slugified_name] || categoryCounts[c.name] || c.product_count || c.products_count || 0 }} items</span>
        </router-link>
      </div>
    </section>

    <!-- ───── Brands (marquee) ───── -->
    <section v-if="brands.length" id="brands" class="mb-20 sm:mb-28" role="region" aria-labelledby="brands-heading">
      <div class="flex items-center justify-between mb-6 reveal" data-reveal-delay="0">
        <h2 id="brands-heading" class="text-lg font-semibold text-white flex items-center gap-2">
          <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
          </svg>
          Featured Brands
        </h2>
        <router-link to="/shop" class="link-underline text-sm text-cyan-400 hover:text-cyan-300 transition-colors font-medium">Browse all →</router-link>
      </div>
      <div class="overflow-hidden rounded-xl bg-slate-900/40 border border-slate-800/60 py-4 reveal" data-reveal-delay="100">
        <div class="marquee-track">
          <template v-for="b in brands" :key="b.id || b.slugified_name">
            <router-link
              :to="'/shop?brand=' + (b.slugified_name || b.name)"
              class="flex-shrink-0 w-32 text-center group"
            >
              <div v-if="b.logo" class="h-10 flex items-center justify-center mb-1">
                <OptimizedImage :src="resolveImage(b.logo)" :alt="b.name" wrapperClass="h-10 flex items-center justify-center" imgClass="max-h-full max-w-full object-contain opacity-60 group-hover:opacity-100 transition-opacity" />
              </div>
              <div v-else class="h-10 flex items-center justify-center mb-1">
                <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 text-sm">{{ (b.name || '?')[0] }}</div>
              </div>
              <span class="text-xs text-slate-500 group-hover:text-white font-medium block truncate">{{ b.name }}</span>
            </router-link>
          </template>
          <template v-for="b in brands" :key="b.id + '-dup'">
            <router-link
              :to="'/shop?brand=' + (b.slugified_name || b.name)"
              class="flex-shrink-0 w-32 text-center group"
            >
              <div v-if="b.logo" class="h-10 flex items-center justify-center mb-1">
                <OptimizedImage :src="resolveImage(b.logo)" :alt="b.name" wrapperClass="h-10 flex items-center justify-center" imgClass="max-h-full max-w-full object-contain opacity-60 group-hover:opacity-100 transition-opacity" />
              </div>
              <div v-else class="h-10 flex items-center justify-center mb-1">
                <div class="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 text-sm">{{ (b.name || '?')[0] }}</div>
              </div>
              <span class="text-xs text-slate-500 group-hover:text-white font-medium block truncate">{{ b.name }}</span>
            </router-link>
          </template>
        </div>
      </div>
    </section>

    <!-- ───── Testimonials ───── -->
    <section id="testimonials" class="max-w-5xl mx-auto mb-20 sm:mb-28" role="region" aria-labelledby="testimonials-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Social Proof</span>
        <h2 id="testimonials-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">{{ store?.testimonials_heading || 'Trusted by Builders' }}</h2>
        <p class="text-slate-400 max-w-lg mx-auto">Real stories from real customers who built their dream rigs with us.</p>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 reveal" data-reveal-stagger="120">
        <template v-if="testimonials.length">
          <div v-for="(t, i) in testimonials" :key="i" class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 space-y-4 hover:border-slate-700 transition-all duration-300">
            <div class="flex items-center gap-2 text-yellow-400 text-sm">{{ '★★★★★'.slice(0, t.rating || 5) }}{{ '☆☆☆☆☆'.slice(0, 5 - (t.rating || 5)) }}</div>
            <p class="text-sm text-slate-400 leading-relaxed">"{{ t.text || t.content }}"</p>
            <div class="flex items-center gap-2 pt-3 border-t border-slate-800">
              <div class="w-8 h-8 rounded-full flex items-center justify-center text-cyan-400 text-xs font-mono font-bold" :class="t.initials_bg || 'bg-cyan-900/40'">{{ (t.initials || (t.name || '').split(' ').map(w => w[0]).join('').slice(0, 2) || '??') }}</div>
              <div><p class="text-xs text-white font-medium">{{ t.name }}</p><p class="text-[10px] text-slate-500">{{ t.role || 'Verified Buyer' }}</p></div>
            </div>
          </div>
        </template>
        <template v-else>
          <div class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 space-y-4 hover:border-slate-700 transition-all duration-300">
            <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★★</div>
            <p class="text-sm text-slate-400 leading-relaxed">"The Vanguard desktop is an absolute beast. Silent, cool, and rips through 4K rendering like nothing."</p>
            <div class="flex items-center gap-2 pt-3 border-t border-slate-800">
              <div class="w-8 h-8 rounded-full bg-cyan-900/40 flex items-center justify-center text-cyan-400 text-xs font-mono font-bold">MK</div>
              <div><p class="text-xs text-white font-medium">Marcus K.</p><p class="text-[10px] text-slate-500">Verified Buyer</p></div>
            </div>
          </div>
          <div class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 space-y-4 hover:border-slate-700 transition-all duration-300">
            <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★★</div>
            <p class="text-sm text-slate-400 leading-relaxed">"Quick shipping, well-packaged, and the QD-OLED monitor exceeded every expectation. Colors are unreal."</p>
            <div class="flex items-center gap-2 pt-3 border-t border-slate-800">
              <div class="w-8 h-8 rounded-full bg-fuchsia-900/40 flex items-center justify-center text-fuchsia-400 text-xs font-mono font-bold">SL</div>
              <div><p class="text-xs text-white font-medium">Sarah L.</p><p class="text-[10px] text-slate-500">Verified Buyer</p></div>
            </div>
          </div>
          <div class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 space-y-4 hover:border-slate-700 transition-all duration-300 sm:col-span-2 lg:col-span-1">
            <div class="flex items-center gap-2 text-yellow-400 text-sm">★★★★☆</div>
            <p class="text-sm text-slate-400 leading-relaxed">"Great selection of components. The market insights helped me time my GPU purchase perfectly. Saved $200."</p>
            <div class="flex items-center gap-2 pt-3 border-t border-slate-800">
              <div class="w-8 h-8 rounded-full bg-emerald-900/40 flex items-center justify-center text-emerald-400 text-xs font-mono font-bold">DJ</div>
              <div><p class="text-xs text-white font-medium">Daemon J.</p><p class="text-[10px] text-slate-500">Insights Member</p></div>
            </div>
          </div>
        </template>
      </div>
    </section>

    <!-- ───── Divider ───── -->
    <div class="section-divider mb-20 sm:mb-28 max-w-xl mx-auto"></div>

    <!-- ───── Recently Viewed ───── -->
    <section v-if="recentlyViewed.length > 0" id="recently-viewed" class="mb-20 sm:mb-28" role="region" aria-labelledby="recently-viewed-heading">
      <div class="reveal" data-reveal-delay="0">
        <h2 id="recently-viewed-heading" class="text-lg sm:text-xl font-semibold text-white flex items-center gap-2 mb-6">
          <svg class="w-5 h-5 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Recently Viewed
        </h2>
      </div>
      <div class="relative group/scroll reveal" data-reveal-delay="100">
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
            class="flex-shrink-0 w-40 sm:w-44 bg-slate-900/70 rounded-lg border border-slate-800/80 overflow-hidden hover:border-cyan-700 hover:-translate-y-0.5 transition-all duration-200 snap-start group"
          >
            <div class="h-24 overflow-hidden">
              <OptimizedImage :src="item.image" :alt="item.name" wrapperClass="h-full w-full" imgClass="group-hover:scale-105 transition-transform duration-500" />
            </div>
            <div class="p-2.5 space-y-1">
              <p class="text-xs text-slate-200 truncate font-medium">{{ item.name }}</p>
              <p class="text-cyan-400 text-xs font-mono">${{ Number(item.price || 0).toFixed(2) }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ───── Featured Products ───── -->
    <section id="products" class="mb-20 sm:mb-28" role="region" aria-labelledby="products-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Featured</span>
        <h2 id="products-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">Core Systems & Gear</h2>
        <p class="text-slate-400 flex items-center justify-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <strong>Next Verified Allocation Drop:</strong>
          <span class="text-cyan-300 font-mono glow-pulse scale-bounce inline-block rounded px-2" aria-live="polite" :key="countdownText">{{ countdownText }}</span>
        </p>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 reveal" data-reveal-stagger="100">
        <ProductCard v-for="product in featuredProducts" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- ───── Coming Soon ───── -->
    <section v-if="comingSoonProducts.length" id="coming-soon" class="max-w-5xl mx-auto mb-20 sm:mb-28" role="region" aria-labelledby="coming-soon-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-amber-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-amber-900/20 border border-amber-800/30">Coming Soon</span>
        <h2 id="coming-soon-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">Pre‑Release Hardware</h2>
        <p class="text-slate-400 max-w-lg mx-auto">Reserve your spot for the next drop. Early backers get priority pricing.</p>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 reveal" data-reveal-stagger="100">
        <ProductCard v-for="product in comingSoonProducts" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- ───── Bundles ───── -->
    <section id="bundles" class="max-w-5xl mx-auto mb-20 sm:mb-28" role="region" aria-labelledby="bundles-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Bundle & Save</span>
        <h2 id="bundles-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">Complete Your Spacestation</h2>
        <p class="text-slate-400 max-w-xl mx-auto">Hand‑picked combos that save you money. Bundle pricing adjusts with demand.</p>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 reveal" data-reveal-stagger="150">
        <div class="bg-gradient-to-br from-slate-900/80 to-slate-800/80 rounded-xl p-6 border border-slate-700 flex flex-col space-y-5 hover:border-cyan-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-900/20 transition-all duration-300">
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
          <button @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple($event); addBundleToCart(bundles[0])" class="magnetic-btn ripple-btn mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
        </div>
        <div class="bg-gradient-to-br from-slate-900/80 to-slate-800/80 rounded-xl p-6 border border-slate-700 flex flex-col space-y-5 hover:border-cyan-700 hover:-translate-y-1 hover:shadow-lg hover:shadow-cyan-900/20 transition-all duration-300">
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
          <button @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple($event); addBundleToCart(bundles[1])" class="magnetic-btn ripple-btn mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
        </div>
      </div>
    </section>

    <!-- ───── Trending + New Arrivals ───── -->
    <section id="discover" class="mb-20 sm:mb-28" role="region" aria-labelledby="discover-heading">
      <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
        <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Discover</span>
        <h2 id="discover-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">Trending & New</h2>
        <p class="text-slate-400 max-w-lg mx-auto">What the community is buying right now.</p>
      </div>

      <!-- Trending -->
      <div class="bg-slate-900/70 rounded-xl p-5 sm:p-6 border border-slate-800/80 mb-8 reveal" data-reveal-delay="50">
        <h3 class="text-lg font-semibold text-white mb-5 flex items-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          Trending Now
        </h3>
        <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 reveal" data-reveal-stagger="80">
          <div v-for="product in trendingProducts" :key="product.uuid || product.id" class="group flex items-center justify-between bg-slate-800/80 rounded-lg p-3 transition-colors hover:bg-slate-700/80">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 overflow-hidden rounded shrink-0">
                <OptimizedImage :src="product.image" :alt="product.name" wrapperClass="h-full w-full rounded" imgClass="group-hover:scale-105 group-hover:rotate-1 transition-transform duration-500 ease-out" />
              </div>
              <div>
                <span class="text-slate-200 text-sm block">{{ product.name }}</span>
                <span class="text-cyan-400 text-xs">{{ product.description }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-slate-300 text-sm font-bold">${{ Number(product.price || 0).toFixed(2) }}</span>
              <button @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple($event); quickAdd(product)" class="magnetic-btn ripple-btn bg-cyan-600 text-white text-xs px-3 py-1.5 rounded-md group-hover:bg-cyan-500 group-hover:shadow-md group-hover:shadow-cyan-500/30 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Quick Add</button>
            </div>
          </div>
        </div>
      </div>

      <!-- New Arrivals -->
      <div class="reveal" data-reveal-delay="0">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold text-white flex items-center gap-2">
            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
            </svg>
            New Arrivals
          </h3>
          <router-link to="/shop" class="link-underline text-sm text-cyan-400 hover:text-cyan-300 transition-colors font-medium">View all →</router-link>
        </div>
      </div>
      <div :ref="(el) => el && observe(el)" class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 reveal" data-reveal-stagger="80">
        <ProductCard v-for="product in newArrivals" :key="product.uuid || product.id" :product="product" />
      </div>
    </section>

    <!-- ───── Divider ───── -->
    <div class="section-divider mb-20 sm:mb-28 max-w-xl mx-auto"></div>

    <!-- ───── Membership (Insights + Tiers merged) ───── -->
    <section id="membership" class="mb-20 sm:mb-28" role="region" aria-labelledby="membership-heading">
      <div class="max-w-5xl mx-auto">
        <div class="text-center space-y-3 mb-10 sm:mb-12 reveal" data-reveal-delay="0">
          <span class="inline-block text-cyan-400 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider bg-cyan-900/20 border border-cyan-800/30">Membership</span>
          <h2 id="membership-heading" class="text-3xl sm:text-4xl font-bold text-gradient-cyan">Insights Membership</h2>
          <p class="text-slate-400 max-w-2xl mx-auto">Know when to buy. Live market data, price alerts, and benchmarking tools.</p>
        </div>

        <!-- Insights Preview -->
        <div class="relative group max-w-3xl mx-auto mb-10 reveal" data-reveal-delay="50">
          <div class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/60 backdrop-blur-[2px] rounded-xl border border-dashed border-cyan-800/50 transition-all duration-300 group-hover:bg-slate-950/70">
            <span class="text-4xl mb-2 float-1">🔒</span>
            <p class="text-white font-semibold text-sm sm:text-base mb-4">Unlock Real‑Time Market Data</p>
            <router-link to="/insights" @click="onRipple" class="ripple-btn bg-cyan-600 text-white px-5 py-2.5 rounded-md font-semibold text-sm hover:bg-cyan-500 active:scale-95 transition-all duration-150 shadow-lg shadow-cyan-900/30 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Subscribe to Unlock →</router-link>
          </div>
          <div class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 opacity-40 blur-sm select-none pointer-events-none">
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

        <!-- Tiers -->
        <div :ref="(el) => el && observe(el)" class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 max-w-4xl mx-auto reveal" data-reveal-stagger="150">
          <div class="bg-slate-900/70 rounded-xl p-6 border border-slate-800/80 flex flex-col space-y-4 hover:border-slate-700 hover:-translate-y-1 hover:shadow-lg transition-all duration-300">
            <h3 class="text-lg sm:text-xl font-semibold text-white">Monthly Pass</h3>
            <p class="text-slate-400 text-sm">Perfect for a one‑time build optimization.</p>
            <span class="text-2xl sm:text-3xl font-bold text-cyan-400">$9.99<span class="text-lg font-normal text-slate-500">/mo</span></span>
            <ul class="space-y-2 text-sm text-slate-400 list-disc list-inside">
              <li>Real‑time price tracking</li>
              <li>Efficiency score tools</li>
              <li>Stock alerts</li>
            </ul>
            <button @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple($event); selectMembership('monthly')" class="magnetic-btn ripple-btn mt-auto bg-cyan-600 text-white py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150">Subscribe Monthly</button>
          </div>
          <div class="relative p-[2px] rounded-xl bg-gradient-to-br from-cyan-400 via-blue-600 to-fuchsia-500 md:scale-105 shadow-xl shadow-cyan-950/40 z-10 hover:shadow-2xl hover:shadow-cyan-900/50 transition-all duration-300 animate-gradient">
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
              <button @mousemove="onMagneticMove" @mouseleave="onMagneticLeave" @click="onRipple($event); selectMembership('annual')" class="magnetic-btn ripple-btn mt-auto bg-cyan-600 text-white py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150">Subscribe Annually</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ───── Rotating Showcase ───── -->
    <section v-if="showcaseItems.length" id="showcase" class="relative -mx-4 sm:-mx-8 px-4 sm:px-8 py-6 overflow-hidden border-y border-slate-800/60 bg-slate-900/30" role="region" aria-label="Featured showcase">
      <div class="max-w-5xl mx-auto">
        <div class="relative flex items-center justify-center h-20 sm:h-24">
          <transition name="showcase" mode="out-in">
            <div v-if="currentShowcase" :key="currentShowcase.id + '-' + showcaseIndex" class="absolute inset-0 flex items-center justify-center gap-4 px-6">
              <template v-if="currentShowcase.type === 'brand'">
                <OptimizedImage v-if="currentShowcase.logo" :src="resolveImage(currentShowcase.logo)" :alt="currentShowcase.name" wrapperClass="h-8 sm:h-10" imgClass="w-auto h-full object-contain opacity-60" />
                <div v-else class="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-slate-500 text-lg font-bold">{{ (currentShowcase.name || '?')[0] }}</div>
                <span class="text-slate-400 text-sm sm:text-base font-medium">{{ currentShowcase.name }}</span>
              </template>
              <template v-else>
                <OptimizedImage :src="currentShowcase.image" :alt="currentShowcase.name" wrapperClass="h-10 sm:h-14" imgClass="w-auto h-full object-contain rounded" />
                <div class="text-left">
                  <p class="text-white text-sm sm:text-base font-medium truncate max-w-[200px] sm:max-w-xs">{{ currentShowcase.name }}</p>
                  <p class="text-cyan-400 text-xs font-mono">${{ Number(currentShowcase.price || 0).toFixed(2) }}</p>
                </div>
              </template>
            </div>
          </transition>
          <div class="absolute bottom-1 left-1/2 -translate-x-1/2 flex gap-1">
            <span v-for="i in Math.min(showcaseItems.length, 20)" :key="i" class="w-1.5 h-1.5 rounded-full transition-all duration-300" :class="i - 1 === showcaseIndex ? 'bg-cyan-400 scale-125' : 'bg-slate-700'"></span>
          </div>
        </div>
      </div>
    </section>
    </template>
  </div>
</template>

<style scoped>
.showcase-enter-active { transition: all 0.35s ease-out; }
.showcase-leave-active { transition: all 0.25s ease-in; }
.showcase-enter-from { opacity: 0; transform: translateY(12px); }
.showcase-leave-to { opacity: 0; transform: translateY(-12px); }

.tilt-card {
  transform: perspective(600px) rotateX(var(--rx, 0deg)) rotateY(var(--ry, 0deg));
  transition: transform 0.15s ease-out, border-color 0.2s, background-color 0.2s;
  will-change: transform;
}

.magnetic-btn {
  transform: translate(var(--mx, 0), var(--my, 0));
  transition: transform 0.15s ease-out, background-color 0.2s, border-color 0.2s, box-shadow 0.2s;
  will-change: transform;
}
</style>
