import { ref } from 'vue'
import router from '../router'

const isLoading = ref(false)
const showSkeleton = ref(false)
let timer = null

router.beforeEach(() => {
  isLoading.value = true
  clearTimeout(timer)
  timer = setTimeout(() => {
    if (isLoading.value) showSkeleton.value = true
  }, 200)
})

router.afterEach(() => {
  isLoading.value = false
  showSkeleton.value = false
  clearTimeout(timer)
})

router.onError(() => {
  isLoading.value = false
  showSkeleton.value = false
  clearTimeout(timer)
})

export function useRouteLoading() {
  return { isLoading, showSkeleton }
}
