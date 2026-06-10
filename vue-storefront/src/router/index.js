import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Shop from '../views/Shop.vue'
// import other views later

const routes = [
  { path: '/', component: Home },
  { path: '/shop', component: Shop },
  // ...
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router