/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
  "./index.html",
  "./src/**/*.{vue,js,ts,jsx,tsx}",
],
  theme: {
    extend: {
      colors: {
        gold: { 300: '#E8C84A', 400: '#D4AF37', 500: '#C5A028', 600: '#A8851E', 700: '#8B6B14 },
        emerald: { 400: '#2DD4A0', 500: '#1B8A6B', 600: '#157A5E', 700: '#0F6A51 },
        rose: { 300: '#F5C6D0', 400: '#E8A0B4', 500: '#D47A96', 600: '#B85A7A },
        cream: { 50: '#FEFCF9', 100: '#FAF8F5', 200: '#F5F0EB', 300: '#EDE5DC' },
        charcoal: { 900: '#14141F', 800: '#1C1C2E', 700: '#262640', 600: '#32325A },
        dark: { bg: '#14141F', card: '#1C1C2E', border: '#262640', text: '#EDEDF0' },
        light: { bg: '#FAF8F5', card: '#FFFFFF', border: '#EDE5DC', text: '#1C1C2E' },
      },
      fontFamily: {
        display: ['Playfair Display', 'Georgia', 'serif'],
        body: ['Poppins', 'Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'gold-pulse': 'goldPulse 2s ease-in-out infinite',
        'card-lift': 'cardLift 0.3s ease-out',
        'fade-up': 'fadeUp 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'count-pulse': 'countPulse 1.5s ease-in-out infinite',
        'shimmer-gold': 'shimmerGold 2s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'scale-bounce': 'scaleBounce 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)',
        'marquee': 'marquee 30s linear infinite',
      },
      keyframes: {
        goldPulse: {
          '0%,100%': { boxShadow: '0 0 8px rgba(212,175,55,0.3)' },
          '50%': { boxShadow: '0 0 20px rgba(212,175,55,0.6)' },
        },
        cardLift: {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(-4px)' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(12px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        countPulse: {
          '0%,100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.15)' },
        },
        shimmerGold: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%,100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
        scaleBounce: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.15)' },
          '100%': { transform: 'scale(1)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [],
}
