import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
const Shop = () => import(/* webpackChunkName: "shop" */ '../views/Shop.vue')
const ProductDetail = () => import(/* webpackChunkName: "product" */ '../views/ProductDetail.vue')
const FavoritesVue = () => import(/* webpackChunkName: "favorites" */ '../views/Favorites.vue')
const Checkout = () => import(/* webpackChunkName: "checkout" */ '../views/Checkout.vue')
const Login = () => import(/* webpackChunkName: "auth" */ '../views/Login.vue')
const GuestLogin = () => import(/* webpackChunkName: "auth" */ '../views/GuestLogin.vue')
const Register = () => import(/* webpackChunkName: "auth" */ '../views/Register.vue')
const Contact = () => import(/* webpackChunkName: "contact" */ '../views/Contact.vue')
const About = () => import(/* webpackChunkName: "about" */ '../views/About.vue')
const Insights = () => import(/* webpackChunkName: "insights" */ '../views/Insights.vue')
const FAQ = () => import(/* webpackChunkName: "faq" */ '../views/FAQ.vue')
const NotFound = () => import(/* webpackChunkName: "notfound" */ '../views/NotFound.vue')
const CounterFeature = () => import(/* webpackChunkName: "counter" */ '../views/CounterFeature.vue')
const OrderTracking = () => import(/* webpackChunkName: "orders" */ '../views/OrderTracking.vue')
const OrderConfirmation = () => import(/* webpackChunkName: "orders" */ '../views/OrderConfirmation.vue')
const OrderHistory = () => import(/* webpackChunkName: "orders" */ '../views/OrderHistory.vue')
const PrivacyPolicy = () => import(/* webpackChunkName: "legal" */ '../views/PrivacyPolicy.vue')
const TermsOfService = () => import(/* webpackChunkName: "legal" */ '../views/TermsOfService.vue')
const CookiesPolicy = () => import(/* webpackChunkName: "legal" */ '../views/CookiesPolicy.vue')
const Profile = () => import(/* webpackChunkName: "profile" */ '../views/Profile.vue')
const Dashboard = () => import(/* webpackChunkName: "dashboard" */ '../views/Dashboard.vue')
const Analytics = () => import(/* webpackChunkName: "analytics" */ '../views/Analytics.vue')
const OsimartAdmin = () => import(/* webpackChunkName: "admin" */ '../views/admin/OsimartAdmin.vue')
const AdminDashboard = () => import(/* webpackChunkName: "admin" */ '../views/AdminDashboard.vue')

const routes = [
  { path: '/', component: Home },
  { path: '/shop', component: Shop },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/admin', redirect: '/admin/osimart' },
  { path: '/admin/dashboard', component: AdminDashboard, meta: { requiresAuth: true, requiresStaff: true } },
  { path: '/admin/analytics', component: Analytics, meta: { requiresAuth: true, requiresStaff: true } },
  { path: '/admin/osimart', component: OsimartAdmin, meta: { requiresAuth: true, requiresStaff: true } },
  { path: '/analytics', component: Analytics, meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/orders', component: OrderHistory, meta: { requiresAuth: true } },
  { path: '/product/:id', component: ProductDetail },
  { path: '/favorites', component: FavoritesVue },
  { path: '/checkout', component: Checkout },
  { path: '/guest-login', component: GuestLogin },
  { path: '/login', component: Login, meta: { guestOnly: true } },
  { path: '/forgot-password', component: () => import(/* webpackChunkName: "auth" */ '../views/ForgotPassword.vue') },
  { path: '/reset-password/:uidb64/:token/', component: () => import(/* webpackChunkName: "auth" */ '../views/ResetPassword.vue') },
  { path: '/register', component: Register },
  { path: '/contact', component: Contact },
  { path: '/about', component: About },
  { path: '/insights', component: Insights },
  { path: '/faq', component: FAQ },
  { path: '/counter', component: CounterFeature },
  { path: '/tracking', component: OrderTracking },
  { path: '/confirmation', component: OrderConfirmation, meta: { title: 'Order Confirmation' } },
  { path: '/privacy', component: PrivacyPolicy },
  { path: '/terms', component: TermsOfService },
  { path: '/cookies', component: CookiesPolicy },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  },
})

router.beforeEach(async (to) => {
  try {
    const { useUser } = await import('../composables/useUser')
    const { user, refresh } = useUser()
    if (!user.value) await refresh()
    if (to.meta?.requiresAuth) {
      if (!user.value) return '/login'
      if (to.meta?.requiresStaff && !user.value?.is_staff) return '/'
    }
    if (to.meta?.guestOnly && user.value) return '/'
  } catch {
    if (to.meta?.requiresAuth) return '/login'
  }
})

export default router
