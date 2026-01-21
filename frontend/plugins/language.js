import { useLanguage } from '~/composables/useLanguage'

export default defineNuxtPlugin(() => {
  const { initLanguage, t } = useLanguage()
  
  // Initialize language on app load
  if (process.client) {
    initLanguage()
  }
  
  return {
    provide: {
      t // Make $t available globally
    }
  }
})