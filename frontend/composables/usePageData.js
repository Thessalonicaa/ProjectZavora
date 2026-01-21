// filepath: e:\ProjectFainal\frontend\composables/usePageData.js
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export const usePageData = (fetchFunction) => {
  const route = useRoute()
  const loading = ref(false)
  const error = ref(null)

  // Watch route to refetch data
  watch(
    () => route.path,
    async () => {
      loading.value = true
      error.value = null
      try {
        await fetchFunction()
      } catch (err) {
        error.value = err.message
        console.error('Error fetching page data:', err)
      } finally {
        loading.value = false
      }
    },
    { immediate: true }
  )

  // Also watch query params
  watch(
    () => route.query,
    async () => {
      loading.value = true
      error.value = null
      try {
        await fetchFunction()
      } catch (err) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    }
  )

  return {
    loading,
    error,
    refetch: fetchFunction
  }
}