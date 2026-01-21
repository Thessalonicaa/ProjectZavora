<template>
  <div class="min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
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

    <div class="max-w-6xl mx-auto relative z-10">
      <!-- Header -->
      <div class="mb-12">
        <div class="flex items-center gap-4 mb-4">
          <button 
            @click="goBack"
            class="group relative inline-flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-br border-red-500/50 hover:border-red-400 hover:from-red-600/40 hover:to-red-700/40 transition-all duration-300 shadow-lg hover:shadow-red-500/30"
            title="Go back"
          >
            <i class="fas fa-arrow-left text-red-500 group-hover:text-red-400 group-hover:-translate-x-1 transition-all duration-300"></i>
          </button>
          
          <NuxtLink 
            to="/CarList" 
            class="inline-flex items-center gap-2 text-red-500 hover:text-red-400 font-semibold group transition-all duration-300"
          >
            <span class="relative overflow-hidden">
              <span class="absolute inset-0 flex items-center translate-x-full group-hover:translate-x-0 transition-transform duration-300 text-red-400">
                <i class="fas fa-arrow-right ml-2"></i> {{ currentLanguage === 'th' ? 'เรียกดูเพิ่มเติม' : 'Browse More' }}
              </span>
            </span>
          </NuxtLink>
        </div>
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2">
          {{ currentLanguage === 'th' ? 'เครื่องคิดเลขผ่อนชำระ' : 'Installment Calculator' }}
        </h1>
        <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'คำนวณการชำระเงินรายเดือนของคุณได้อย่างง่ายดาย' : 'Calculate your monthly payment easily' }}</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Left Side - Calculator Form -->
        <div class="space-y-6">
          <div class="bg-gradient-to-br from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl">
            
            <!-- Car Items Summary -->
            <div class="mb-8">
              <h2 class="text-2xl font-bold mb-4 flex items-center gap-3">
                <i class="fas fa-car text-red-500 text-2xl"></i>
                {{ currentLanguage === 'th' ? 'รายการรถในตะกร้า' : 'Cart Items' }} ({{ cartItems.length }})
              </h2>
              <div class="space-y-3 max-h-40 overflow-y-auto">
                <div v-for="(item, index) in cartItems" :key="index" class="bg-gray-800/50 p-3 rounded-lg border border-gray-700 hover:border-red-500/30 transition-all group">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="font-bold text-white">{{ item.brand }} {{ item.model }}</p>
                      <p class="text-xs text-gray-400">{{ item.year }} • ฿{{ formatPrice(item.price) }}</p>
                    </div>
                    <button 
                      @click="removeFromCart(index)"
                      class="opacity-0 group-hover:opacity-100 transition-opacity p-2 text-red-500 hover:text-red-400"
                      title="Remove"
                    >
                      <i class="fas fa-trash-alt"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Price Input -->
            <div class="mb-6">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-2 block">{{ currentLanguage === 'th' ? 'ราคารวม' : 'Total Price' }} (฿)</label>
              <div class="flex items-center gap-2">
                <span class="text-red-500 font-bold text-xl">฿</span>
                <input
                  v-model.number="totalPrice"
                  type="number"
                  disabled
                  class="flex-1 px-4 py-3 rounded-xl bg-gray-700 border border-gray-600 text-gray-300 text-lg focus:outline-none font-semibold cursor-not-allowed"
                  placeholder="Auto-calculated"
                />
              </div>
              <p class="text-xs text-gray-500 mt-2">{{ currentLanguage === 'th' ? 'อัตโนมัติคำนวณจากรายการรถ' : 'Auto-calculated from cart items' }}</p>
            </div>

            <!-- Down Payment Input & Percentage -->
            <div class="mb-6">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-3 block">{{ currentLanguage === 'th' ? 'เงินดาวน์' : 'Down Payment' }}</label>
              <div class="flex gap-3">
                <div class="flex-1 flex items-center gap-2">
                  <span class="text-red-500 font-bold text-xl">฿</span>
                  <input
                    v-model.number="downPayment"
                    type="number"
                    class="flex-1 px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white text-lg focus:outline-none focus:ring-2 focus:ring-red-500 font-semibold"
                    placeholder="Enter amount"
                    @input="updatePercentFromAmount"
                  />
                </div>
                <div class="w-24">
                  <input
                    v-model.number="downPaymentPercent"
                    type="number"
                    class="w-full px-4 py-3 rounded-xl bg-gray-800 border border-gray-700 text-white text-lg focus:outline-none focus:ring-2 focus:ring-red-500 font-semibold"
                    placeholder="%"
                    @input="updateAmountFromPercent"
                  />
                </div>
                <span class="text-gray-400 text-lg">%</span>
              </div>
              <!-- Warning / Error Message -->
              <div v-if="downPaymentPercent > 0 && downPaymentPercent < 10" class="mt-2 flex items-center gap-2 p-3 bg-red-600/20 border border-red-500/50 rounded-lg">
                <i class="fas fa-times-circle text-red-400"></i>
                <p class="text-red-400 text-xs font-semibold">{{ currentLanguage === 'th' ? '❌ เงินดาวน์ต้องไม่น้อยกว่า 10%' : '❌ Down payment must be at least 10%' }}</p>
              </div>
              <div v-else-if="downPaymentPercent >= 10" class="mt-2 flex items-center gap-2 p-3 bg-green-600/20 border border-green-500/50 rounded-lg">
                <i class="fas fa-check-circle text-green-400"></i>
                <p class="text-green-400 text-xs font-semibold">{{ currentLanguage === 'th' ? '✅ เงินดาวน์ถูกต้อง (ขั้นต่ำ: 10% | สูงสุด: 100%)' : '✅ Valid down payment (Min: 10% | Max: 100%)' }}</p>
              </div>
              <p v-else class="text-xs text-gray-500 mt-2">{{ currentLanguage === 'th' ? 'ขั้นต่ำ: 10% | สูงสุด: 100%' : 'Min: 10% | Max: 100%' }}</p>
            </div>

            <!-- Interest Rate -->
            <div class="mb-6">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-2 block">{{ currentLanguage === 'th' ? 'อัตราดอกเบี้ย (%) - อัตโนมัติ' : 'Interest Rate (%) - Auto' }}</label>
              <div class="space-y-3">
                <div class="flex items-center gap-2">
                  <input
                    v-model.number="interestRate"
                    type="number"
                    step="0.1"
                    min="0"
                    disabled
                    class="flex-1 px-4 py-3 rounded-xl bg-gray-700 border border-gray-600 text-gray-300 text-lg focus:outline-none font-semibold cursor-not-allowed"
                    placeholder="Auto-calculated"
                  />
                  <span class="text-gray-400 text-lg">%</span>
                </div>
                <!-- Interest Rate Increment Info -->
                <div class="p-3 bg-blue-600/20 border border-blue-500/30 rounded-lg">
                  <p class="text-blue-300 text-xs font-semibold flex items-center gap-2">
                    <i class="fas fa-info-circle"></i>
                    {{ currentLanguage === 'th' ? 'อัตราดอกเบี้ยเพิ่มขึ้น 5% ต่อปี' : 'Interest rate increases 5% per year' }}
                  </p>
                  <p class="text-blue-200 text-xs mt-1">
                    {{ currentLanguage === 'th' ? 'ปี 1 (1-12 เดือน)' : 'Year 1 (1-12 mo)' }}: {{ (baseInterestRate).toFixed(1) }}% 
                    <span class="text-gray-400">→</span> 
                    {{ currentLanguage === 'th' ? 'ปี 2 (13-24 เดือน)' : 'Year 2 (13-24 mo)' }}: {{ (baseInterestRate * 1.05).toFixed(1) }}% 
                    <span class="text-gray-400">→</span> 
                    {{ currentLanguage === 'th' ? 'ปี 3 (25-36 เดือน)' : 'Year 3 (25-36 mo)' }}: {{ (baseInterestRate * 1.1025).toFixed(1) }}%
                  </p>
                  <p class="text-green-300 text-xs mt-2 font-bold">
                    📊 {{ currentLanguage === 'th' ? 'ปัจจุบัน' : 'Current' }}: {{ interestRate.toFixed(2) }}% ({{ Math.floor(duration / 12) + 1 }} year{{ Math.floor(duration / 12) > 0 ? 's' : '' }})
                  </p>
                </div>
              </div>
            </div>

            <!-- Duration -->
            <div class="mb-8">
              <label class="text-gray-400 text-sm uppercase font-semibold mb-3 block">{{ currentLanguage === 'th' ? 'ระยะเวลา (เดือน)' : 'Duration (Months)' }}</label>
              <div class="flex items-center gap-4">
                <span class="text-white font-bold text-lg min-w-fit">{{ duration }} {{ currentLanguage === 'th' ? 'เดือน' : 'months' }}</span>
                <input
                  v-model.number="duration"
                  type="range"
                  min="1"
                  max="60"
                  class="flex-1 h-2 rounded-lg appearance-none cursor-pointer duration-slider"
                  :style="{ '--slider-value': (duration / 60) * 100 + '%' }"
                />
              </div>
              <p class="text-xs text-gray-500 mt-2">{{ currentLanguage === 'th' ? '1 - 60 เดือน' : '1 - 60 months' }}</p>
            </div>

            <!-- Calculate Button -->
            <button
              @click="calculatePayment"
              class="w-full py-4 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-500/50 flex items-center justify-center gap-2 text-lg"
            >
              <i class="fas fa-calculator mr-2"></i>{{ currentLanguage === 'th' ? 'คำนวณ' : 'Calculate' }}
            </button>
          </div>
        </div>

        <!-- Right Side - Result Circular Display -->
        <div class="space-y-6">
          <!-- Result Card with Circular Display -->
          <div class="bg-gradient-to-br from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 shadow-2xl">
            <h2 class="text-2xl font-bold mb-8 text-center">{{ currentLanguage === 'th' ? 'ผลลัพธ์' : 'Result' }}</h2>

            <!-- Circular Progress Display -->
            <div class="flex items-center justify-center mb-8">
              <div class="relative w-64 h-64">
                <!-- Outer Circle -->
                <svg class="w-full h-full" viewBox="0 0 200 200">
                  <!-- Background Circle -->
                  <circle cx="100" cy="100" r="95" fill="none" stroke="#374151" stroke-width="2"/>
                  
                  <!-- Progress Circle with Gradient -->
                  <defs>
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style="stop-color:#dc2626;stop-opacity:1" />
                      <stop offset="100%" style="stop-color:#16a34a;stop-opacity:1" />
                    </linearGradient>
                  </defs>
                  <circle 
                    cx="100" 
                    cy="100" 
                    r="95" 
                    fill="none" 
                    stroke="url(#progressGradient)" 
                    stroke-width="3"
                    stroke-dasharray="596"
                    :stroke-dashoffset="596 - (downPaymentPercent / 100) * 596"
                    stroke-linecap="round"
                    class="transition-all duration-500"
                    style="transform: rotate(-90deg); transform-origin: 100px 100px;"
                  />
                </svg>

                <!-- Center Content -->
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                  <p class="text-gray-400 text-xs uppercase font-bold tracking-wider mb-2">{{ currentLanguage === 'th' ? 'การชำระเงินรายเดือน' : 'Monthly Payment' }}</p>
                  <p class="text-5xl font-extrabold text-red-500 drop-shadow-lg">{{ formatPrice(monthlyPayment) }}</p>
                  <p class="text-gray-400 text-xs mt-2">฿ / {{ currentLanguage === 'th' ? 'เดือน' : 'Month' }}</p>
                </div>
              </div>
            </div>

            <!-- Result Summary -->
            <div class="space-y-3 pt-6 border-t border-gray-700">
              <!-- Down Payment -->
              <div class="flex items-center justify-between p-4 bg-gradient-to-r from-red-600/20 to-red-800/10 rounded-xl border border-red-500/30 group hover:border-red-500/60 transition-all">
                <div class="flex items-center gap-3">
                  <div class="w-3 h-3 rounded-full bg-red-500"></div>
                  <span class="text-gray-400 text-sm uppercase font-bold">{{ currentLanguage === 'th' ? 'เงินดาวน์' : 'Down Payment' }}</span>
                </div>
                <span class="text-red-400 font-bold text-lg">฿{{ formatPrice(downPayment) }}</span>
              </div>

              <!-- Remaining Amount -->
              <div class="flex items-center justify-between p-4 bg-gray-800/50 rounded-xl border border-gray-700 group hover:border-blue-500/50 transition-all">
                <span class="text-gray-400 text-sm uppercase font-bold">{{ currentLanguage === 'th' ? 'ยอดคงเหลือ' : 'Remaining' }}</span>
                <span class="text-blue-400 font-bold text-lg">฿{{ formatPrice(totalPrice - downPayment) }}</span>
              </div>

              <!-- Monthly Payment -->
              <div class="flex items-center justify-between p-4 bg-gradient-to-r from-blue-600/20 to-blue-800/10 rounded-xl border border-blue-500/30 group hover:border-blue-500/60 transition-all">
                <span class="text-gray-400 text-sm uppercase font-bold">{{ currentLanguage === 'th' ? 'การชำระเงินรายเดือน' : 'Monthly Payment' }}</span>
                <span class="text-blue-400 font-bold text-lg">฿{{ formatPrice(monthlyPayment) }}</span>
              </div>

              <!-- Total Interest -->
              <div class="flex items-center justify-between p-4 bg-gradient-to-r from-orange-600/20 to-orange-800/10 rounded-xl border border-orange-500/30 group hover:border-orange-500/60 transition-all">
                <span class="text-gray-400 text-sm uppercase font-bold">{{ currentLanguage === 'th' ? 'ดอกเบี้ยรวม' : 'Total Interest' }}</span>
                <span class="text-orange-400 font-bold text-lg">฿{{ formatPrice(totalInterest) }}</span>
              </div>

              <!-- Total Payment -->
              <div class="flex items-center justify-between p-4 bg-gradient-to-r from-green-600/20 to-green-800/10 rounded-xl border border-green-500/30 group hover:border-green-500/60 transition-all">
                <span class="text-gray-400 text-sm uppercase font-bold">{{ currentLanguage === 'th' ? 'ยอดชำระทั้งหมด' : 'Total Payment' }}</span>
                <span class="text-green-400 font-bold text-lg">฿{{ formatPrice(totalPayment) }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="space-y-3">
            <!-- Contact Seller Button -->
            <button
              @click="contactSellerWithCalculation"
              class="w-full py-4 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-500/50 flex items-center justify-center gap-2 text-lg"
            >
              <i class="fas fa-comments"></i>{{ currentLanguage === 'th' ? 'ติดต่อผู้ขาย' : 'Contact Seller' }}
            </button>

            <!-- Continue Shopping Button -->
            <NuxtLink
              to="/CarList"
              class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-blue-500/50 flex items-center justify-center gap-2 text-lg"
            >
              <i class="fas fa-shopping-cart"></i> {{ currentLanguage === 'th' ? 'รถยนต์เพิ่มเติม' : 'More Cars' }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguage } from '~/composables/useLanguage'

const router = useRouter()
const { t, currentLanguage } = useLanguage()

const cartItems = ref([])
const totalPrice = ref(0)
const downPayment = ref(0)
const downPaymentPercent = ref(10)
const interestRate = ref(4.8)
const duration = ref(12)
const monthlyPayment = ref(0)
const totalInterest = ref(0)
const totalPayment = ref(0)
const currentUsername = ref('')
const showWarning = ref(false)
const warningMessage = ref('')
const baseInterestRate = ref(4.8) // Store base rate

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(Math.round(price || 0))
}

// Calculate interest rate based on duration
const calculateInterestRateByDuration = (months) => {
  // Base rate: 4.8%
  // +0.1% per year (or +0.00833% per month)
  // Y1 (1-12 months): 4.8%
  // Y2 (13-24 months): 5.04% (4.8 × 1.05)
  // Y3 (25-36 months): 5.29% (4.8 × 1.1025)
  const years = months / 12
  const calculatedRate = baseInterestRate.value * Math.pow(1.05, Math.floor(years))
  return parseFloat(calculatedRate.toFixed(2))
}

const goBack = () => {
  router.back()
}

const loadCart = () => {
  const username = localStorage.getItem('username')
  const cartKey = `cart_${username}`
  const saved = localStorage.getItem(cartKey)
  if (saved) {
    cartItems.value = JSON.parse(saved)
    const sum = cartItems.value.reduce((acc, item) => acc + item.price, 0)
    totalPrice.value = sum
    downPayment.value = Math.ceil(sum * (downPaymentPercent.value / 100))
    calculatePayment()
  }
}

const removeFromCart = (index) => {
  if (confirm('Remove this item from cart?')) {
    cartItems.value.splice(index, 1)
    const username = localStorage.getItem('username')
    const cartKey = `cart_${username}`
    localStorage.setItem(cartKey, JSON.stringify(cartItems.value))
    
    if (cartItems.value.length > 0) {
      const sum = cartItems.value.reduce((acc, item) => acc + item.price, 0)
      totalPrice.value = sum
      downPayment.value = Math.ceil(sum * (downPaymentPercent.value / 100))
      calculatePayment()
    } else {
      totalPrice.value = 0
      downPayment.value = 0
      monthlyPayment.value = 0
      totalInterest.value = 0
      totalPayment.value = 0
    }
  }
}

const calculatePayment = () => {
  // Check if down payment is valid (>= 10%)
  if (downPaymentPercent.value < 10 && downPaymentPercent.value > 0) {
    // Don't calculate, show 0 or previous values
    monthlyPayment.value = 0
    totalInterest.value = 0
    totalPayment.value = 0
    return
  }

  const principal = totalPrice.value - downPayment.value
  
  // Prevent negative principal
  if (principal < 0) {
    monthlyPayment.value = 0
    totalInterest.value = 0
    totalPayment.value = 0
    return
  }

  const totalMonths = duration.value
  const avgRate = interestRate.value
  const monthlyRate = (avgRate / 100) / 12
  
  if (monthlyRate === 0) {
    monthlyPayment.value = Math.ceil(principal / totalMonths)
  } else {
    const numerator = monthlyRate * Math.pow(1 + monthlyRate, totalMonths)
    const denominator = Math.pow(1 + monthlyRate, totalMonths) - 1
    monthlyPayment.value = Math.ceil(principal * (numerator / denominator))
  }
  
  totalPayment.value = Math.ceil(monthlyPayment.value * totalMonths) + downPayment.value
  totalInterest.value = Math.ceil(totalPayment.value - downPayment.value - principal)
}

// Update percent from amount input
const updatePercentFromAmount = () => {
  if (totalPrice.value > 0) {
    let calculatedPercent = Math.round((downPayment.value / totalPrice.value) * 100)
    downPaymentPercent.value = calculatedPercent
  }
  calculatePayment()
}

// Update amount from percent input
const updateAmountFromPercent = () => {
  if (downPaymentPercent.value > 0) {
    downPayment.value = Math.ceil(totalPrice.value * (downPaymentPercent.value / 100))
  }
  calculatePayment()
}

const contactSellerWithCalculation = async () => {
  if (cartItems.value.length === 0) {
    alert('No items in cart')
    return
  }

  try {
    const firstCarId = cartItems.value[0].id
    const carResponse = await fetch(`http://localhost:5000/api/cars/${firstCarId}`)
    const carData = await carResponse.json()
    
    if (!carData.success || !carData.car || !carData.car.seller) {
      alert('Error: Could not find seller information')
      return
    }

    const sellerUsername = carData.car.seller.username || carData.car.seller
    
    let message = `สวัสดีครับ/ค่ะ ต้องการสอบถามข้อมูลการผ่อนรถเหล่านี้\n\n`
    
    cartItems.value.forEach((item, idx) => {
      message += `${idx + 1}. 📍 ${item.brand} ${item.model}\n`
      message += `   📅 ปี ${item.year}\n`
      message += `   💰 ฿${formatPrice(item.price)}\n`
      if (idx < cartItems.value.length - 1) message += '\n'
    })

    message += `\n\n💳 ข้อมูลการผ่อน:\n`
    message += `📊 ราคารวม: ฿${formatPrice(totalPrice.value)}\n`
    message += `💵 เงินดาวน์: ฿${formatPrice(downPayment.value)} (${downPaymentPercent.value}%)\n`
    message += `📈 อัตราดอก: ${interestRate.value}%\n`
    message += `📅 จำนวนงวด: ${duration.value} เดือน\n`
    message += `💰 ค่างวดต่อเดือน: ฿${formatPrice(monthlyPayment.value)}\n`
    message += `📋 รวมดอก: ฿${formatPrice(totalInterest.value)}\n`
    message += `💳 ยอดชำระทั้งหมด: ฿${formatPrice(totalPayment.value)}`

    const cartData = {
      items: cartItems.value,
      downPayment: downPayment.value,
      downPaymentPercent: downPaymentPercent.value,
      interestRate: interestRate.value,
      duration: duration.value,
      monthlyPayment: monthlyPayment.value,
      totalInterest: totalInterest.value,
      totalPrice: totalPrice.value,
      totalPayment: totalPayment.value
    }
    
    sessionStorage.setItem('contactCarData', JSON.stringify(cartData))
    sessionStorage.setItem('contactSellerMessage', message)
    sessionStorage.setItem('contactSeller', sellerUsername)
    sessionStorage.setItem('isFromCart', 'true')
    
    await new Promise(resolve => setTimeout(resolve, 100))
    router.push(`/messages?seller=${sellerUsername}`)
  } catch (error) {
    console.error('Error:', error)
    alert('Error: ' + error.message)
  }
}

onMounted(() => {
  currentUsername.value = localStorage.getItem('username') || ''
  loadCart()
  loadCalculatorSettings()
})

// ... watchers ...

// Save calculator settings to localStorage
const saveCalculatorSettings = () => {
  const username = localStorage.getItem('username')
  const settingsKey = `calculator_settings_${username}`
  localStorage.setItem(settingsKey, JSON.stringify({
    downPaymentPercent: downPaymentPercent.value,
    interestRate: interestRate.value,
    duration: duration.value
  }))
}

// Load calculator settings from localStorage
const loadCalculatorSettings = () => {
  const username = localStorage.getItem('username')
  const settingsKey = `calculator_settings_${username}`
  const saved = localStorage.getItem(settingsKey)
  
  if (saved) {
    try {
      const settings = JSON.parse(saved)
      downPaymentPercent.value = settings.downPaymentPercent || 10
      interestRate.value = settings.interestRate || 4.8
      duration.value = settings.duration || 12
    } catch (error) {
      console.error('Error loading calculator settings:', error)
    }
  }
}

// Watch for changes in downPaymentPercent and update downPayment
watch(downPaymentPercent, (newPercent) => {
  // Only calculate, don't auto-change the value
  calculatePayment()
  if (newPercent > 0) {
    saveCalculatorSettings()
  }
})

// Watch for changes in downPayment and update percentage
watch(downPayment, (newDownPayment) => {
  // Only calculate, don't auto-change the value
  calculatePayment()
})

// Watch for changes in totalPrice
watch(totalPrice, (newTotal) => {
  downPayment.value = Math.ceil(newTotal * (downPaymentPercent.value / 100))
  calculatePayment()
})

// Watch for changes in duration and auto calculate
watch(duration, (newDuration) => {
  // Auto-update interest rate based on duration
  const newRate = calculateInterestRateByDuration(newDuration)
  interestRate.value = newRate
  calculatePayment()
  saveCalculatorSettings()
})

// Watch for changes in interestRate and auto calculate
watch(interestRate, () => {
  calculatePayment()
  saveCalculatorSettings()
})</script>

<style scoped>
.duration-slider {
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 5px;
  outline: none;
  background: linear-gradient(to right, #dc2626 0%, #dc2626 var(--slider-value, 0%), #374151 var(--slider-value, 0%), #374151 100%);
}

.duration-slider::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #dc2626;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
  transition: all 0.2s;
}

.duration-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 20px rgba(220, 38, 38, 0.8);
}

.duration-slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #dc2626;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 10px rgba(220, 38, 38, 0.5);
  transition: all 0.2s;
}

.duration-slider::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 20px rgba(220, 38, 38, 0.8);
}

.duration-slider::-moz-range-track {
  background: transparent;
  border: none;
}

.beams-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}
</style>