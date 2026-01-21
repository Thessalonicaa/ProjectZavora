<template>
  <div class="relative min-h-screen bg-gray-950 overflow-hidden">
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
    </div>

    <div class="flex justify-center items-center min-h-screen relative z-10 animate-fade-in">
      <div class="reset-card bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-96 border border-blue-500/40 animate-slide-up">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="inline-block mb-4">
            <div >
              <i class="fas fa-key text-2xl text-white"></i>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-white animate-fadeInDown">
            <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Reset Password
            </span>
          </h1>
        </div>

        <!-- Step 1: Request Token -->
        <div v-if="currentStep === 1" class="space-y-4">
          <div class="input-group">
            <label class="block text-gray-300 text-sm font-semibold mb-2">Username</label>
            <input
              v-model="resetUsername"
              @input="debouncedCheckUsername"
              type="text"
              placeholder="Enter your username"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              required
              @keyup.enter="requestResetToken"
            />
            <p v-if="usernameCheckMsg" :class="['text-xs mt-1', usernameExists ? 'text-green-400' : 'text-red-400']">
              {{ usernameCheckMsg }}
            </p>
          </div>

          <button
            @click="requestResetToken"
            :disabled="!resetUsername || !usernameExists || isLoading"
            class="w-full p-3 rounded-lg bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold shadow-lg hover:shadow-blue-500/50 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {{ isLoading ? 'Requesting...' : 'Next Step' }}
          </button>

          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
            {{ errorMsg }}
          </p>
        </div>

        <!-- Step 2: Update Password -->
        <div v-if="currentStep === 2" class="space-y-4">
          <p class="text-gray-300 text-sm text-center mb-4">
            Enter your new password below.
          </p>

          <div class="input-group">
            <label class="block text-gray-300 text-sm font-semibold mb-2">New Password</label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="New password"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              required
              @keyup.enter="updatePassword"
            />
            <p v-if="passwordError" class="text-red-400 text-xs mt-1">{{ passwordError }}</p>
          </div>

          <div class="input-group">
            <label class="block text-gray-300 text-sm font-semibold mb-2">Confirm Password</label>
            <input
              v-model="confirmPassword"
              type="password"
              placeholder="Confirm password"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              required
              @keyup.enter="updatePassword"
            />
            <p v-if="confirmPasswordError" class="text-red-400 text-xs mt-1">{{ confirmPasswordError }}</p>
          </div>

          <button
            @click="updatePassword"
            :disabled="!newPassword || !confirmPassword || passwordError || confirmPasswordError || isLoading"
            class="w-full p-3 rounded-lg bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white font-semibold shadow-lg hover:shadow-green-500/50 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {{ isLoading ? 'Updating...' : 'Reset Password' }}
          </button>

          <button
            @click="currentStep = 1; errorMsg = ''; resetToken = ''; newPassword = ''; confirmPassword = ''"
            class="w-full p-3 rounded-lg bg-gray-700 hover:bg-gray-600 text-white font-semibold shadow-lg transition-all transform hover:scale-105 active:scale-95"
          >
            <i class="fas fa-arrow-left mr-2"></i>Back
          </button>

          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
            {{ errorMsg }}
          </p>
        </div>

        <!-- Step 3: Success -->
        <div v-if="currentStep === 3" class="text-center space-y-4">
          <div class="inline-block mb-4">
            <div class="w-16 h-16 bg-gradient-to-br from-blue-600 to-blue-700 rounded-full flex items-center justify-center shadow-lg animate-success-icon">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
          </div>

          <h2 class="text-2xl font-bold text-white bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Password Reset Successful!
          </h2>

          <p class="text-gray-300">
            Redirecting to login...
          </p>
        </div>

        <p class="text-center text-sm mt-6 text-gray-300">
          Remember your password?
          <NuxtLink  to="/login" class="text-blue-500 hover:text-blue-400 font-semibold hover:underline transition-colors">
            Login Here
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'

// ✅ Define page meta - allow public access
definePageMeta({
  middleware: []
})

const router = useRouter()
const resetUsername = ref('')
const resetToken = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const currentStep = ref(1)
const usernameCheckMsg = ref('')
const usernameExists = ref(false)
let debounceTimer = null

onMounted(() => {
  // Pre-fill username if passed via route or session
  const storedUsername = sessionStorage.getItem('resetPasswordUsername')
  if (storedUsername) {
    resetUsername.value = storedUsername
  }
})

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})

// ... existing code ...

const passwordError = computed(() => {
  if (!newPassword.value) return ''
  if (newPassword.value.length < 3) return 'Password must be at least 3 characters'
  return ''
})

const confirmPasswordError = computed(() => {
  if (!confirmPassword.value) return ''
  if (newPassword.value !== confirmPassword.value) return 'Passwords do not match'
  return ''
})

const checkUsernameAvailability = async (username) => {
  if (!username) {
    usernameCheckMsg.value = ''
    usernameExists.value = false
    return
  }

  try {
    const response = await fetch(`http://localhost:5000/api/check-username/${username}`)
    const data = await response.json()
    
    if (data.exists) {
      usernameCheckMsg.value = '✓ Username found'
      usernameExists.value = true
    } else {
      usernameCheckMsg.value = '✗ Username not found'
      usernameExists.value = false
    }
  } catch (error) {
    usernameCheckMsg.value = 'Error checking username'
    usernameExists.value = false
  }
}

// Watch for username changes
const debouncedCheckUsername = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    checkUsernameAvailability(resetUsername.value)
  }, 500)
}

const requestResetToken = async () => {
  try {
    errorMsg.value = ''
    isLoading.value = true

    const response = await fetch('http://localhost:5000/api/reset-password/request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: resetUsername.value })
    })

    const data = await response.json()
    console.log('Reset token response:', data)

    if (response.ok && data.success) {
      resetToken.value = data.reset_token
      console.log('Token stored:', resetToken.value)
      currentStep.value = 2
      errorMsg.value = ''
    } else {
      errorMsg.value = data.error || 'Failed to request reset token'
    }
  } catch (error) {
    errorMsg.value = 'Error requesting reset token'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const updatePassword = async () => {
  try {
    if (passwordError.value || confirmPasswordError.value) {
      return
    }

    errorMsg.value = ''
    isLoading.value = true

    console.log('Sending data:', {
      username: resetUsername.value,
      reset_token: resetToken.value,
      new_password: newPassword.value
    })

    const response = await fetch('http://localhost:5000/api/reset-password/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: resetUsername.value,
        reset_token: resetToken.value,
        new_password: newPassword.value
      })
    })

    const data = await response.json()
    console.log('Response:', data)

    if (response.ok && data.success) {
      currentStep.value = 3
      // ✅ Auto redirect to login immediately after success
      setTimeout(() => {
        goToLogin()
      }, 1500)
    } else {
      errorMsg.value = data.error || 'Failed to update password'
    }
  } catch (error) {
    errorMsg.value = 'Error updating password'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const startRedirectCountdown = () => {
  redirectCountdown.value = 5
  redirectTimer = setInterval(() => {
    redirectCountdown.value--
    if (redirectCountdown.value <= 0) {
      clearInterval(redirectTimer)
      goToLogin()
    }
  }, 1000)
}

const goToLogin = () => {
  sessionStorage.removeItem('resetPasswordUsername')
  router.push('/login')
}
</script>

<style scoped>
.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.6;
}

.reset-card {
  animation: fadeInUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
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

@keyframes successIcon {
  0% {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  50% {
    transform: scale(1.3) rotate(10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
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

.animate-success-icon {
  animation: successIcon 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>
