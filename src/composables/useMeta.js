import { watch, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useHead } from '../utils/head'

const DEFAULTS = {
  title: 'Vertex — High-Tier Hardware & Precision Components',
  description: 'High-tier hardware, precision-sourced. Direct vendor supply chains, real-time market intelligence, and custom-tuned peak-performance builds.',
  image: '/og-image.png',
  url: 'https://vertex.dev',
  siteName: 'Vertex',
}

const PAGE_META = {
  '/': {
    title: 'Vertex — High-Tier Hardware & Precision Components',
    description: 'High-tier hardware, precision-sourced. Direct vendor chains, real-time market intelligence, custom-tuned performance builds.',
  },
  '/shop': {
    title: 'Shop — Vertex',
    description: 'Browse our catalogue of high-tier hardware — GPUs, CPUs, storage, peripherals, and precision-tuned systems.',
  },
  '/favorites': {
    title: 'Favorites — Vertex',
    description: 'Your saved products and wishlist.',
  },
  '/checkout': {
    title: 'Checkout — Vertex',
    description: 'Review your cart and complete your order.',
  },
  '/login': {
    title: 'Sign In — Vertex',
    description: 'Sign in to your Vertex account.',
  },
  '/register': {
    title: 'Create Account — Vertex',
    description: 'Create a Vertex account to track orders and save favorites.',
  },
  '/contact': {
    title: 'Contact — Vertex',
    description: 'Get in touch with the Vertex team for support, inquiries, or custom builds.',
  },
  '/about': {
    title: 'About — Vertex',
    description: 'Learn about Vertex — our mission, team, and commitment to high-tier hardware.',
  },
  '/insights': {
    title: 'Market Pulse — Vertex',
    description: 'Real-time market data, component pricing, stock levels, and demand forecasts.',
  },
  '/faq': {
    title: 'FAQ — Vertex',
    description: 'Frequently asked questions about ordering, shipping, returns, and memberships.',
  },
  '/privacy': {
    title: 'Privacy Policy — Vertex',
    description: 'Vertex privacy policy — how we collect, use, and protect your data.',
  },
  '/terms': {
    title: 'Terms of Service — Vertex',
    description: 'Vertex terms of service — the rules governing your use of our platform.',
  },
  '/cookies': {
    title: 'Cookie Policy — Vertex',
    description: 'How Vertex uses cookies and how you can manage your preferences.',
  },
  '/profile': {
    title: 'Your Profile — Vertex',
    description: 'Manage your Vertex account profile and preferences.',
  },
  '/orders': {
    title: 'Order History — Vertex',
    description: 'View your order history and track shipments.',
  },
  '/tracking': {
    title: 'Order Tracking — Vertex',
    description: 'Track your Vertex order in real time.',
  },
  '/confirmation': {
    title: 'Order Confirmed — Vertex',
    description: 'Your Vertex order has been placed successfully.',
  },
  '/dashboard': {
    title: 'Dashboard — Vertex',
    description: 'Your Vertex account dashboard — orders, favorites, and activity.',
  },
}

export function useMeta(pageMeta) {
  const route = useRoute()

  watch(() => route.path, (path) => {
    const isProduct = path.startsWith('/product/')
    const isAdmin = path.startsWith('/admin/')
    let meta

    if (isProduct) {
      meta = { title: 'Product — Vertex', description: 'View product details, specs, and pricing.' }
    } else if (isAdmin) {
      meta = { title: 'Admin — Vertex', description: 'Vertex admin panel — manage your store.' }
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
