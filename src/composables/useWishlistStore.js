import { ref } from 'vue'
import { useFavorites } from './useFavorites'

const userEmail = ref('')

export function useWishlistStore() {
  function setUser(email) {
    userEmail.value = email
  }

  const favs = useFavorites()

  return {
    ...favs,
    userEmail,
    setUser,
  }
}
