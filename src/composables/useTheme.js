import { ref, watch } from 'vue'

const THEME_KEY = 'vertex_theme'
const stored = localStorage.getItem(THEME_KEY)
const isDark = ref(stored !== null ? stored === 'dark' : true)

function apply() {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

apply()

watch(isDark, (val) => {
  localStorage.setItem(THEME_KEY, val ? 'dark' : 'light')
  apply()
})

export function useTheme() {
  function toggle() {
    isDark.value = !isDark.value
  }

  return { isDark, toggle }
}
