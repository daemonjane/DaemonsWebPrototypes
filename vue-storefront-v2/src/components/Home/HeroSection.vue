<template>
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
</template>