<script setup>
defineProps({
  variant: { type: String, default: 'hero' }
})
</script>

<template>
  <!-- Abstract geometric art — AI-generated style SVG patterns -->
  <div class="absolute pointer-events-none select-none" aria-hidden="true">
    <!-- Hero variant: large gradient geometric shapes -->
    <svg v-if="variant === 'hero'" class="w-full h-full opacity-20 dark:opacity-20" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#a78bfa" stop-opacity="0.1"/>
        </linearGradient>
        <linearGradient id="g2" x1="100%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.1"/>
        </linearGradient>
        <linearGradient id="g3" x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="#2dd4bf" stop-opacity="0.05"/>
        </linearGradient>
      </defs>
      <polygon points="100,50 300,20 280,180 80,160" fill="url(#g1)">
        <animateTransform attributeName="transform" type="translate" values="0,0;20,-10;0,0" dur="15s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="600,80 750,150 700,300 550,230" fill="url(#g2)">
        <animateTransform attributeName="transform" type="translate" values="0,0;-15,12;0,0" dur="18s" repeatCount="indefinite"/>
      </polygon>
      <circle cx="400" cy="300" r="180" fill="url(#g3)">
        <animate attributeName="r" values="170;190;170" dur="12s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.5;0.8;0.5" dur="12s" repeatCount="indefinite"/>
      </circle>
      <polygon points="200,400 350,380 330,520 180,500" fill="url(#g1)" opacity="0.4">
        <animateTransform attributeName="transform" type="rotate" values="0 265 450;5 265 450;0 265 450" dur="20s" repeatCount="indefinite"/>
      </polygon>
      <polygon points="500,350 650,320 620,470" fill="url(#g2)" opacity="0.3">
        <animateTransform attributeName="transform" type="rotate" values="0 575 400;-4 575 400;0 575 400" dur="14s" repeatCount="indefinite"/>
      </polygon>
      <line x1="50" y1="550" x2="750" y2="550" stroke="url(#g1)" stroke-width="2" opacity="0.2">
        <animate attributeName="x1" values="50;150;50" dur="10s" repeatCount="indefinite"/>
      </line>
      <circle cx="120" cy="180" r="4" fill="#06b6d4" opacity="0.6">
        <animate attributeName="r" values="4;8;4" dur="4s" repeatCount="indefinite"/>
      </circle>
      <circle cx="680" cy="120" r="3" fill="#a78bfa" opacity="0.5">
        <animate attributeName="r" values="3;7;3" dur="5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="350" cy="500" r="5" fill="#38bdf8" opacity="0.4">
        <animate attributeName="r" values="5;10;5" dur="6s" repeatCount="indefinite"/>
      </circle>
    </svg>

    <!-- About variant: soft floating geometric clusters -->
    <svg v-else-if="variant === 'about'" class="w-full h-full opacity-15 dark:opacity-15" viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="ga1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="#2dd4bf" stop-opacity="0.05"/>
        </linearGradient>
        <linearGradient id="ga2" x1="100%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stop-color="#a78bfa" stop-opacity="0.15"/>
          <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.05"/>
        </linearGradient>
      </defs>
      <rect x="30" y="40" width="120" height="120" rx="20" fill="url(#ga1)" transform="rotate(15 90 100)">
        <animateTransform attributeName="transform" type="rotate" values="15 90 100;20 90 100;15 90 100" dur="12s" repeatCount="indefinite"/>
      </rect>
      <rect x="450" y="60" width="100" height="100" rx="16" fill="url(#ga2)" transform="rotate(-10 500 110)">
        <animateTransform attributeName="transform" type="rotate" values="-10 500 110;-5 500 110;-10 500 110" dur="14s" repeatCount="indefinite"/>
      </rect>
      <circle cx="300" cy="250" r="100" fill="url(#ga1)" opacity="0.4">
        <animate attributeName="r" values="95;105;95" dur="10s" repeatCount="indefinite"/>
      </circle>
      <polygon points="80,350 200,320 190,430" fill="url(#ga2)" opacity="0.3"/>
      <polygon points="420,380 520,350 500,460" fill="url(#ga1)" opacity="0.25"/>
    </svg>
  </div>
</template>
