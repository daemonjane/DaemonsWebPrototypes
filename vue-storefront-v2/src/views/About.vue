<script setup>
import { ref, onMounted } from 'vue'
import AnimatedCounter from '../components/AnimatedCounter.vue'

const timelineOpen = ref(false)
const expandedValue = ref(null)
const stackVisible = ref(false)

onMounted(() => { setTimeout(() => { stackVisible.value = true }, 200) })

const techStack = [
  { name: 'Vue 3 + Vite', level: 95, color: 'bg-emerald-500' },
  { name: 'Python / Django', level: 88, color: 'bg-cyan-500' },
  { name: 'Go (CLI tooling)', level: 82, color: 'bg-sky-500' },
  { name: 'Rust (experimental)', level: 65, color: 'bg-fuchsia-500' },
  { name: 'PostgreSQL / Redis', level: 90, color: 'bg-amber-500' },
  { name: 'Docker / K8s', level: 78, color: 'bg-blue-500' },
]

const values = [
  { id: 'quality', title: 'Relentless Quality', icon: '⚙️', detail: 'Every component undergoes a 12-hour stress test in our lab. If it doesn\'t pass, it doesn\'t ship.' },
  { id: 'transparency', title: 'Radical Transparency', icon: '📡', detail: 'We publish real-time market pricing so you know exactly what you\'re paying for — no hidden margins.' },
  { id: 'speed', title: 'Velocity', icon: '⚡', detail: 'From order to doorstep in under 48 hours for in-stock items. Our warehouse operates 24/7.' },
  { id: 'support', title: 'White-Glove Support', icon: '🛡️', detail: 'Dedicated engineer assigned to every custom build. Direct line, no chatbots.' },
]

const milestones = [
  { year: '2024 Q1', event: 'TechStore founded in San Francisco' },
  { year: '2024 Q3', event: 'First 1,000 orders shipped' },
  { year: '2025 Q1', event: 'Launched real-time market insights platform' },
  { year: '2025 Q3', event: 'Opened second warehouse in Austin, TX' },
  { year: '2026 Q1', event: 'Surpassed 50,000 customers globally' },
]
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <span class="text-xs font-mono text-cyan-500 uppercase tracking-wider bg-cyan-950/30 px-2 py-1 rounded">Company</span>
    <h1 class="text-3xl sm:text-4xl font-bold text-white mt-3 mb-2">About TechStore</h1>
    <p class="text-slate-400 mb-10">The infrastructure behind the infrastructure.</p>

    <!-- Stats row -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-6 mb-10 py-6 border-y border-slate-800">
      <AnimatedCounter :target="50" suffix="K+" label="Customers" :duration="2000" />
      <AnimatedCounter :target="10" suffix="K+" label="Products Shipped" :duration="2200" />
      <AnimatedCounter :target="3" suffix="" label="Years Operation" :duration="1500" />
      <AnimatedCounter :target="99.7" suffix="%" label="Satisfaction" :decimals="1" :duration="2500" />
    </div>

    <!-- Mission -->
    <div class="bg-slate-900 p-6 sm:p-8 rounded-xl border border-slate-800 space-y-4 mb-8">
      <h2 class="text-xl font-semibold text-white">Our Mission</h2>
      <p class="text-slate-400 leading-relaxed">
        Founded in 2024, TechStore delivers verified high-performance hardware with transparent pricing and real-time market insights.
        We stress-test every component and offer direct vendor sourcing — no middlemen, no markup games.
      </p>
      <p class="text-slate-400 leading-relaxed">
        Our mission: empower builders, gamers, and creators with gear that outperforms expectations at every price point.
      </p>
    </div>

    <!-- Values (interactive expandable cards) -->
    <div class="grid sm:grid-cols-2 gap-4 mb-8">
      <button
        v-for="v in values"
        :key="v.id"
        @click="expandedValue = expandedValue === v.id ? null : v.id"
        class="bg-slate-900 p-5 rounded-xl border text-left transition-all duration-200"
        :class="expandedValue === v.id ? 'border-cyan-700 bg-cyan-950/10' : 'border-slate-800 hover:border-slate-700'"
      >
        <div class="flex items-center gap-3 mb-2">
          <span class="text-xl">{{ v.icon }}</span>
          <h3 class="font-semibold text-white">{{ v.title }}</h3>
        </div>
        <div v-if="expandedValue === v.id" class="mt-2 text-sm text-slate-400 leading-relaxed animate-[fadeIn_0.2s_ease]">
          {{ v.detail }}
        </div>
        <p v-else class="text-xs text-slate-500 mt-1">Click to expand →</p>
      </button>
    </div>

    <!-- Tech Stack -->
    <div class="bg-slate-900 rounded-xl border border-slate-800 p-6 mb-8">
      <h2 class="text-xl font-semibold text-white mb-4">Tech Stack</h2>
      <div class="space-y-3">
        <div v-for="tech in techStack" :key="tech.name">
          <div class="flex justify-between text-sm mb-1">
            <span class="text-slate-300">{{ tech.name }}</span>
            <span class="text-cyan-400 font-mono text-xs">{{ tech.level }}%</span>
          </div>
          <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div class="h-full rounded-full transition-all duration-1000 ease-out" :style="{ width: stackVisible ? tech.level + '%' : '0%' }" :class="tech.color"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Timeline (interactive toggle) -->
    <div class="bg-slate-900 rounded-xl border border-slate-800 mb-8">
      <button
        @click="timelineOpen = !timelineOpen"
        class="w-full flex items-center justify-between p-6 text-left"
      >
        <h2 class="text-xl font-semibold text-white">Milestones</h2>
        <svg class="w-5 h-5 text-slate-400 transition-transform duration-200" :class="{ 'rotate-180': timelineOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <div v-if="timelineOpen" class="px-6 pb-6 space-y-0">
        <div v-for="(m, i) in milestones" :key="i" class="flex gap-4 pb-4 last:pb-0">
          <div class="flex flex-col items-center">
            <div class="w-3 h-3 rounded-full bg-cyan-600 mt-1.5"></div>
            <div v-if="i < milestones.length - 1" class="w-0.5 flex-1 bg-slate-800 mt-1"></div>
          </div>
          <div>
            <p class="text-xs font-mono text-cyan-400 font-bold">{{ m.year }}</p>
            <p class="text-sm text-slate-300">{{ m.event }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Team -->
    <div class="bg-slate-900 p-6 sm:p-8 rounded-xl border border-slate-800">
      <h2 class="text-xl font-semibold text-white mb-4">Team</h2>
      <div class="grid sm:grid-cols-2 gap-4 text-sm">
        <div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 hover:bg-slate-800 hover:border-cyan-800/50 border border-transparent transition-all duration-200 group">
          <div class="w-10 h-10 rounded-full bg-cyan-900/40 flex items-center justify-center text-cyan-400 font-mono font-bold group-hover:scale-110 transition-transform">JD</div>
          <div>
            <p class="text-white font-medium">Jane Daemon</p>
            <p class="text-slate-500 group-hover:text-cyan-400 transition-colors">Founder & Lead Engineer</p>
          </div>
        </div>
        <div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3 hover:bg-slate-800 hover:border-cyan-800/50 border border-transparent transition-all duration-200 group">
          <div class="w-10 h-10 rounded-full bg-fuchsia-900/40 flex items-center justify-center text-fuchsia-400 font-mono font-bold group-hover:scale-110 transition-transform">CE</div>
          <div>
            <p class="text-white font-medium">Charbel Elias</p>
            <p class="text-slate-500 group-hover:text-cyan-400 transition-colors">Systems Architect</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
