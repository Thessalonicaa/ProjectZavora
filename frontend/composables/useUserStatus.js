import { ref, onMounted, onBeforeUnmount } from 'vue'

export const useUserStatus = () => {
  const isOnline = ref(true)
  const userStatus = ref('online') // 'online', 'away', 'offline'
  let inactivityTimer = null
  let awayTimer = null
  let offlineTimer = null

  const updateLastActivity = () => {
    // Reset timers
    if (inactivityTimer) clearTimeout(inactivityTimer)
    if (awayTimer) clearTimeout(awayTimer)
    if (offlineTimer) clearTimeout(offlineTimer)

    // Set as online
    isOnline.value = true
    userStatus.value = 'online'

    // After 3 minutes of inactivity, set to 'away'
    inactivityTimer = setTimeout(() => {
      userStatus.value = 'away'
      console.log('User is away')
    }, 3 * 60 * 1000) // 3 minutes

    // After 10 minutes of inactivity, set to 'offline'
    offlineTimer = setTimeout(() => {
      userStatus.value = 'offline'
      isOnline.value = false
      console.log('User is offline')
    }, 10 * 60 * 1000) // 10 minutes
  }

  const handleUserActivity = () => {
    updateLastActivity()
  }

  onMounted(() => {
    // Set initial status
    updateLastActivity()

    // Listen to user activity
    window.addEventListener('mousemove', handleUserActivity)
    window.addEventListener('keypress', handleUserActivity)
    window.addEventListener('click', handleUserActivity)
    window.addEventListener('scroll', handleUserActivity)
  })

  onBeforeUnmount(() => {
    // Clean up timers
    if (inactivityTimer) clearTimeout(inactivityTimer)
    if (awayTimer) clearTimeout(awayTimer)
    if (offlineTimer) clearTimeout(offlineTimer)

    // Remove event listeners
    window.removeEventListener('mousemove', handleUserActivity)
    window.removeEventListener('keypress', handleUserActivity)
    window.removeEventListener('click', handleUserActivity)
    window.removeEventListener('scroll', handleUserActivity)
  })

  return {
    isOnline,
    userStatus // 'online' (green), 'away' (yellow), 'offline' (gray)
  }
}