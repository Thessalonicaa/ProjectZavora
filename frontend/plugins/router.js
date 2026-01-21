// filepath: e:\ProjectFainal\frontend\plugins/router.js
export default defineNuxtPlugin((nuxtApp) => {
  const router = useRouter()

  // Force data refresh on route change
  router.afterEach((to, from) => {
    // Clear any cached data that might be stale
    if (to.path !== from.path) {
      // Refresh page data by triggering component re-render
      nuxtApp.$refresh?.()
    }
  })

  router.beforeEach((to, from, next) => {
    // Ensure we're not using stale data
    if (to.name !== from.name) {
      // Different page, make sure to refetch
      next()
    } else {
      next()
    }
  })
})