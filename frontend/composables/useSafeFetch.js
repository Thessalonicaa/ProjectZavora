// filepath: e:\ProjectFainal\frontend\composables\useSafeFetch.js
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

/**
 * Safe data fetching hook that prevents "Cannot access before initialization" errors
 * @param {Function} fetchFunction - Async function to fetch data
 * @param {Object} options - Optional configuration
 * @returns {Object} - { loading, error, data, refetch }
 */
export const useSafeFetch = (fetchFunction, options = {}) => {
  const route = useRoute()
  const loading = ref(false)
  const error = ref(null)
  const data = ref(options.initialData || null)
  
  // Safe wrapper for fetch function
  const safeFetch = async () => {
    loading.value = true
    error.value = null
    try {
      await fetchFunction()
    } catch (err) {
      error.value = err.message || 'An error occurred'
      console.error('Fetch error:', err)
    } finally {
      loading.value = false
    }
  }
  
  // Watch route ONLY if specified
  if (options.watchRoute !== false) {
    watch(() => route.path, safeFetch, { immediate: false })
  }
  
  // Call on mount
  if (options.onMount !== false) {
    safeFetch()
  }
  
  return {
    loading,
    error,
    data,
    refetch: safeFetch
  }
}
