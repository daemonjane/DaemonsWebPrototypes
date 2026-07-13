<script setup>
</script>

<template>
  <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
    <!-- Deep dark base -->
    <div class="absolute inset-0 bg-gradient-to-br from-surface-950 via-surface-900 to-surface-950"></div>

    <!-- Gold ambient glow — top center -->
    <div class="absolute inset-0 opacity-40" style="background: radial-gradient(ellipse 70% 40% at 50% -10%, rgba(212, 175, 55, 0.06), transparent);"></div>
    <!-- Warm accent — bottom right -->
    <div class="absolute inset-0 opacity-25" style="background: radial-gradient(ellipse 50% 40% at 85% 85%, rgba(212, 175, 55, 0.04), transparent);"></div>
    <!-- Subtle cool contrast — left -->
    <div class="absolute inset-0 opacity-15" style="background: radial-gradient(ellipse 40% 50% at 15% 60%, rgba(96, 74, 14, 0.08), transparent);"></div>

    <!-- Floating gold orbs -->
    <div class="absolute w-96 h-96 rounded-full" style="top: 8%; left: 10%; background: radial-gradient(circle, rgba(212, 175, 55, 0.03), transparent 70%); animation: orbFloat 14s ease-in-out infinite;"></div>
    <div class="absolute w-80 h-80 rounded-full" style="top: 55%; right: 8%; background: radial-gradient(circle, rgba(232, 185, 19, 0.025), transparent 70%); animation: orbFloat 18s ease-in-out infinite reverse;"></div>
    <div class="absolute w-64 h-64 rounded-full" style="bottom: 10%; left: 45%; background: radial-gradient(circle, rgba(184, 147, 26, 0.02), transparent 70%); animation: orbFloat 12s ease-in-out infinite 3s;"></div>

    <!-- Grid overlay — very subtle -->
    <div class="absolute inset-0 opacity-[0.012]" style="background-image: linear-gradient(rgba(212, 175, 55, 0.4) 1px, transparent 1px), linear-gradient(90deg, rgba(212, 175, 55, 0.4) 1px, transparent 1px); background-size: 48px 48px;"></div>

    <!-- Floating gold particles -->
    <div class="particle" style="top: 20%; left: 15%; width: 2px; height: 2px; background: #D4AF37; animation: particleFloat 22s linear infinite;"></div>
    <div class="particle" style="top: 35%; left: 75%; width: 2px; height: 2px; background: #E8B913; animation: particleFloat 28s linear infinite 4s;"></div>
    <div class="particle" style="top: 60%; left: 25%; width: 1px; height: 1px; background: #D4AF37; animation: particleFloat 20s linear infinite 7s;"></div>
    <div class="particle" style="top: 80%; left: 85%; width: 2px; height: 2px; background: #B8931A; animation: particleFloat 24s linear infinite 2s;"></div>
    <div class="particle" style="top: 45%; left: 50%; width: 1px; height: 1px; background: #D4AF37; animation: particleFloat 30s linear infinite 9s;"></div>
    <div class="particle" style="top: 15%; left: 90%; width: 2px; height: 2px; background: #E8B913; animation: particleFloat 18s linear infinite 5s;"></div>
    <div class="particle" style="top: 70%; left: 10%; width: 1px; height: 1px; background: #D4AF37; animation: particleFloat 26s linear infinite 1s;"></div>
    <div class="particle" style="top: 90%; left: 55%; width: 2px; height: 2px; background: #B8931A; animation: particleFloat 21s linear infinite 8s;"></div>
    <div class="particle" style="top: 50%; left: 35%; width: 1px; height: 1px; background: #D4AF37; animation: particleFloat 23s linear infinite 3s;"></div>
    <div class="particle" style="top: 5%; left: 45%; width: 2px; height: 2px; background: #E8B913; animation: particleFloat 27s linear infinite 6s;"></div>

    <!-- Noise texture -->
    <svg class="absolute inset-0 w-full h-full opacity-[0.025]" xmlns="http://www.w3.org/2000/svg">
      <filter id="noise">
        <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
        <feColorMatrix type="saturate" values="0"/>
      </filter>
      <rect width="100%" height="100%" filter="url(#noise)"/>
    </svg>
  </div>
</template>

<style>
.particle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.4;
}
@keyframes particleFloat {
  0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
  10% { opacity: 0.4; }
  45% { opacity: 0.5; }
  90% { opacity: 0.15; }
  100% { transform: translateY(-100vh) translateX(30px) scale(0.5); opacity: 0; }
}
@keyframes orbFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.05); }
  66% { transform: translate(-20px, 15px) scale(0.95); }
}
</style>
