import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useLoadingBar } from './composables/useLoadingBar'
import { vSpotlight, vMagnetic } from './directives/effects'
import './style.css'

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
app.directive('spotlight', vSpotlight)
app.directive('magnetic', vMagnetic)
app.mount('#app')