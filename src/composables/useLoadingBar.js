import { ref } from 'vue'
import nprogress from 'nprogress'
import 'nprogress/nprogress.css'

nprogress.configure({ showSpinner: false, trickleSpeed: 200 })

const configured = ref(true)

export function useLoadingBar() {
  function start() {
    nprogress.start()
  }

  function done() {
    nprogress.done()
  }

  return { start, done, configured }
}
