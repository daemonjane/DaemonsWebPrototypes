import { createRouter, createWebHistory } from 'vue-router'

const Home = () => import('../views/Home.vue')
const Shop = () => import('../views/Shop.vue')
const ProductDetail = () => import('../views/ProductDetail.vue')
const Checkout = () => import('../views/Checkout.vue')
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Contact = () => import('../views/Contact.vue')
const About = () => import('../views/About.vue')
const Insights = () => import('../views/Insights.vue')

const routes = [
  { path: '/', component: Home },
  { path: '/shop', component: Shop },
  { path: '/product/:id', component: ProductDetail },
  { path: '/checkout', component: Checkout },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/contact', component: Contact },
  { path: '/about', component: About },
  { path: '/insights', component: Insights },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router