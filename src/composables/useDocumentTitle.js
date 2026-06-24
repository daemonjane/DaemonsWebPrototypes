import { watch } from 'vue'
import { useRoute } from 'vue-router'

const TITLES = {
  '/': 'Home',
  '/shop': 'Shop',
  '/favorites': 'Favorites',
  '/checkout': 'Checkout',
  '/login': 'Sign In',
  '/register': 'Register',
  '/contact': 'Contact',
  '/about': 'About',
  '/insights': 'Market Pulse',
  '/faq': 'FAQ',
  '/privacy': 'Privacy Policy',
  '/terms': 'Terms of Service',
  '/cookies': 'Cookie Policy',
  '/profile': 'Your Profile',
  '/orders': 'Order History',
  '/tracking': 'Order Tracking',
  '/counter': 'Counter',
}

export function useDocumentTitle() {
  const route = useRoute()
  watch(() => route.path, (path) => {
    const title = path.startsWith('/product/') ? 'Product' : (TITLES[path] || 'TechStore')
    document.title = `${title} | TechStore`
  }, { immediate: true })
}
