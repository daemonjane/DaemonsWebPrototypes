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
        gold: {
          50: '#FEF9E7',
          100: '#FDF0C4',
          200: '#FBE08A',
          300: '#F5CB45',
          400: '#E8B913',
          500: '#D4AF37',
          600: '#B8931A',
          700: '#8C6E13',
          800: '#604A0E',
          900: '#3A2D09',
        },
        surface: {
          950: '#08080D',
          900: '#0E0E16',
          850: '#13131D',
          800: '#1A1A27',
          750: '#20202F',
          700: '#2A2A3D',
          600: '#3A3A52',
          500: '#50506A',
          400: '#70708A',
          300: '#9898AD',
          200: '#C0C0D0',
          100: '#E0E0EA',
          50: '#F4F4F8',
        },
        success: { 400: '#4ADE80', 500: '#22C55E', 600: '#16A34A' },
        danger: { 400: '#F87171', 500: '#EF4444', 600: '#DC2626' },
        warn: { 400: '#FBBF24', 500: '#F59E0B', 600: '#D97706' },
      },
      fontFamily: {
        display: ['"Space Grotesk"', '"Inter"', 'system-ui', 'sans-serif'],
        body: ['"Inter"', '"Space Grotesk"', 'system-ui', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Fira Code"', 'monospace'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.25rem',
      },
      boxShadow: {
        'glow-gold': '0 0 20px rgba(212, 175, 55, 0.15)',
        'glow-gold-lg': '0 0 40px rgba(212, 175, 55, 0.2)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.25)',
        'card-hover': '0 8px 40px rgba(0, 0, 0, 0.35), 0 0 20px rgba(212, 175, 55, 0.08)',
        'elevated': '0 12px 48px rgba(0, 0, 0, 0.4)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'fade-up': 'fadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1)',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.3s ease-out',
        'scale-in': 'scaleIn 0.3s cubic-bezier(0.22, 1, 0.36, 1)',
        'float': 'float 6s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'marquee': 'marquee 30s linear infinite',
        'pulse-gold': 'pulseGold 3s ease-in-out infinite',
        'counter': 'counterSpin 0.4s cubic-bezier(0.22, 1, 0.36, 1)',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        slideInLeft: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        pulseGold: {
          '0%, 100%': { boxShadow: '0 0 8px rgba(212, 175, 55, 0)' },
          '50%': { boxShadow: '0 0 24px rgba(212, 175, 55, 0.2)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        counterSpin: {
          '0%': { opacity: '0', transform: 'translateY(8px) scale(0.95)' },
          '100%': { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
      },
    },
  },
  plugins: [],
}
