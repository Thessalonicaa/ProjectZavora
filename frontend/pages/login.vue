<template>
  <div>
    <!-- ZAVORA Loader -->
    <ZavoraLoader v-if="showLoader" @complete="showLoader = false" />
    
    <div v-if="!showLoader" class="relative min-h-screen flex items-center justify-center bg-gray-950 overflow-hidden">
    <!-- Beams Background -->
    <div class="beams-background">
      <Beams
        :beamWidth="3"
        :beamHeight="25"
        :beamNumber="20"
        lightColor="#ff3c03"
        :speed="2"
        :noiseIntensity="1.75"
        :scale="0.2"
        :rotation="30"
        :width="1920"
        :height="1080"
      />
      <div class="beams-gradient-overlay"></div>
    </div>

    <div class="flex justify-center items-center min-h-screen w-full relative z-10 animate-fade-in">
      <div class="login-card bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-96 border border-red-500/40 animate-slide-up">
        <h1 class="text-3xl font-bold mb-6 text-center text-white animate-fadeInDown">
          <span class="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 bg-clip-text text-transparent">
            Login
          </span>
        </h1>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="input-group">
            <input
              v-model="username"
              type="text"
              placeholder="Username"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              required
              @keyup.enter="handleLogin"
            />
            <p v-if="usernameError" class="text-red-400 text-xs mt-1">{{ usernameError }}</p>
          </div>

          <div class="input-group">
            <input
              v-model="password"
              type="password"
              placeholder="Password"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              required
              @keyup.enter="handleLogin"
            />
            <p v-if="passwordError" class="text-red-400 text-xs mt-1">{{ passwordError }}</p>
          </div>

          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
            class="w-full p-3 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <p class="text-center text-sm mt-6 text-gray-300">
          Don't have an account?
          <NuxtLink to="/register" class="text-orange-500 hover:text-orange-400 font-semibold hover:underline transition-colors">
            Register
          </NuxtLink>
        </p>

        <p class="text-center text-sm mt-3 text-gray-300">
          Forgot your password?
          <NuxtLink to="/reset-password" class="text-blue-500 hover:text-blue-400 font-semibold hover:underline transition-colors">
            Reset it here
          </NuxtLink>
        </p>

        <p v-if="error" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
          {{ error }}
        </p>
      </div>
      </div>
    </div>
  </div>
</template><script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'
import ZavoraLoader from '~/components/ZavoraLoader.vue'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const showLoader = ref(true)
const isLoading = ref(false)

onMounted(() => {
  if (sessionStorage.getItem('zavora_loader_shown')) showLoader.value = false
  else sessionStorage.setItem('zavora_loader_shown', 'true')
})

// ✅ Username validation
const usernameError = computed(() => {
  if (!username.value) return ''
  if (username.value.length < 2) return 'Username must be at least 2 characters'
  return ''
})

// ✅ Password validation
const passwordError = computed(() => {
  if (!password.value) return ''
  if (password.value.length < 3) return 'Password must be at least 3 characters'
  return ''
})

// ✅ Form validation
const isFormValid = computed(() => {
  return (
    username.value &&
    password.value &&
    !usernameError.value &&
    !passwordError.value
  )
})

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('token', data.token)
      localStorage.setItem('user_id', data.user_id)
      localStorage.setItem('username', data.username)
      localStorage.setItem('role', data.role)
      localStorage.setItem('is_seller', data.is_seller || (data.role === 'seller' ? 'true' : 'false'))
      localStorage.setItem('is_admin', data.is_admin || false)

      // Redirect based on role
      if (data.role === 'admin' || data.is_admin) {
        router.push('/admin')
      } else if (data.is_seller || data.role === 'seller') {
        router.push('/seller/PostCar')
      } else {
        router.push('/dashboard')
      }
    } else {
      console.log('Error response:', data)
      if (data.error.includes('ชื่อผู้ใช้') && data.error.includes('รหัสผ่าน')) {
        error.value = 'ชื่อผู้ใช้และรหัสผ่านไม่ถูกต้อง'
      } else if (data.error.includes('ชื่อผู้ใช้')) {
        error.value = 'ชื่อผู้ใช้ไม่ถูกต้อง'
      } else if (data.error.includes('รหัสผ่าน')) {
        error.value = 'รหัสผ่านไม่ถูกต้อง'
      } else {
        error.value = data.error || 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ'
      }
    }
  } catch (err) {
    error.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์'
    console.error('Login error:', err)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.6;
}

.beams-gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0.7) 100%);
  pointer-events: none;
}

.login-card {
  animation: fadeInUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3), 0 8px 16px rgba(0, 0, 0, 0.2);
}

.input-group {
  animation: fadeInLeft 0.6s ease-out;
}

.input-group:nth-child(2) {
  animation-delay: 0.1s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.animate-fadeInDown {
  animation: fadeInDown 0.8s ease-out;
}

.animate-shake {
  animation: shake 0.5s ease-in-out;
}

.animate-fade-in {
  animation: fadeIn 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.animate-slide-up {
  animation: slideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>