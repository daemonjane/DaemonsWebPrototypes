<script setup>
/**
 * About page with company history, team, and mission statement.
 * @view
 */
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-3xl font-bold text-white mb-2">About TechStore</h1>
    <p class="text-slate-400 mb-8">The infrastructure behind the infrastructure.</p>

    <div class="space-y-8">
      <div class="bg-slate-900 p-6 sm:p-8 rounded-xl border border-slate-800 space-y-4">
        <h2 class="text-xl font-semibold text-white">Our Mission</h2>
        <p class="text-slate-400 leading-relaxed">
          Founded in 2024, TechStore delivers verified high-performance hardware with transparent pricing and real-time market insights.
          We stress-test every component and offer direct vendor sourcing — no middlemen, no markup games.
        </p>
        <p class="text-slate-400 leading-relaxed">
          Our mission: empower builders, gamers, and creators with gear that outperforms expectations at every price point.
        </p>
      </div>

      <div class="grid sm:grid-cols-3 gap-6">
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 text-center space-y-3 hover:border-cyan-800 transition-colors">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">⚙️</div>
          <h3 class="font-semibold text-white">12-Hour Stress Test</h3>
          <p class="text-sm text-slate-400">Every component tested before it leaves the lab.</p>
        </div>
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 text-center space-y-3 hover:border-cyan-800 transition-colors">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📡</div>
          <h3 class="font-semibold text-white">Direct Sourcing</h3>
          <p class="text-sm text-slate-400">Authentic parts straight from the production line.</p>
        </div>
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 text-center space-y-3 hover:border-cyan-800 transition-colors">
          <div class="w-12 h-12 mx-auto bg-cyan-900/30 rounded-full flex items-center justify-center text-cyan-400 text-xl">📊</div>
          <h3 class="font-semibold text-white">Real-Time Pricing</h3>
          <p class="text-sm text-slate-400">Market-driven prices updated in real time.</p>
        </div>
      </div>

      <div class="bg-slate-900 p-6 sm:p-8 rounded-xl border border-slate-800">
        <h2 class="text-xl font-semibold text-white mb-4">Team</h2>
        <div class="grid sm:grid-cols-2 gap-4 text-sm">
          <div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3">
            <div class="w-10 h-10 rounded-full bg-cyan-900/40 flex items-center justify-center text-cyan-400 font-mono font-bold">JD</div>
            <div><p class="text-white font-medium">Jane Daemon</p><p class="text-slate-500">Founder & Lead Engineer</p></div>
          </div>
          <div class="flex items-center gap-3 bg-slate-800/50 rounded-lg p-3">
            <div class="w-10 h-10 rounded-full bg-fuchsia-900/40 flex items-center justify-center text-fuchsia-400 font-mono font-bold">CE</div>
            <div><p class="text-white font-medium">Charbel Elias</p><p class="text-slate-500">Systems Architect</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
