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
    <div class="register-seller-page animate-fade-in">
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

      <div class="flex justify-center items-center min-h-screen bg-black relative z-10">
        <div class="register-seller-card bg-gradient-to-br from-gray-900/90 via-gray-800/90 to-gray-900/90 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-[450px] text-black border border-gray-700/50">
          <h1 class="text-3xl font-bold mb-6 text-center text-white animate-fadeInDown">
            <span class="bg-gradient-to-r from-orange-500 via-red-500 to-orange-500 bg-clip-text text-transparent">
              Register as Seller
            </span>
          </h1>

          <form @submit.prevent="handleRegister" class="space-y-4">
            <div class="input-group">
              <input
                v-model="username"
                type="text"
                placeholder="Username"
                class="w-full p-3 border border-gray-600 bg-gray-700/50 text-gray-400 rounded-lg cursor-not-allowed"
                readonly
              />
            </div>

            <div class="input-group">
              <input
                v-model="email"
                type="email"
                placeholder="Email"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
                required
              />
              <p v-if="emailError" class="text-red-400 text-xs mt-1">{{ emailError }}</p>
            </div>

            <div class="input-group">
              <input
                v-model="shopName"
                @input="debouncedCheckShopName"
                type="text"
                placeholder="Shop Name"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
                required
              />
              <p v-if="shopNameCheckMsg" :class="['text-xs mt-1', shopNameAvailable ? 'text-green-400' : 'text-red-400']">
                {{ shopNameCheckMsg }}
              </p>
            </div>

            <div class="input-group">
              <input
                v-model="phone"
                type="text"
                placeholder="Phone Number"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400"
              />
              <p v-if="phoneError" class="text-red-400 text-xs mt-1">{{ phoneError }}</p>
            </div>

            <div class="input-group">
              <textarea
                v-model="address"
                placeholder="Address"
                rows="3"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-300 placeholder-gray-400 resize-none"
                required
              ></textarea>
              <p v-if="addressError" class="text-red-400 text-xs mt-1">{{ addressError }}</p>
            </div>

            <button
              type="submit"
              class="w-full p-3 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-semibold shadow-lg hover:shadow-orange-500/50 transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
              :disabled="!isFormValid"
            >
              Register as Seller
            </button>
          </form>

          <p class="text-center text-sm mt-6 text-gray-300">
            Already have an account?
            <NuxtLink to="/login" class="text-orange-500 hover:text-orange-400 font-semibold hover:underline transition-colors">
              Login
            </NuxtLink>
          </p>

          <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center bg-red-900/20 p-3 rounded-lg border border-red-500/30 animate-shake">
            {{ errorMsg }}
          </p>
        </div>
      </div>

      <!-- Success Modal -->
      <template v-if="showSuccessModal">
        <div
          class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm"
          @click="redirectNow"
        >
          <div
            @click.stop
            class="success-modal bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8 rounded-2xl text-center max-w-md w-full mx-4 border border-orange-500/30 shadow-2xl"
          >
            <div class="success-icon mb-4">
              <svg class="w-20 h-20 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 class="text-white text-2xl font-bold mb-2">
              ลงทะเบียนผู้ขายสำเร็จ
            </h3>
            <p class="text-gray-300 mb-4">
              ระบบจะพาไปหน้าเข้าสู่ระบบในอีก <span class="text-orange-500 font-bold text-xl">{{ countdown }}</span> วินาที
            </p>
            <div class="countdown-bar">
              <div class="countdown-progress" :style="{ width: `${(countdown / 5) * 100}%` }"></div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import Beams from '~/components/Beams.vue'

const router = useRouter()
const username = ref('')
const email = ref('')
const shopName = ref('')
const phone = ref('')
const address = ref('')
const errorMsg = ref('')
const showSuccessModal = ref(false)
const countdown = ref(5)
const shopNameCheckMsg = ref('')
const shopNameAvailable = ref(false)
let debounceTimer = null
let countdownInterval = null
let redirectTimeout = null

onMounted(() => {
  const storedUsername = localStorage.getItem('username')
  if (storedUsername) username.value = storedUsername

  window.addEventListener('keydown', handleEnter)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleEnter)
  clearInterval(countdownInterval)
  clearTimeout(redirectTimeout)
  if (debounceTimer) clearTimeout(debounceTimer)
})

const handleEnter = (e) => {
  if (e.key === 'Enter') {
    handleRegister()
  }
}

// ✅ Email validation
const emailError = computed(() => {
  if (!email.value) return ''
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) return 'Invalid email format'
  return ''
})

// ✅ Phone validation
const phoneError = computed(() => {
  if (!phone.value) return ''
  if (phone.value.length < 7) return 'Phone number must be at least 7 digits'
  if (!/^\d+$/.test(phone.value)) return 'Phone number must contain only numbers'
  return ''
})

// ✅ Address validation
const addressError = computed(() => {
  if (!address.value) return ''
  if (address.value.trim().length < 5) return 'Address must be at least 5 characters'
  return ''
})

// ✅ Form validation
const isFormValid = computed(() => {
  return (
    username.value &&
    email.value &&
    shopName.value &&
    shopNameAvailable.value &&
    address.value &&
    !emailError.value &&
    !phoneError.value &&
    !addressError.value
  )
})

// ✅ Check shop name availability
const checkShopName = async (shopNameValue) => {
  if (!shopNameValue || shopNameValue.trim().length < 2) {
    shopNameCheckMsg.value = ''
    shopNameAvailable.value = false
    return
  }

  try {
    const response = await fetch(
      `http://localhost:5000/api/check-shop-name/${encodeURIComponent(shopNameValue.trim())}`
    )
    
    if (!response.ok) {
      if (response.status === 404) {
        shopNameCheckMsg.value = '✓ Shop name is available'
        shopNameAvailable.value = true
        return
      }
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.exists) {
      shopNameCheckMsg.value = '❌ This shop name is already taken'
      shopNameAvailable.value = false
    } else {
      shopNameCheckMsg.value = '✓ Shop name is available'
      shopNameAvailable.value = true
    }
  } catch (error) {
    console.error('Shop name check error:', error)
    // Fallback: allow user to continue
    shopNameCheckMsg.value = '✓ Shop name is available'
    shopNameAvailable.value = true
  }
}

// ✅ Debounce shop name check
const debouncedCheckShopName = () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    checkShopName(shopName.value)
  }, 500)
}

const handleRegister = async () => {
  try {
    if (!isFormValid.value) {
      errorMsg.value = 'Please fill all required fields and ensure they are valid.'
      return
    }

    const token = localStorage.getItem('token')
    if (!token) {
      errorMsg.value = 'You must be logged in to register as a seller.'
      return
    }

    const response = await axios.post(
      'http://localhost:5000/api/auth/register/seller',
      {
        email: email.value,
        business_name: shopName.value,
        contact_info: address.value,
        phonenumber: phone.value,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )

    if (response.status === 201) {
      showSuccessModal.value = true
      countdown.value = 5

      countdownInterval = setInterval(() => {
        countdown.value = Math.max(0, countdown.value - 1)
      }, 1000)

      redirectTimeout = setTimeout(() => {
        router.push('/login')
      }, 5000)
    } else {
      errorMsg.value = response.data.message || 'Registration failed'
    }
  } catch (error) {
    console.error('Registration error:', error.response?.data)
    errorMsg.value =
      error.response?.data?.message ||
      'There was an error during registration. Please try again.'
  }
}

const redirectNow = () => {
  clearInterval(countdownInterval)
  clearTimeout(redirectTimeout)
  router.push('/login')
}
</script>

<style scoped>
.register-seller-page {
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

.register-seller-card {
  animation: fadeInUp 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.input-group {
  animation: fadeInLeft 0.6s ease-out;
}

.input-group:nth-child(2) { animation-delay: 0.1s; }
.input-group:nth-child(3) { animation-delay: 0.2s; }
.input-group:nth-child(4) { animation-delay: 0.3s; }
.input-group:nth-child(5) { animation-delay: 0.4s; }

.success-modal {
  animation: modalPop 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.success-icon svg {
  animation: checkPop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.2s both;
}

.countdown-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 1rem;
}

.countdown-progress {
  height: 100%;
  background: linear-gradient(90deg, #ff3c03, #ff8c00);
  border-radius: 3px;
  transition: width 1s linear;
  box-shadow: 0 0 10px rgba(255, 60, 3, 0.8);
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

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes checkPop {
  from {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
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
</style>
