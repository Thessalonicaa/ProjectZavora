<!-- pages/Register.vue -->
<template>
  <div class="min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
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
    </div>

    <ZavoraLoader v-if="showLoader" @complete="showLoader = false" />
    <div v-if="!showLoader" class="relative min-h-screen flex items-center justify-center bg-gray-950 overflow-hidden">
      <div class="flex justify-center items-center min-h-screen w-full relative z-10 animate-fade-in">
        <div class="register-card bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-96 border border-red-500/40 animate-slide-up">
          <h1 class="text-3xl font-bold mb-6 text-center text-white animate-fadeInDown">
            <span class="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 bg-clip-text text-transparent">
              Register
            </span>
          </h1>

          <form @submit.prevent="handleRegister" class="space-y-4">
            <div class="input-group">
              <input
                v-model="username"
                @input="debouncedCheckUsername"
                placeholder="Username"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              />
              <p v-if="usernameCheckMsg" :class="['text-xs mt-1', usernameAvailable ? 'text-green-400' : 'text-red-400']">
                {{ usernameCheckMsg }}
              </p>
            </div>

            <div class="input-group">
              <input
                v-model="password"
                type="password"
                placeholder="Password"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              />
              <p v-if="passwordError" class="text-red-400 text-xs mt-1">{{ passwordError }}</p>
            </div>

            <div class="input-group">
              <input
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm Password"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              />
              <p v-if="confirmPasswordError" class="text-red-400 text-xs mt-1">{{ confirmPasswordError }}</p>
            </div>

            <button
              type="submit"
              :disabled="!isFormValid"
              class="w-full p-3 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              Register
            </button>
          </form>

          <p class="text-center text-sm mt-6 text-gray-300">
            Already have an account?
            <router-link to="/login" class="text-orange-500 hover:text-orange-400 font-semibold hover:underline transition-colors">
              Login
            </router-link>
          </p>

          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
            {{ errorMsg }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'
import ZavoraLoader from '~/components/ZavoraLoader.vue'

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const showLoader = ref(true)
const router = useRouter()
const usernameCheckMsg = ref('')
const usernameAvailable = ref(false)
let debounceTimer = null

onMounted(() => {
  if (sessionStorage.getItem('zavora_loader_shown')) showLoader.value = false
  else sessionStorage.setItem('zavora_loader_shown', 'true')
})

// ✅ Password validation
const passwordError = computed(() => {
  if (!password.value) return ''
  if (password.value.length < 3) return 'Password must be at least 3 characters'
  return ''
})

const confirmPasswordError = computed(() => {
  if (!confirmPassword.value) return ''
  if (password.value !== confirmPassword.value) return 'Passwords do not match'
  return ''
})

// ✅ Form validation
const isFormValid = computed(() => {
  return (
    username.value &&
    usernameAvailable.value &&
    password.value &&
    confirmPassword.value &&
    !passwordError.value &&
    !confirmPasswordError.value
  )
})

const handleRegister = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = 'Please fill all fields'
    return
  }
  
  // ✅ Check if username is available before registering
  if (!usernameAvailable.value) {
    errorMsg.value = 'Username is not available'
    return
  }
  
  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match'
    return
  }

  try {
    const response = await fetch('http://localhost:5000/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
        role: 'user'
      })
    })

    const data = await response.json()

    if (response.ok || data?.msg || data?.success) {
      router.push('/login')
      return
    } else {
      errorMsg.value = data.message || 'มีข้อผิดพลาดในการลงทะเบียน กรุณาลองใหม่อีกครั้งในภายหลัง'
    }
  } catch (error) {
    console.error('Registration error:', error)
    errorMsg.value = 'เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์'
  }
}

// ✅ Check username availability
const checkUsername = async (usernameValue) => {
  if (!usernameValue || usernameValue.trim().length < 2) {
    usernameCheckMsg.value = ''
    usernameAvailable.value = false
    return
  }

  try {
    const response = await fetch(
      `http://localhost:5000/api/check-username/${encodeURIComponent(usernameValue.trim())}`
    )
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.exists) {
      usernameCheckMsg.value = '❌ Username already taken'
      usernameAvailable.value = false
    } else {
      usernameCheckMsg.value = '✓ Username is available'
      usernameAvailable.value = true
    }
  } catch (error) {
    console.error('Username check error:', error)
    // Fallback: allow user to continue
    usernameCheckMsg.value = '✓ Username is available'
    usernameAvailable.value = true
  }
}

// ✅ Debounce username check
const debouncedCheckUsername = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    checkUsername(username.value)
  }, 500)
}
</script>

<style scoped>
.register-page {
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
  z-index: 1;
}

.register-card {
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

.input-group:nth-child(3) {
  animation-delay: 0.2s;
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
