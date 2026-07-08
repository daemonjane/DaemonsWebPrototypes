import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useLoadingBar } from './composables/useLoadingBar'
import { ensureCSRF } from './utils/api'
import './style.css'

ensureCSRF().catch(() => {})

router.beforeEach(() => {
  const { start } = useLoadingBar()
  start()
})

router.afterEach(() => {
  const { done } = useLoadingBar()
  done()
})

const app = createApp(App)
app.use(router)
app.mount('#app')