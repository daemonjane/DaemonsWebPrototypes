/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.html", "./assets/**/*.js"],
  theme: {
    extend: {
      colors: {
        cyan: { 400: '#06b6d4', 500: '#0891b2', 600: '#0e7490', 900: '#164e63' },
        slate: { 950: '#020617', 900: '#0f172a', 800: '#1e293b', 700: '#334155', 600: '#475569', 500: '#64748b', 400: '#94a3b8' },
      },
      fontFamily: { mono: ['JetBrains Mono', 'Fira Code', 'monospace'], sans: ['Inter', 'system-ui'] },
      animation: { 'float-glow': 'floatGlow 6s ease-in-out infinite' },
      keyframes: { floatGlow: { '0%,100%': { transform: 'translateX(-50%) translateY(0px)' }, '50%': { transform: 'translateX(-50%) translateY(-15px)' } } },
    },
  },
  plugins: [],
}