import { watch, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '../utils/head'

const DEFAULTS = {
  title: 'TechStore — Premium Hardware & Verified Components',
  description: 'Build the ultimate workspace with verified high-performance hardware. Direct vendor sourcing, real-time market insights, and custom-tuned systems.',
  image: '/og-image.png',
  url: 'https://techstore.dev',
  siteName: 'TechStore',
}

const PAGE_META = {
  '/': {
    title: 'TechStore — Premium Hardware & Verified Components',
    description: 'Build the ultimate workspace with verified high-performance hardware. Direct vendor sourcing, real-time market insights, and custom-tuned systems.',
  },
  '/shop': {
    title: 'Shop — TechStore',
    description: 'Browse our catalogue of verified high-performance hardware — GPUs, CPUs, monitors, peripherals, and complete systems.',
  },
  '/favorites': {
    title: 'Favorites — TechStore',
    description: 'Your saved products and wishlist items.',
  },
  '/checkout': {
    title: 'Checkout — TechStore',
    description: 'Review your cart and complete your purchase.',
  },
  '/login': {
    title: 'Sign In — TechStore',
    description: 'Sign in to your TechStore account.',
  },
  '/register': {
    title: 'Create Account — TechStore',
    description: 'Create a TechStore account to track orders and save favorites.',
  },
  '/contact': {
    title: 'Contact — TechStore',
    description: 'Get in touch with the TechStore team for support, inquiries, or custom builds.',
  },
  '/about': {
    title: 'About — TechStore',
    description: 'Learn about TechStore — our mission, team, and commitment to quality hardware.',
  },
  '/insights': {
    title: 'Market Pulse — TechStore',
    description: 'Real-time market data, component pricing, stock levels, and demand forecasts.',
  },
  '/faq': {
    title: 'FAQ — TechStore',
    description: 'Frequently asked questions about ordering, shipping, returns, and memberships.',
  },
  '/privacy': {
    title: 'Privacy Policy — TechStore',
    description: 'TechStore privacy policy — how we collect, use, and protect your data.',
  },
  '/terms': {
    title: 'Terms of Service — TechStore',
    description: 'TechStore terms of service — the rules governing your use of our platform.',
  },
  '/cookies': {
    title: 'Cookie Policy — TechStore',
    description: 'How TechStore uses cookies and how you can manage your preferences.',
  },
  '/profile': {
    title: 'Your Profile — TechStore',
    description: 'Manage your TechStore account profile and preferences.',
  },
  '/orders': {
    title: 'Order History — TechStore',
    description: 'View your order history and track shipments.',
  },
  '/tracking': {
    title: 'Order Tracking — TechStore',
    description: 'Track your TechStore order in real time.',
  },
  '/confirmation': {
    title: 'Order Confirmed — TechStore',
    description: 'Your TechStore order has been placed successfully.',
  },
  '/dashboard': {
    title: 'Dashboard — TechStore',
    description: 'Your TechStore account dashboard — orders, favorites, and activity.',
  },
}

export function useMeta(pageMeta) {
  const route = useRoute()

  watch(() => route.path, (path) => {
    const isProduct = path.startsWith('/product/')
    const isAdmin = path.startsWith('/admin/')
    let meta

    if (isProduct) {
      meta = { title: 'Product — TechStore', description: 'View product details, specs, and pricing.' }
    } else if (isAdmin) {
      meta = { title: 'Admin — TechStore', description: 'TechStore admin panel — manage your store.' }
    } else {
      meta = PAGE_META[path] || { title: DEFAULTS.title, description: DEFAULTS.description }
    }

    useHead({
      title: meta.title,
      meta: [
        { name: 'description', content: meta.description },
        { property: 'og:title', content: meta.title },
        { property: 'og:description', content: meta.description },
        { property: 'og:image', content: DEFAULTS.image },
        { property: 'og:url', content: `${DEFAULTS.url}${path}` },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: DEFAULTS.siteName },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: meta.title },
        { name: 'twitter:description', content: meta.description },
        { name: 'twitter:image', content: DEFAULTS.image },
      ],
    })
  }, { immediate: true })
}
