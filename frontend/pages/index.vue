<template>
  <div class="min-h-screen bg-gray-950 text-white transition-all duration-500">
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
    <div v-if="!showLoader" class="min-h-screen bg-gray-950 text-white transition-all duration-500 animate-fade-in">
     <!-- Car List -->
      <div class="space-y-12 p-8">
        <!-- Section Title -->
        <div class="text-center mb-12 animate-fade-in">
          <h2 class="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-red-500 via-orange-500 to-red-500 bg-clip-text text-transparent mb-4 drop-shadow-lg">
            {{ currentLanguage === 'th' ? 'รถยนต์แนะนำ'  : 'Featured Cars' }}
          </h2>
          <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'ค้นหารถยนต์ที่คุณต้องการ' : 'Find the car you want' }}</p>
        </div>

        <!-- First Row -->
        <div class="relative">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollLeft('row1')" class="p-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95">
              <i class="fas fa-chevron-left text-xl text-white"></i>
            </button>
          </div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollRight('row1')" class="p-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95">
              <i class="fas fa-chevron-right text-xl text-white"></i>
            </button>
          </div>
          <div id="row1" class="flex overflow-x-auto hide-scrollbar gap-6 px-16 scroll-smooth">
            <NuxtLink
              v-for="car in cars.slice(0, Math.ceil(cars.length/2))"
              :key="car.id"
              :to="`/car/${car.id}`"
              class="car-card flex-shrink-0 w-[320px] bg-gradient-to-br from-gray-900/80 via-gray-800/50 to-gray-950/80 backdrop-blur-xl p-6 rounded-2xl border border-gray-700/50 hover:border-red-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-red-600/30 hover:-translate-y-3 transform group overflow-hidden relative"
            >
              <!-- Gradient Overlay on Hover -->
              <div class="absolute inset-0 bg-gradient-to-t from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <!-- Image Container -->
              <div class="relative mb-6 overflow-hidden rounded-xl group/image">
                <img 
                  :src="car.image" 
                  alt="car" 
                  class="rounded-xl w-full h-48 object-cover group-hover/image:scale-110 transition-transform duration-500 shadow-xl" 
                />
                <!-- Year Badge -->
                <div class="absolute top-4 left-4 bg-gray-900/80 backdrop-blur-sm px-4 py-2 rounded-full text-xs font-bold text-gray-200 border border-gray-700">
                  {{ car.year }}
                </div>
              </div>

              <!-- Content -->
              <div class="relative z-10 space-y-4">
                <!-- Title -->
                <div>
                  <h3 class="font-extrabold text-xl text-white mb-1 group-hover:text-red-400 transition-colors">{{ car.name }}</h3>
                  <p class="text-sm text-gray-400 font-semibold">{{ car.brand }}</p>
                </div>

                <!-- Specs -->
                <div class="grid grid-cols-2 gap-3">
                  <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-red-500/50 transition-all duration-300">
                    <p class="text-white font-semibold flex items-center gap-2">
                      <i class="fas fa-cog text-red-500"></i>
                      {{ car.transmission || 'N/A' }}
                    </p>
                  </div>
                  <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-orange-500/50 transition-all duration-300">
                    <p class="text-white font-semibold flex items-center gap-2">
                      <i class="fas fa-gas-pump text-orange-500"></i>
                      {{ car.fuel || 'N/A' }}
                    </p>
                  </div>
                </div>

                <!-- Price & Button -->
                <div class="flex items-center justify-between pt-4 border-t border-gray-700/50">
                  <div v-if="!car.sold">
                    <p class="text-gray-400 text-xs uppercase font-bold mb-1">{{ currentLanguage === 'th' ? 'ราคา' : 'Price' }}</p>
                    <p class="text-3xl font-extrabold text-red-500 drop-shadow-lg">฿{{ formatPrice(car.price) }}</p>
                  </div>
                  <div v-else class="flex-1">
                    <p class="text-2xl font-extrabold text-gray-500 drop-shadow-lg">{{ currentLanguage === 'th' ? 'ขายแล้ว' : 'SOLD OUT' }}</p>
                  </div>
                  <button v-if="!car.sold" class="px-6 py-3 rounded-xl bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold hover:shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95 shadow-lg flex items-center gap-2">
                    <i class="fas fa-eye"></i>
                    {{ currentLanguage === 'th' ? 'ดู' : 'View' }}
                  </button>
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>

        <!-- Second Row -->
        <div class="relative">
          <div class="absolute left-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollLeft('row2')" class="p-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95">
              <i class="fas fa-chevron-left text-xl text-white"></i>
            </button>
          </div>
          <div class="absolute right-0 top-1/2 -translate-y-1/2 z-10">
            <button @click="scrollRight('row2')" class="p-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95">
              <i class="fas fa-chevron-right text-xl text-white"></i>
            </button>
          </div>
          <div id="row2" class="flex overflow-x-auto hide-scrollbar gap-6 px-16 scroll-smooth">
            <NuxtLink
              v-for="car in cars.slice(Math.ceil(cars.length/2))"
              :key="car.id"
              :to="`/car/${car.id}`"
              class="car-card flex-shrink-0 w-[320px] bg-gradient-to-br from-gray-900/80 via-gray-800/50 to-gray-950/80 backdrop-blur-xl p-6 rounded-2xl border border-gray-700/50 hover:border-red-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-red-600/30 hover:-translate-y-3 transform group overflow-hidden relative"
            >
              <!-- Gradient Overlay on Hover -->
              <div class="absolute inset-0 bg-gradient-to-t from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

              <!-- Image Container -->
              <div class="relative mb-6 overflow-hidden rounded-xl group/image">
                <img 
                  :src="car.image" 
                  alt="car" 
                  class="rounded-xl w-full h-48 object-cover group-hover/image:scale-110 transition-transform duration-500 shadow-xl" 
                />
                <!-- Year Badge -->
                <div class="absolute top-4 left-4 bg-gray-900/80 backdrop-blur-sm px-4 py-2 rounded-full text-xs font-bold text-gray-200 border border-gray-700">
                  {{ car.year }}
                </div>
              </div>

              <!-- Content -->
              <div class="relative z-10 space-y-4">
                <!-- Title -->
                <div>
                  <h3 class="font-extrabold text-xl text-white mb-1 group-hover:text-red-400 transition-colors">{{ car.name }}</h3>
                  <p class="text-sm text-gray-400 font-semibold">{{ car.brand }}</p>
                </div>

                <!-- Specs -->
                <div class="grid grid-cols-2 gap-3">
                  <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-red-500/50 transition-all duration-300">
                    <p class="text-white font-semibold flex items-center gap-2">
                      <i class="fas fa-cog text-red-500"></i>
                      {{ car.transmission || 'N/A' }}
                    </p>
                  </div>
                  <div class="bg-gray-800/50 border border-gray-700/50 p-3 rounded-xl hover:border-orange-500/50 transition-all duration-300">
                    <p class="text-white font-semibold flex items-center gap-2">
                      <i class="fas fa-gas-pump text-orange-500"></i>
                      {{ car.fuel|| 'N/A' }}
                    </p>
                  </div>
                </div>

                <!-- Price & Button -->
                <div class="flex items-center justify-between pt-4 border-t border-gray-700/50">
                  <div v-if="!car.sold">
                    <p class="text-gray-400 text-xs uppercase font-bold mb-1">{{ currentLanguage === 'th' ? 'ราคา' : 'Price' }}</p>
                    <p class="text-3xl font-extrabold text-red-500 drop-shadow-lg">฿{{ formatPrice(car.price) }}</p>
                  </div>
                  <div v-else class="flex-1">
                    <p class="text-2xl font-extrabold text-gray-500 drop-shadow-lg">{{ currentLanguage === 'th' ? 'ขายแล้ว' : 'SOLD OUT' }}</p>
                  </div>
                  <button v-if="!car.sold" class="px-6 py-3 rounded-xl bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold hover:shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-110 active:scale-95 shadow-lg flex items-center gap-2">
                    <i class="fas fa-eye"></i>
                    {{ currentLanguage === 'th' ? 'ดู' : 'View' }}
                  </button>
                </div>
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>


      <!-- Compare Modal -->
      <div v-if="showCompare" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
        <div class="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-4xl">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">{{ currentLanguage === 'th' ? 'เปรียบเทียบรถยนต์' : 'Compare Cars' }}</h2>
            <button @click="showCompare = false" class="text-gray-500 hover:text-gray-700">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="grid grid-cols-3 gap-4">
            <!-- Compare cars content -->
          </div>
        </div>
      </div>

      <!-- Enhanced Brand Menu -->
      <div class="relative py-12 px-6 bg-gradient-to-r from-red-700/20 via-orange-600/10 to-red-700/20 border-y border-red-500/30 backdrop-blur-xl overflow-hidden">
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <div class="absolute -top-1/2 -left-1/4 w-96 h-96 bg-red-600/10 rounded-full blur-3xl animate-pulse"></div>
          <div class="absolute -bottom-1/2 -right-1/4 w-96 h-96 bg-red-600/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 0.5s;"></div>
        </div>

        <div class="max-w-7xl mx-auto relative z-10">
          <!-- Section Header -->
          <div class="text-center mb-8 animate-fade-in">
            <h3 class="text-3xl md:text-4xl font-extrabold bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent mb-2">
              <i class="fas fa-layer-group mr-3"></i>{{ currentLanguage === 'th' ? 'แบรนด์ยอดนิยม' : 'Popular Brands' }}
            </h3>
            <p class="text-gray-400 text-sm">{{ currentLanguage === 'th' ? 'สำรวจรถยนต์จากผู้ผลิตชั้นนำ' : 'Explore vehicles from top manufacturers' }}</p>
          </div>

          <!-- Brand Carousel -->
          <div class="relative">
            <!-- Left Button -->
            <div class="absolute left-0 top-1/2 -translate-y-1/2 z-20">
              <button 
                @click="scrollLeft('brands')" 
                class="p-4 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-125 active:scale-95 backdrop-blur-sm border border-red-500/50"
              >
                <i class="fas fa-chevron-left text-xl text-white"></i>
              </button>
            </div>

            <!-- Right Button -->
            <div class="absolute right-0 top-1/2 -translate-y-1/2 z-20">
              <button 
                @click="scrollRight('brands')" 
                class="p-4 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 rounded-full shadow-lg hover:shadow-red-600/50 transition-all transform hover:scale-125 active:scale-95 backdrop-blur-sm border border-red-500/50"
              >
                <i class="fas fa-chevron-right text-xl text-white"></i>
              </button>
            </div>

            <!-- Brands Scroll Container -->
            <div id="brands" class="flex overflow-x-auto hide-scrollbar gap-5 px-20 scroll-smooth py-4">
              <NuxtLink
                v-for="(brand, index) in brands"
                :key="brand"
                :to="`/brand/${brand.toLowerCase()}`"
                class="brand-button group flex flex-col items-center justify-center bg-gradient-to-br from-gray-800/60 via-gray-900/40 to-gray-950/60 backdrop-blur-xl px-8 py-6 rounded-2xl hover:from-red-600/40 hover:via-orange-600/30 hover:to-red-600/40 border border-gray-700/50 hover:border-red-500/80 transition-all duration-300 flex-shrink-0 transform hover:scale-110 shadow-lg hover:shadow-2xl hover:shadow-red-600/40 relative overflow-hidden"
                :style="{ 'animation-delay': `${index * 0.05}s` }"
              >
                <!-- Gradient Overlay on Hover -->
                <div class="absolute inset-0 bg-gradient-to-t from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>

                <!-- Brand Logo Container -->
                <div class="relative z-10 w-16 h-16 flex items-center justify-center mb-3 bg-gray-900/50 rounded-full group-hover:bg-gray-800/50 transition-all duration-300 border border-gray-700/50 group-hover:border-red-500/50 shadow-lg group-hover:shadow-red-600/30">
                  <img 
                    :src="`/images/brands/${brand.toLowerCase()}.png`" 
                    :alt="`${brand} logo`" 
                    class="w-10 h-10 object-contain drop-shadow-lg group-hover:scale-110 transition-transform duration-300"
                    @error="handleImageError"
                  />
                </div>

                <!-- Brand Name -->
                <span class="whitespace-nowrap font-bold text-white text-base group-hover:text-red-400 transition-colors duration-300 text-center">{{ brand }}</span>

                <!-- Hover Arrow -->
                <div class="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transform group-hover:translate-x-0 translate-x-2 transition-all duration-300">
                  <i class="fas fa-arrow-right text-red-500 text-sm"></i>
                </div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Beams from '~/components/Beams.vue'
import ZavoraLoader from '~/components/ZavoraLoader.vue'
import { useLanguage } from '~/composables/useLanguage'

const { t, currentLanguage } = useLanguage()
const isDark = ref(true)
const searchQuery = ref('')
const showCompare = ref(false)
const showWishlist = ref(false)
const compareList = ref([])
const wishlist = ref([])
const cars = ref([])
const brands = ref(['Toyota', 'Honda', 'Nissan', 'Mazda', 'BMW', 'Mercedes', 'Audi', 'Ford', 'Chevrolet', 'Mitsubishi'])
const loading = ref(true)
const showLoader = ref(true)

// Fetch cars from backend
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:5000/api/cars')
    const data = await response.json()
    
    if (data.success) {
      cars.value = data.cars.map(car => ({
        id: car.id || car._id,
        name: car.model,
        brand: car.brand,
        model: car.model,
        year: car.year,
        price: car.price,
        image: car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/300x200?text=No+Image',
        transmission: car.transmission || 'Automatic',
        fuel: car.fuel_type || 'Petrol',
        views: car.views || 0,
        sold: car.sold || car.sold_out || false
      }))
      
      // ✅ Sort by views (descending) - most viewed first
      cars.value.sort((a, b) => (b.views || 0) - (a.views || 0))
    }
  } catch (error) {
    console.error('Error fetching cars:', error)
  } finally {
    loading.value = false
  }
})

// Format price function
const formatPrice = (price) => {
  if (!price) return 'N/A'
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

// Handle missing brand images
const handleImageError = (e) => {
  e.target.src = '/images/brands/'
}

// Dark mode toggle
const toggleDarkMode = () => {
  isDark.value = !isDark.value
}

// Search functionality
const searchSuggestions = computed(() => {
  if (!searchQuery.value) return []
  return cars.value.filter(car => 
    car.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    car.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
  ).slice(0, 5)
})

const filteredCars = computed(() => {
  if (!searchQuery.value) return cars.value
  return cars.value.filter(car => 
    car.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    car.brand.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// Wishlist & Compare functions
const toggleWishlist = (car) => {
  const index = wishlist.value.findIndex(item => item.id === car.id)
  if (index === -1) {
    wishlist.value.push(car)
  } else {
    wishlist.value.splice(index, 1)
  }
}

const toggleCompare = (car) => {
  if (compareList.value.length >= 3 && !isInCompare(car.id)) {
    alert('You can compare up to 3 cars')
    return
  }
  const index = compareList.value.findIndex(item => item.id === car.id)
  if (index === -1) {
    compareList.value.push(car)
  } else {
    compareList.value.splice(index, 1)
  }
}

const isInWishlist = (id) => wishlist.value.some(car => car.id === id)
const isInCompare = (id) => compareList.value.some(car => car.id === id)

// Scroll functions
const scrollLeft = (elementId) => {
  const element = document.getElementById(elementId)
  element.scrollBy({ left: -300, behavior: 'smooth' })
}

const scrollRight = (elementId) => {
  const element = document.getElementById(elementId)
  element.scrollBy({ left: 300, behavior: 'smooth' })
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  font-family: 'Inter', sans-serif;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.car-card {
  border-radius: 0.75rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  transition: all 500ms;
  animation: fadeIn 0.5s ease-out;
}

.car-card:hover {
  box-shadow: 0 20px 50px rgba(220, 38, 38, 0.2);
  transform: translateY(-4px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.brand-button {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-fade-in { 
  animation: fadeIn 1s cubic-bezier(0.34, 1.56, 0.64, 1) both; 
}

.beams-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}
</style>
