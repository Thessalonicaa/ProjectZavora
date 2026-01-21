// filepath: e:\ProjectFainal\frontend\middleware\navigationGuard.js
export default defineNuxtRouteMiddleware((to, from) => {
  // Pages that should not be in browser history
  const restrictedPages = ['/login', '/register', '/register-seller', '/reset-password']

  // If trying to navigate to a restricted page, clear history
  if (restrictedPages.includes(to.path)) {
    // This will be handled by the back button logic
  }
})
