import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('../views/Home.vue')
const Shop = () => import('../views/Shop.vue')
const ProductDetail = () => import('../views/ProductDetail.vue')
const FavoritesVue = () => import('../views/Favorites.vue')
const Checkout = () => import('../views/Checkout.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Contact = () => import('../views/Contact.vue')
const About = () => import('../views/About.vue')
const Insights = () => import('../views/Insights.vue')
const FAQ = () => import('../views/FAQ.vue')
const NotFound = () => import('../views/NotFound.vue')
const OrderTracking = () => import('../views/OrderTracking.vue')
const OrderConfirmation = () => import('../views/OrderConfirmation.vue')
const PrivacyPolicy = () => import('../views/PrivacyPolicy.vue')
const TermsOfService = () => import('../views/TermsOfService.vue')
const CookiesPolicy = () => import('../views/CookiesPolicy.vue')

const routes = [
  { path: '/', component: Home },
  { path: '/shop', component: Shop },
  { path: '/product/:id', component: ProductDetail },
  { path: '/favorites', component: FavoritesVue },
  { path: '/checkout', component: Checkout },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/contact', component: Contact },
  { path: '/about', component: About },
  { path: '/insights', component: Insights },
  { path: '/faq', component: FAQ },
  { path: '/tracking', component: OrderTracking },
  { path: '/confirmation', component: OrderConfirmation },
  { path: '/privacy', component: PrivacyPolicy },
  { path: '/terms', component: TermsOfService },
  { path: '/cookies', component: CookiesPolicy },
  { path: '/:pathMatch(.*)*', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router