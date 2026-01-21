// filepath: e:\ProjectFainal\frontend\composables\useSmartBack.js
import { useRouter } from 'vue-router'

export const useSmartBack = () => {
  const router = useRouter()
  
  // Pages that should not be navigated back to
  const restrictedPages = ['/login', '/register', '/register-seller']
  
  // Track navigation history
  const navigationHistory = ref([])
  
  const goBack = () => {
    // Try to go back in history
    const canGoBack = window.history.length > 1
    
    if (canGoBack) {
      // Check if previous page is restricted
      let attempts = 0
      const maxAttempts = 5
      
      const goBackSafely = () => {
        if (attempts < maxAttempts) {
          window.history.back()
          attempts++
          
          // Wait a bit then check if we're on a restricted page
          setTimeout(() => {
            const currentPath = router.currentRoute.value.path
            if (restrictedPages.includes(currentPath)) {
              goBackSafely() // Keep going back
            }
          }, 100)
        } else {
          // If can't find safe page, go to home
          router.push('/')
        }
      }
      
      goBackSafely()
    } else {
      // No history, go to home
      router.push('/')
    }
  }
  
  return {
    goBack
  }
}
