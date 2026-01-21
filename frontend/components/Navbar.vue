<template>
  <!-- ZAVORA Animation Overlay -->
  <transition name="zavora-fade">
    <div v-if="showZavoraAnimation" class="zavora-animation-overlay">
      <div class="zavora-animated-text">
        <span v-for="(letter, index) in 'ZAVORA'.split('')" :key="index" :style="{ animationDelay: `${index * 0.1}s` }" class="zavora-letter">
          {{ letter }}
        </span>
      </div>
    </div>
  </transition>

  <Nav
    :class="['bg-gradient-to-r from-gray-950/95 via-gray-900/95 to-gray-950/95 backdrop-blur-xl text-white px-4 md:px-8 py-4 flex items-center shadow-2xl transition-all duration-500 relative z-50 border-b border-red-500/10', { 'navbar-visible': !showZavoraAnimation }]"
  >
    <!-- หน้า login/register -->
    <template v-if="isAuthPage">
      <div class="w-full flex justify-center">
        <NuxtLink
          to="/login"
          class="font-extrabold text-2xl tracking-widest text-transparent bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text hover:scale-110 transition-transform duration-300 drop-shadow-lg"
        >
          ZAVORA
        </NuxtLink>
      </div>
    </template>

    <!-- หน้าอื่น -->
    <template v-else>
      <div class="w-full flex justify-between items-center">
        <!-- โลโก้ -->
          <NuxtLink
          to="/"
          :class="['font-extrabold text-2xl md:text-3xl tracking-widest text-transparent bg-gradient-to-r from-red-500 via-orange-500 to-red-500 bg-clip-text hover:scale-110 transition-transform duration-300 drop-shadow-lg relative group', { 'logo-fade-in': logoVisible }]"
        >
          ZAVORA
          <div class="absolute bottom-0 left-0 w-0 h-1 bg-gradient-to-r from-red-500 to-orange-500 group-hover:w-full transition-all duration-500 rounded-full"></div>
        </NuxtLink>

        <!-- ส่วนขวา -->
        <div v-if="isLoggedIn" class="flex items-center space-x-6">
          <!-- ข้อความแจ้งเตือน -->
          <div class="relative group">
            <NuxtLink 
              to="/messages" 
              class="relative flex items-center text-white hover:text-red-500 transition-all duration-300 transform hover:scale-110"
            >
              <i class="fas fa-bell text-xl group-hover:animate-ring"></i>
              <span v-if="messageCount > 0" class="absolute -top-3 -right-3 bg-gradient-to-r from-red-600 to-red-700 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center font-bold animate-pulse shadow-lg border border-red-400">
                {{ messageCount }}
              </span>
            </NuxtLink>
            <!-- Notification Tooltip -->
            <transition name="tooltip">
              <div v-if="messageCount > 0" class="absolute right-0 top-12 bg-gradient-to-br from-red-600 to-red-700 text-white px-4 py-2 rounded-lg text-sm font-semibold whitespace-nowrap shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                <i class="fas fa-bell mr-2"></i>{{ messageCount }} {{ currentLanguage === 'th' ? 'ข้อความใหม่' : 'new message' }}{{ messageCount > 1 ? 's' : '' }}
              </div>
            </transition>
          </div>

          <!-- โปรไฟล์ -->
          <div class="relative group">
            <NuxtLink to="/profile" class="flex items-center space-x-3 text-gray-300 hover:text-red-500 transition-all duration-300 px-4 py-2 rounded-lg hover:bg-red-600/20">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-red-600 to-red-700 border-2 border-red-500 flex items-center justify-center hover:scale-110 transition-transform duration-300 shadow-lg">
                <img v-if="profileImage" :src="profileImage" class="w-full h-full rounded-full object-cover" />
                <i v-else class="fas fa-user text-white text-lg"></i>
              </div>
              <span class="hidden md:block font-semibold">{{ username }}</span>
            </NuxtLink>
          </div>

          <!-- กล่องค้นหา -->
          <div class="relative group w-72">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search cars..."
              class="px-4 py-2.5 rounded-xl bg-gradient-to-r from-gray-900 to-gray-800 border border-gray-700 text-white w-full focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all duration-300 placeholder-gray-500 group-focus-within:ring-2 group-focus-within:ring-orange-500 group-focus-within:border-orange-500 group-focus-within:bg-gray-800 group-focus-within:scale-105 shadow-lg"
              @input="searchCars"
              @keyup.enter="handleEnterSearch"
            />
            <!-- Search Icon Animation -->
            <i class="fas fa-search absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-orange-500 group-focus-within:animate-pulse transition-colors duration-300 pointer-events-none"></i>
            
            <!-- ผลลัพธ์ค้นหา Real-time -->
            <transition name="search-fade">
              <div
                v-if="searchResults.length > 0 && searchQuery.trim()"
                class="absolute z-50 w-full mt-3 bg-gray-900/95 backdrop-blur-lg border border-red-500/50 rounded-xl shadow-2xl animate-search-slide-down max-h-96 overflow-y-auto"
              >
                <div class="p-3 sticky top-0 bg-gradient-to-r from-gray-900/80 to-gray-950/80 border-b border-gray-700/50">
                  <div class="text-xs text-gray-400 px-2 py-1 font-bold uppercase tracking-wide">
                    <i class="fas fa-search text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ผลลัพธ์การค้นหา' : 'Search Results' }} ({{ searchResults.length }})
                  </div>
                </div>
                <div
                  v-for="(car, index) in searchResults"
                  :key="car._id || car.id"
                  @click="selectCar(car)"
                  class="p-4 hover:bg-red-600/20 cursor-pointer flex items-center gap-4 transition-all transform hover:translate-x-2 rounded-lg hover:rounded-2xl animate-search-item hover:shadow-lg hover:shadow-red-600/30 mx-2 my-1 group/search-item border border-transparent hover:border-red-500/50"
                  :style="{ 'animation-delay': `${index * 0.05}s` }"
                >
                  <div class="relative flex-shrink-0">
                    <img 
                      :src="car.images?.[0] || 'https://via.placeholder.com/50x50'" 
                      class="w-16 h-14 object-cover rounded-lg hover:scale-110 transition-transform duration-300 border border-gray-700" 
                      @error="(e) => e.target.src = 'https://via.placeholder.com/50x50'"
                    />
                    <div class="absolute inset-0 rounded-lg bg-gradient-to-r from-red-600/0 to-red-600/20 opacity-0 group-hover/search-item:opacity-100 transition-opacity duration-300"></div>
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-bold text-white group-hover/search-item:text-red-400 transition-colors truncate">
                      {{ car.brand }} {{ car.model }}
                    </div>
                    <div class="text-xs text-gray-400 mt-1">
                      <i class="fas fa-calendar text-red-500 mr-1"></i>{{ car.year }} 
                      <span class="ml-2">•</span>
                      <span class="ml-2 font-semibold text-red-400">฿{{ formatPrice(car.price) }}</span>
                    </div>
                    <div v-if="car.sold" class="text-xs text-red-400 mt-1 font-bold">
                      <i class="fas fa-ban mr-1"></i>{{ currentLanguage === 'th' ? 'ขายแล้ว' : 'SOLD OUT' }}
                    </div>
                  </div>
                  <i class="fas fa-arrow-right text-red-500 text-sm flex-shrink-0 opacity-0 group-hover/search-item:opacity-100 transform group-hover/search-item:translate-x-1 transition-all duration-300"></i>
                </div>
              </div>
            </transition>

            <!-- No results message -->
            <transition name="search-fade">
              <div
                v-if="searchQuery.trim() && searchResults.length === 0"
                class="absolute z-50 w-full mt-3 bg-gray-900/95 backdrop-blur-lg border border-gray-700/50 rounded-xl shadow-lg p-6 text-center animate-search-slide-down"
              >
                <i class="fas fa-search text-gray-500 text-3xl mb-2"></i>
                <p class="text-gray-400 text-sm font-medium">{{ currentLanguage === 'th' ? 'ไม่พบผลลัพธ์' : 'No results found' }}</p>
              </div>
            </transition>
          </div>

          <!-- ปุ่มเปลี่ยนภาษา -->
          <div class="relative group">
            <button 
              @click="languageDropdownVisible = !languageDropdownVisible"
              class="relative flex items-center text-white hover:text-red-500 transition-all duration-300 transform hover:scale-110 font-bold text-sm px-3 py-2 rounded-lg hover:bg-red-600/20"
              :title="languageMode === 'th' ? 'Switch to English' : 'สลับไปภาษาไทย'"
            >
              <i class="fas fa-globe text-lg mr-2"></i>
              {{ languageMode.toUpperCase() }}
            </button>
            <!-- Language Dropdown -->
            <transition name="fade-slide">
              <div
                v-if="languageDropdownVisible"
                class="absolute right-0 top-12 bg-gradient-to-br from-gray-900/95 to-gray-950/95 backdrop-blur-md border border-gray-700 rounded-lg shadow-2xl p-2 w-40 space-y-1 z-50"
              >
                <button
                  @click="switchLanguage('th')"
                  :class="['w-full text-left px-3 py-2 rounded-lg transition-all duration-300', languageMode === 'th' ? 'bg-red-600 text-white' : 'text-gray-300 hover:bg-red-600/20 hover:text-white']"
                >
                  <i class="fas fa-flag mr-2"></i>ไทย (TH)
                </button>
                <button
                  @click="switchLanguage('en')"
                  :class="['w-full text-left px-3 py-2 rounded-lg transition-all duration-300', languageMode === 'en' ? 'bg-red-600 text-white' : 'text-gray-300 hover:bg-red-600/20 hover:text-white']"
                >
                  <i class="fas fa-flag mr-2"></i>English (EN)
                </button>
              </div>
            </transition>
          </div>

          <!-- ปุ่มเมนู -->
          <div
            class="relative"
            @mouseenter="hovering = true"
            @mouseleave="hovering = false"
          >
            <button
              class="flex items-center gap-2 text-gray-300 hover:text-red-500 transition-all duration-300"
              @click="toggleMenu"
            >
              <i class="fas fa-bars text-lg"></i>
              {{ currentLanguage === 'th' ? 'เมนู' : 'Menu' }}
            </button>

            <!-- พื้นหลังบังหน้าทั้งหน้า -->
            <transition name="fade">
              <div
                v-if="isMenuVisible"
                class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                @click="closeMenu"
              ></div>
            </transition>

            <!-- Dropdown -->
            <transition name="fade-slide">
              <div
                v-if="isMenuVisible"
                class="absolute right-0 top-12 bg-gradient-to-br from-gray-900/95 to-gray-950/95 backdrop-blur-md border border-gray-700 hover:border-red-500/50 rounded-2xl shadow-2xl p-4 w-56 flex flex-col space-y-2 animate-slideDown z-50"
              >
                <NuxtLink
                  to="/"
                  class="menu-item font-extrabold text-lg tracking-wide text-red-500 hover:scale-110 hover:text-red-400 transition-all duration-300 hover:bg-red-600/20 rounded-lg px-3 py-2"
                  >
                  <i class="fas fa-home mr-3 text-red-500 text-lg"></i> {{ currentLanguage === 'th' ? 'หน้าแรก' : 'Home' }}
                </NuxtLink>
                <NuxtLink to="/dashboard" class="menu-item hover:bg-red-600/20 rounded-lg px-3 py-2">
                  <i class="fas fa-user mr-3 text-red-500 text-lg"></i> {{ currentLanguage === 'th' ? 'โปรไฟล์ของฉัน' : 'My Profile' }}
                </NuxtLink>
                <NuxtLink to="/messages" class="menu-item hover:bg-red-600/20 rounded-lg px-3 py-2">
                  <i class="fas fa-comments mr-3 text-red-500 text-lg"></i> {{ currentLanguage === 'th' ? 'ข้อความ' : 'Messages' }}
                </NuxtLink>
                <NuxtLink to="/CarList" class="menu-item hover:bg-red-600/20 rounded-lg px-3 py-2">
                  <i class="fas fa-car-side mr-3 text-red-500 text-lg"></i> {{ currentLanguage === 'th' ? 'รายการรถ' : 'Cars' }}
                </NuxtLink>

                <!-- Divider -->
                <div class="border-b border-gray-700/50"></div>

                <!-- Sell Your Car (button) -->
                <button @click="handleSellClick" class="menu-item flex items-center hover:bg-red-600/20 rounded-lg px-3 py-2 w-full">
                  <i class="fas fa-plus-circle mr-3 text-red-500 text-lg"></i>
                  {{ currentLanguage === 'th' ? 'ขายรถของคุณ' : 'Sell Your Car' }}
                </button>

                <!-- Logout -->
                <div class="border-b border-gray-700/50"></div>
                <button @click="handleLogout" class="menu-item text-left hover:bg-red-600/20 rounded-lg px-3 py-2 w-full">
                  <i class="fas fa-sign-out-alt mr-3 text-red-500 text-lg"></i> {{ currentLanguage === 'th' ? 'ออกจากระบบ' : 'Logout' }}
                </button>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </template>
  </Nav>

  <!-- Teleport modal -->
  <teleport to="body">
    <div v-if="showNotSellerModal" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <div class="absolute inset-0 bg-black/70" @click="closeNotSellerModal"></div>
      <div class="relative z-50 max-w-lg w-full mx-4 p-8 bg-gray-900 text-center rounded-lg animate-modal">
        <div class="text-white text-2xl font-bold">{{ currentLanguage === 'th' ? 'คุณไม่ใช่ผู้ขาย' : 'You are not a seller' }}</div>
        <div class="text-sm text-gray-400 mt-3">{{ currentLanguage === 'th' ? 'คลิกที่ใดก็ได้บนหน้าจอนี้เพื่อไปที่ลงทะเบียนเป็นผู้ขาย' : 'Click anywhere on this screen to go to Register as a Seller' }}</div>
      </div>
    </div>
  </teleport>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useSmartBack } from '~/composables/useSmartBack'
import { useLanguage } from '~/composables/useLanguage'

const router = useRouter()
const route = useRoute()
const { t, setLanguage, currentLanguage, initLanguage } = useLanguage()

const searchQuery = ref('')
const searchResults = ref([])
const hovering = ref(false)
const clicked = ref(false)
const username = ref('')
const profileImage = ref('')
const showNotSellerModal = ref(false)
const cartCount = ref(0)
const showZavoraAnimation = ref(false)
const logoVisible = ref(false)
const messageCount = ref(0)
const languageMode = ref('th')
const languageDropdownVisible = ref(false)
let searchTimeout = null

const { goBack } = useSmartBack()

const isSeller = computed(() => {
  if (!process.client) return false
  const role = localStorage.getItem('role')
  const isSellerFlag = localStorage.getItem('is_seller')
  return role === 'seller' || isSellerFlag === 'true' || isSellerFlag === '1'
})

onMounted(() => {
  if (process.client) {
    username.value = localStorage.getItem('username') || ''
    loadProfileImage()
    updateCartCount()
    updateMessageCount()
    
    // Initialize language
    initLanguage()
    languageMode.value = currentLanguage.value
    
    // Watch language changes
    watch(() => currentLanguage.value, (newLang) => {
      languageMode.value = newLang
    })
    
    // Remove ZAVORA animation from Navbar - show only on Login page
    logoVisible.value = true
    
    // Watch for cart changes every 500ms
    const cartWatchInterval = setInterval(() => {
      updateCartCount()
    }, 500)
    
    // Watch for message changes every 1 second (more frequent)
    const messageWatchInterval = setInterval(() => {
      updateMessageCount()
    }, 1000)
    
    // Poll for profile image updates every 2 seconds
    const profileWatchInterval = setInterval(() => {
      loadProfileImage()
    }, 2000)
    
    // Listen to storage changes from other tabs
    window.addEventListener('storage', (e) => {
      if (e.key && e.key.startsWith('cart_')) {
        updateCartCount()
      }
    })
    
    // Cleanup intervals on unmount
    return () => {
      clearInterval(cartWatchInterval)
      clearInterval(messageWatchInterval)
      clearInterval(profileWatchInterval)
    }
  }
})

// Watch route changes to update cart count
watch(() => route.path, () => {
  updateCartCount()
})

// Fetch profile image from API
const loadProfileImage = async () => {
  try {
    const currentUsername = localStorage.getItem('username')
    if (!currentUsername) return

    const response = await fetch(
      `http://localhost:5000/api/get-profile?username=${currentUsername}`
    )
    const data = await response.json()

    if (data.success && data.profileImageUrl) {
      profileImage.value = data.profileImageUrl
      // Also save to localStorage for faster access
      localStorage.setItem('profileImage', data.profileImageUrl)
    }
  } catch (error) {
    console.error('Error loading profile image:', error)
  }
}

const isLoggedIn = computed(() => !!localStorage.getItem('token'))
const isAuthPage = computed(() =>
  ['/login', '/register', '/register-seller'].includes(route.path)
)

const isMenuVisible = computed(() => hovering.value || clicked.value)

const toggleMenu = () => {
  clicked.value = !clicked.value
}

const closeMenu = () => {
  clicked.value = false
  hovering.value = false
}

const updateCartCount = () => {
  if (!process.client) return
  
  const currentUsername = localStorage.getItem('username')
  if (!currentUsername) {
    cartCount.value = 0
    return
  }
  
  const cartKey = `cart_${currentUsername}`
  const cart = localStorage.getItem(cartKey)
  
  try {
    cartCount.value = cart ? JSON.parse(cart).length : 0
  } catch (error) {
    console.error('Error parsing cart:', error)
    cartCount.value = 0
  }
}

const updateMessageCount = async () => {
  try {
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')
    
    if (!token || !username) {
      messageCount.value = 0
      return
    }

    // Get unread message count from API
    const response = await fetch(`http://localhost:5000/api/conversations/unread-count/${username}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      console.error('Failed to fetch unread count:', response.status)
      return
    }

    const data = await response.json()
    
    if (data.success) {
      messageCount.value = data.unreadCount || 0
      
      // Log when there are new messages
      if (data.unreadCount > 0) {
        console.log(`📬 ${data.unreadCount} unread message(s)`)
      }
    }
  } catch (error) {
    console.error('Error fetching message count:', error)
  }
}

const searchCars = async () => {
  if (!searchQuery.value || searchQuery.value.trim().length < 1) {
    searchResults.value = []
    return
  }

  // Clear previous timeout
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }

  // Debounce search - wait 300ms before making API call
  searchTimeout = setTimeout(async () => {
    try {
      console.log('🔍 Searching for:', searchQuery.value)
      
      // Try multiple search strategies
      const query = encodeURIComponent(searchQuery.value.trim())
      
      // First, try dedicated search endpoint
      let response = await fetch(
        `http://localhost:5000/api/cars/search?q=${query}`
      )
      
      // If search endpoint not found, fetch all cars and filter locally
      if (!response.ok || response.status === 404) {
        console.log('Search endpoint not found, fetching all cars...')
        response = await fetch('http://localhost:5000/api/cars')
      }
      
      if (!response.ok) {
        console.error('Search API error:', response.status)
        searchResults.value = []
        return
      }

      const data = await response.json()
      console.log('Response data:', data)
      
      let results = []
      
      if (data.success && Array.isArray(data.cars)) {
        // Filter cars based on search query
        const searchLower = searchQuery.value.toLowerCase()
        results = data.cars.filter(car => {
          if (!car) return false
          
          const brand = (car.brand || '').toLowerCase()
          const model = (car.model || '').toLowerCase()
          const year = (car.year || '').toString()
          const price = (car.price || '').toString()
          const carType = (car.car_type || '').toLowerCase()
          const fuelType = (car.fuel_type || '').toLowerCase()
          
          return (
            brand.includes(searchLower) ||
            model.includes(searchLower) ||
            year.includes(searchLower) ||
            price.includes(searchLower) ||
            carType.includes(searchLower) ||
            fuelType.includes(searchLower) ||
            `${brand} ${model}`.includes(searchLower)
          )
        })
      }
      
      searchResults.value = results.slice(0, 8)
      console.log(`✅ Found ${searchResults.value.length} cars`)
    } catch (error) {
      console.error('❌ Search failed:', error)
      searchResults.value = []
    }
  }, 300)
}

const selectCar = (car) => {
  if (car.sold) {
    alert('This car has been sold')
    searchQuery.value = ''
    searchResults.value = []
    return
  }
  router.push(`/car/${car._id || car.id}`)
  searchQuery.value = ''
  searchResults.value = []
  closeMenu()
}

const handleEnterSearch = () => {
  if (searchResults.value.length > 0) selectCar(searchResults.value[0])
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
  closeMenu()
}

const handleSellClick = (e) => {
  if (isSeller.value) {
    router.push('/seller/PostCar')
    closeMenu()
  } else {
    showNotSellerModal.value = true
  }
}

const closeNotSellerModal = () => {
  showNotSellerModal.value = false
  closeMenu()
  router.push('/dashboard')
}

const handleBackClick = () => {
  goBack()
}

const formatPrice = (price) => {
  if (!price) return 'N/A'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const switchLanguage = (lang) => {
  setLanguage(lang)
  languageMode.value = lang
  languageDropdownVisible.value = false
  // Optional: Show toast notification
  console.log(`🌐 Language switched to ${lang === 'th' ? 'Thai' : 'English'}`)
}

const toggleLanguageDropdown = () => {
  languageDropdownVisible.value = !languageDropdownVisible.value
}
</script>

<style scoped>
/* เมนู hover */
.menu-item {
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  color: rgb(209, 213, 219);
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.menu-item:hover {
  background-color: rgb(220, 38, 38);
  color: white;
}

/* Bell Ring Animation */
@keyframes bellRing {
  0%, 100% {
    transform: rotate(0deg);
  }
  10%, 20% {
    transform: rotate(-15deg);
  }
  30%, 50%, 70%, 90% {
    transform: rotate(15deg);
  }
  40%, 60%, 80% {
    transform: rotate(-15deg);
  }
}

.group-hover\:animate-ring:hover {
  animation: bellRing 0.6s ease-in-out infinite;
}

/* Tooltip Animation */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.tooltip-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.tooltip-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Pulse Animation for Badge */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Slide */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.25s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* keyframes */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
.animate-slideDown {
  animation: slideDown 0.30s ease-out;
}

/* Modal animation */
.animate-modal {
  animation: popIn 0.35s ease-out;
}

@keyframes popIn {
  0% { opacity: 0; transform: translateY(-12px) scale(0.98); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

/* Search animations */
.animate-search-slide-down {
  animation: searchSlideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-search-item {
  animation: searchItemSlide 0.4s ease-out forwards;
  opacity: 0;
}

@keyframes searchSlideDown {
  from {
    opacity: 0;
    transform: translateY(-15px) scaleY(0.95);
    filter: blur(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scaleY(1);
    filter: blur(0);
  }
}

@keyframes searchItemSlide {
  from {
    opacity: 0;
    transform: translateX(-15px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.search-fade-enter-active,
.search-fade-leave-active {
  transition: all 0.25s ease;
}

.search-fade-enter-from,
.search-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px) scaleY(0.95);
  filter: blur(4px);
}

/* ZAVORA Animation Overlay */
.zavora-animation-overlay {
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #000000 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: zavoraOverlaySlideUp 0.8s ease-out 1.2s forwards;
}

.zavora-animated-text {
  display: flex;
  gap: 0.5rem;
  font-size: 6rem;
  font-weight: 900;
  letter-spacing: 0.3rem;
}

.zavora-letter {
  display: inline-block;
  background: linear-gradient(135deg, #ff3c03, #ff8c00, #ff3c03);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: 
    zavoraLetterPop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards,
    zavoraGradientShift 3s ease infinite,
    zavoraMoveToNav 0.8s ease-out 1.2s forwards;
  opacity: 0;
  transform: scale(0) rotateY(180deg);
  text-shadow: 0 0 30px rgba(255, 60, 3, 0.5);
}

@keyframes zavoraLetterPop {
  0% {
    opacity: 0;
    transform: scale(0) rotateY(180deg);
  }
  50% {
    transform: scale(1.2) rotateY(0deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateY(0deg);
  }
}

@keyframes zavoraGradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes zavoraMoveToNav {
  0% {
    font-size: 6rem;
    transform: translate(0, 0) scale(1);
  }
  100% {
    font-size: 1.5rem;
    transform: translate(calc(-50vw + 100px), calc(-50vh + 30px)) scale(0.4);
    opacity: 0;
  }
}

@keyframes zavoraOverlaySlideUp {
  to {
    transform: translateY(-100%);
    opacity: 0;
  }
}

.zavora-fade-enter-active,
.zavora-fade-leave-active {
  transition: all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.zavora-fade-leave-to {
  opacity: 0;
  transform: translateY(-100%) scale(0.8);
}

.logo-fade-in {
  animation: logoFadeIn 0.6s ease-out 2s both;
}

@keyframes logoFadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.navbar-visible {
  animation: navbarSlideDown 0.5s ease-out 1s both;
}

@keyframes navbarSlideDown {
  from {
    opacity: 0;
    transform: translateY(-100%);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
