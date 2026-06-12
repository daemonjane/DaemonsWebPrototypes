<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import { products } from '../data/products'
import { useCart } from '../composables/useCart'

const { addItem, addUpgrade, removeUpgrade, setMembership } = useCart()

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
  const name = event.target.labels?.[0]?.innerText || id
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

// Show more / less
const showMoreItems = ref(false)

// Trending items
const trendingIds = ['thermal-paste', 'cable-ties', 'cleaning-kit', 'gpu-bracket', 'displayport-cable', 'mouse-bungee']
const trendingProducts = products.filter(p => trendingIds.includes(p.id))

// Featured products
const featuredProducts = products.filter(p => ['gaming-mouse', 'mousepad', 'usb-hub'].includes(p.id))

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
    <!-- Hero -->
    <section id="hero" class="relative flex flex-col items-center text-center py-16 sm:py-20 lg:py-24 overflow-hidden">
      <div class="hero-glow"></div>
      <div id="hero-core-container" class="relative max-w-3xl space-y-5 sm:space-y-7">
        <span class="inline-block bg-cyan-900/40 text-cyan-300 text-xs font-mono px-4 py-1.5 rounded-full uppercase tracking-wider">SYSTEM_READY</span>
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-extrabold text-white leading-tight drop-shadow-lg">Your Command Station Awaits</h1>
        <p class="text-base sm:text-lg text-slate-400 max-w-xl mx-auto">Build the ultimate workspace from the comfort of your home. We ship the finest hardware, custom‑tuned for silence and power.</p>
        <div id="hero-actions" class="flex flex-wrap justify-center gap-4 pt-4">
          <router-link to="/shop" class="bg-cyan-600 text-white px-6 sm:px-7 py-3 sm:py-3.5 rounded-md font-semibold shadow-lg shadow-cyan-900/30 hover:bg-cyan-500 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Start Building</router-link>
          <router-link to="/insights" class="border border-slate-600 text-slate-300 px-6 sm:px-7 py-3 sm:py-3.5 rounded-md font-semibold hover:border-cyan-500 hover:text-cyan-400 active:scale-95 transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Explore Membership</router-link>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="features" class="space-y-10 sm:space-y-12">
      <h2 class="text-2xl sm:text-3xl font-bold text-white text-center">Why TechStore?</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8">
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

    <!-- Products (featured) -->
    <section id="products" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white">Core Systems & Gear</h2>
        <p class="text-slate-400 text-sm sm:text-base flex items-center justify-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <strong>Next Verified Allocation Drop:</strong>
          <span class="text-cyan-300 font-mono">{{ countdownText }}</span>
        </p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
        <!-- Vanguard Desktop large card -->
        <article class="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 flex flex-col md:col-span-2 md:flex-row group transition-all duration-300 hover:border-slate-700 hover:shadow-xl hover:shadow-cyan-950/30 hover:-translate-y-1 transform">
          <div class="w-full md:w-1/2 shrink-0 bg-slate-800 aspect-[16/10] md:aspect-auto md:h-full relative overflow-hidden">
            <img src="/assets/vanguard-desktop-fallback.png" alt="Vanguard Gaming Desktop" class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out">
          </div>
          <div class="p-5 sm:p-6 flex flex-col flex-1 justify-between space-y-4">
            <div class="space-y-4">
              <div class="flex justify-between items-start">
                <h3 class="text-lg sm:text-xl font-bold text-white">Vanguard Series Core i7 / <mark class="bg-cyan-900/40 text-cyan-300 px-1.5 py-0.5 rounded text-sm">RTX 5070</mark></h3>
                <span class="bg-cyan-500/10 text-cyan-400 text-xs font-mono px-2 py-0.5 rounded border border-cyan-500/20 uppercase tracking-wider hidden sm:inline">Flagship Rig</span>
              </div>
              <p class="text-slate-400 text-sm leading-relaxed">Extreme workload desktop. Liquid‑cooled silence engineered for absolute dominance.</p>
              <div class="space-y-2">
                <label class="text-xs text-slate-500 font-medium block">Price-to-Quality Metric:</label>
                <meter min="0" max="10" low="4" high="7" optimum="9" value="9.4" class="w-full max-w-xs h-2 block">9.4/10</meter>
              </div>
              <details class="text-sm text-slate-400">
                <summary class="font-medium text-slate-300 hover:text-cyan-400 cursor-pointer transition-colors">Technical Blueprint</summary>
                <ul class="mt-2 space-y-1.5 list-disc list-inside bg-slate-950/40 p-3 rounded-lg border border-slate-800/60 font-mono text-xs">
                  <li><strong class="text-slate-300">GPU:</strong> 12GB Next‑Gen</li>
                  <li><strong class="text-slate-300">CPU:</strong> Intel i7‑14th, 20‑Core</li>
                  <li><strong class="text-slate-300">Cooling:</strong> 360mm AIO</li>
                </ul>
              </details>
            </div>
            <div class="flex items-center justify-between pt-4 border-t border-slate-800">
              <span class="text-xl sm:text-2xl font-mono font-bold text-white">$2,499</span>
              <button @click="addItem({ id: 'vanguard-desktop', name: 'Vanguard Series Core i7 / RTX 5070', price: 2499 })"
                      class="bg-cyan-600 text-white px-4 sm:px-5 py-2 sm:py-2.5 rounded-md text-sm font-semibold hover:bg-cyan-500 shadow-md hover:shadow-lg hover:shadow-cyan-500/20 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add to Cart</button>
            </div>
          </div>
        </article>

        <!-- Keyboard -->
        <ProductCard :product="products.find(p => p.id === 'cyberpro-keyboard')" />

        <!-- Monitor -->
        <ProductCard :product="products.find(p => p.id === 'ultrawide-monitor')" />
      </div>
    </section>

    <!-- Bundles -->
    <section id="bundles" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white">Complete Your Spacestation</h2>
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
          <button @click="addBundleToCart(bundles[0])"
                  class="mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
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
          <button @click="addBundleToCart(bundles[1])"
                  class="mt-auto bg-cyan-600 text-white px-5 sm:px-6 py-3 rounded-md font-semibold w-full hover:bg-cyan-500 active:scale-95 active:shadow-inner transition-all duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">Add Bundle to Cart</button>
        </div>
      </div>
    </section>

    <!-- Micro-upgrades -->
    <section id="micro-upgrades" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white">Personalize & Protect</h2>
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
                <label for="custom-engraving-text" class="text-xs text-slate-500 font-bold block">Engraving Text:</label>
                <input type="text" id="custom-engraving-text" value="jxne" placeholder=" " required minlength="3"
                       class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-slate-200 font-mono
                              focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950
                              [&:not(:placeholder-shown):invalid]:border-pink-500 [&:not(:placeholder-shown):invalid]:ring-pink-500/30
                              [&:not(:placeholder-shown):valid]:border-emerald-500 [&:not(:placeholder-shown):valid]:ring-emerald-500/30
                              transition-colors">
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
      <div id="impulse-checkout-counter" class="bg-slate-900 rounded-xl p-5 sm:p-6 border border-slate-800" role="group">
        <h3 class="text-lg sm:text-xl font-semibold text-white mb-5 flex items-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          ⚡ Trending Now!!!
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="product in trendingProducts" :key="product.id" class="group flex items-center justify-between bg-slate-800 rounded-lg p-3 transition-colors hover:bg-slate-700/80">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 overflow-hidden rounded bg-slate-700 shrink-0">
                <img :src="product.image" :alt="product.name" class="w-full h-full object-cover transition-transform duration-500 ease-out group-hover:scale-105 group-hover:rotate-1">
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
    <section id="insights-preview" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white flex items-center justify-center gap-2">
          <span class="flex h-2 w-2 relative">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          Market Pulse Preview
        </h2>
        <p class="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">
          Live component pricing, demand trends, and allocation forecasts — locked for members only.
          <br class="hidden sm:block">Subscribe to see the full data stream.
        </p>
      </div>
      <div class="relative group max-w-3xl mx-auto">
        <div class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-slate-950/60 backdrop-blur-[2px] rounded-xl border border-dashed border-cyan-800/50 transition-all duration-300 group-hover:bg-slate-950/70">
          <span class="text-4xl mb-2">🔒</span>
          <p class="text-white font-semibold text-sm sm:text-base mb-4">Unlock Real‑Time Market Data</p>
          <router-link to="/insights" class="bg-cyan-600 text-white px-5 py-2.5 rounded-md font-semibold text-sm hover:bg-cyan-500 active:scale-95 transition-all duration-150 shadow-lg shadow-cyan-900/30 focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950">
            Subscribe to Unlock →
          </router-link>
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
    <section id="insights-membership" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white">Insights Membership</h2>
        <p class="text-slate-400 max-w-2xl mx-auto text-sm sm:text-base">Know when to buy. Live market data, price alerts, and benchmarking tools.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 max-w-4xl mx-auto">
        <!-- Monthly -->
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
        <!-- Annual (highlighted) -->
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

    <!-- Show More Items (extra products) -->
    <section id="more-products" class="space-y-10 sm:space-y-12">
      <div class="text-center space-y-3">
        <h2 class="text-2xl sm:text-3xl font-bold text-white">Explore More Gear</h2>
        <p class="text-slate-400 max-w-xl mx-auto text-sm sm:text-base">Extra essentials that didn't fit the main deck. Still 100% verified.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Always visible: first three -->
        <ProductCard v-for="product in featuredProducts" :key="product.id" :product="product" />
        <!-- Extra items (hidden by default) -->
        <template v-if="showMoreItems">
          <ProductCard v-for="product in products.filter(p => ['wireless-headset', 'webcam', 'speakers'].includes(p.id))" :key="product.id" :product="product" />
        </template>
      </div>
      <div class="flex justify-center gap-4">
        <button v-if="!showMoreItems" @click="showMoreItems = true" class="bg-cyan-600 text-white px-6 py-3 rounded-md font-semibold hover:bg-cyan-500 active:scale-95 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400">
          Show More Items
        </button>
        <button v-else @click="showMoreItems = false" class="bg-slate-800 text-slate-300 px-6 py-3 rounded-md font-semibold hover:bg-slate-700 active:scale-95 transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400">
          Show Less
        </button>
      </div>
    </section>
  </div>
</template>