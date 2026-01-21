// filepath: e:\ProjectFainal\frontend\composables\useLogout.js
import { useRouter } from 'vue-router'

export const useLogout = () => {
  const router = useRouter()

  const logout = () => {
    // Clear all localStorage data
    localStorage.removeItem('token')
    localStorage.removeItem('user_id')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
    localStorage.removeItem('is_seller')
    localStorage.removeItem('is_admin')
    localStorage.removeItem('app_initialized')

    // Clear sessionStorage
    sessionStorage.removeItem('zavora_loader_shown')
    sessionStorage.removeItem('just_logged_in')

    // Force redirect to login
    window.location.href = '/login'
  }

  return {
    logout
  }
}
