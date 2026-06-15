<script setup>
/**
 * Site footer with links, social icons, newsletter CTA, meta info, and live visitor count.
 * @component
 */
import { useLiveVisitorCount } from '../composables/useLiveVisitorCount'

const { count } = useLiveVisitorCount()
</script>

<template>
  <footer id="main-footer" class="bg-slate-900 border-t border-slate-800 mt-16 sm:mt-20">
    <div class="max-w-7xl mx-auto px-4 py-10 sm:py-12">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
        <!-- Brand -->
        <div class="col-span-2 md:col-span-1 space-y-3">
          <router-link to="/" class="text-lg font-bold text-white tracking-tight">
            <span class="text-cyan-400">&lt;</span>TECH<span class="text-cyan-400">/</span>STORE<span class="text-cyan-400">&gt;</span>
          </router-link>
          <p class="text-xs text-slate-500 leading-relaxed">Verified high-performance hardware. Direct vendor sourcing. Real-time market insights.</p>
        </div>

        <!-- Navigation -->
        <div class="space-y-3">
          <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Navigate</h3>
          <ul class="space-y-2">
            <li><router-link to="/shop" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Shop All</router-link></li>
            <li><router-link to="/favorites" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Favorites</router-link></li>
            <li><router-link to="/insights" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Market Pulse</router-link></li>
            <li><router-link to="/about" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">About</router-link></li>
          </ul>
        </div>

        <!-- Support -->
        <div class="space-y-3">
          <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Support</h3>
          <ul class="space-y-2">
            <li><router-link to="/contact" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Contact</router-link></li>
            <li><router-link to="/login" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Account</router-link></li>
            <li><router-link to="/register" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">Register</router-link></li>
            <li><router-link to="/faq" class="text-sm text-slate-500 hover:text-cyan-400 transition-colors">FAQ</router-link></li>
          </ul>
        </div>

        <!-- Newsletter -->
        <div class="col-span-2 md:col-span-1 space-y-3">
          <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Stay Updated</h3>
          <p class="text-xs text-slate-500">Get allocation drops and pricing alerts.</p>
          <form @submit.prevent class="flex gap-2">
            <input type="email" placeholder="Your email" class="flex-1 bg-slate-800 border border-slate-700 rounded-md px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400">
            <button type="submit" class="bg-cyan-600 text-white px-3 py-2 rounded-md text-xs font-semibold hover:bg-cyan-500 transition-colors">Subscribe</button>
          </form>
          <div class="flex gap-3 pt-1">
            <a href="#" class="text-slate-600 hover:text-cyan-400 transition-colors" aria-label="Twitter">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
            </a>
            <a href="#" class="text-slate-600 hover:text-cyan-400 transition-colors" aria-label="GitHub">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
            </a>
            <a href="#" class="text-slate-600 hover:text-cyan-400 transition-colors" aria-label="Discord">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z"/></svg>
            </a>
          </div>
        </div>
      </div>
    </div>
    <div class="border-t border-slate-800 py-4">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-slate-600">
        <div>&copy; 2026 TechStore Engine. Global Supply Hub.</div>
        <div class="flex items-center gap-4">
          <span class="flex items-center gap-1.5" title="Live visitors">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="font-mono text-emerald-400/80">{{ count }}</span>
            <span>browsing now</span>
          </span>
          <span class="hover:text-slate-400 transition-colors cursor-pointer">Privacy</span>
          <span class="hover:text-slate-400 transition-colors cursor-pointer">Terms</span>
          <span class="hover:text-slate-400 transition-colors cursor-pointer">Cookies</span>
        </div>
      </div>
    </div>
  </footer>
</template>
