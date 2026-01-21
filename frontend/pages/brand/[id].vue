<template>
  <div>
    

    <div v-if="!loading" class="brandcars-page min-h-screen bg-gray-950 text-white relative overflow-hidden p-8">
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

    <div class="max-w-7xl mx-auto relative z-10">

        

        <!-- Brand Header - Enhanced -->
        <div class="mb-12 animate-slide-down">
          <div class="bg-gradient-to-r from-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-3xl p-10 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-2xl">
            <div class="flex flex-col lg:flex-row items-center gap-10">
              <!-- Brand Logo Circle -->
              <div class="relative flex-shrink-0">
                <div class="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-full blur-2xl opacity-40"></div>
                <div class="relative w-40 h-40 bg-gradient-to-br from-gray-800 to-gray-900 rounded-full flex items-center justify-center border-4 border-red-500 shadow-2xl overflow-hidden group hover:border-red-400 transition-all transform hover:scale-110 duration-300">
                  <img 
                    v-if="brandLogo" 
                    :src="brandLogo" 
                    :alt="selectedBrand" 
                    class="w-full h-full object-cover"
                    @error="brandLogo = ''"
                  />
                  <i v-else class="fas fa-car text-6xl text-red-500 group-hover:text-red-400 transition-colors"></i>
                </div>
              </div>

              <!-- Brand Info -->
              <div class="flex-1">
                <h1 class="text-6xl font-extrabold bg-gradient-to-r from-red-500 via-red-400 to-orange-400 bg-clip-text text-transparent mb-3 drop-shadow-lg">
                  {{ selectedBrand }}
                </h1>
                <p class="text-xl text-gray-300 mb-6">{{ currentLanguage === 'th' ? 'สำรวจรถยนต์' : 'Explore all available' }} {{ selectedBrand }} {{ currentLanguage === 'th' ? 'รถยนต์ในสต็อกของเรา' : 'Vehicles in our inventory' }} </p>

                <!-- Stats Grid -->
                <div class="grid grid-cols-3 gap-4">
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">{{ currentLanguage === 'th' ? 'จำนวนรถทั้งหมด' : 'Total Cars' }}</p>
                    <p class="text-white font-bold text-3xl">{{ brandCars.length }}</p>
                    <p class="text-xs text-gray-500 mt-1">{{ availableCount }} {{ currentLanguage === 'th' ? 'คัน' : 'available' }} </p>
                  </div>
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">{{ currentLanguage === 'th' ? 'ราคาต่ำสุด' : 'Min Price' }}</p>
                    <p class="text-green-400 font-bold text-lg">฿{{ minPrice.toLocaleString('th-TH') }}</p>
                  </div>
                  <div class="bg-gray-800/50 p-4 rounded-xl border border-gray-700 hover:border-red-500/50 transition-all">
                    <p class="text-gray-400 text-sm mb-1 uppercase font-semibold">{{ currentLanguage === 'th' ? 'ราคาสูงสุด' : 'Max Price' }}</p>
                    <p class="text-red-400 font-bold text-lg">฿{{ maxPrice.toLocaleString('th-TH') }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Header -->
        <div class="mb-8 animate-fade-in">
          <h2 class="text-3xl font-bold text-white mb-2">{{ currentLanguage === 'th' ? 'เรียกรถยนต์' : 'Browse Vehicles' }}</h2>
          <p class="text-gray-400">{{ currentLanguage === 'th' ? 'กรองและค้นหารถยนต์ที่สมบูรณ์แบบของคุณ' : 'Filter and find your perfect' }} {{ selectedBrand }} {{ currentLanguage === 'th' ? 'รถยนต์' : 'vehicle' }}</p>
        </div>

        <!-- Search Bar -->
        <div class="mb-8 animate-fade-in-up">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by model, color, fuel type..."
              class="w-full px-6 py-4 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
            />
            <i class="fas fa-search absolute right-4 top-1/2 -translate-y-1/2 text-gray-500"></i>
          </div>
        </div>

        <!-- Filters Section - Like CarList -->
        <div class="mb-8 flex flex-wrap gap-4 animate-fade-in-up">
          <!-- Year Filter -->
          <select
            v-model="selectedYear"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ปี' : 'Year' }} </option>
            <option v-for="year in uniqueYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>

          <!-- Fuel Type -->
          <select
            v-model="selectedFuelType"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ประเภทเชื้อเพลิงทั้งหมด' : 'All Fuel Types' }}</option>
            <option value="Petrol">{{ currentLanguage === 'th' ? 'เบนซิน' : 'Petrol' }}</option>
            <option value="Diesel">{{ currentLanguage === 'th' ? 'ดีเซล' : 'Diesel' }}</option>
            <option value="Hybrid">{{ currentLanguage === 'th' ? 'ไฮบริด' : 'Hybrid' }}</option>
            <option value="Electric">{{ currentLanguage === 'th' ? 'ไฟฟ้า' : 'Electric' }}</option>
          </select>

          <!-- Gas System (Dynamic - shown after Fuel Type selection) -->
          <select
            v-if="selectedFuelType"
            v-model="selectedGasSystem"
            class="px-6 py-3 bg-gray-800/50 border border-orange-500/50 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-orange-400 animate-fade-in"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ระบบแก๊สทั้งหมด' : 'All Gas Systems' }}</option>
            <option v-for="gasSystem in uniqueGasSystems" :key="gasSystem" :value="gasSystem">
              {{ gasSystem }}
            </option>
          </select>

          <!-- Drive Systems -->
          <select
            v-model="selectedDriveSystem"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ระบบขับเคลื่อนทั้งหมด' : 'All Drive Systems' }}</option>
            <option value="FWD">{{ currentLanguage === 'th' ? 'FWD ' : 'FWD ' }}</option>
            <option value="RWD">{{ currentLanguage === 'th' ? 'RWD ' : 'RWD ' }}</option>
            <option value="AWD">{{ currentLanguage === 'th' ? 'AWD ' : 'AWD ' }}</option>
            <option value="4WD">{{ currentLanguage === 'th' ? '4WD ' : '4WD ' }}</option>
          </select>

          <select
            v-model="selectedTransmission"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ประเภทเกียร์ทั้งหมด' : 'All Transmissions' }}</option>
            <option value="Automatic">{{ currentLanguage === 'th' ? 'อัตโนมัติ' : 'Automatic' }}</option>
            <option value="Manual">{{ currentLanguage === 'th' ? 'ธรรมดา' : 'Manual' }}</option>
            <option value="Semi-Automatic">{{ currentLanguage === 'th' ? 'กึ่งอัตโนมัติ' : 'Semi-Automatic' }}</option>
            <option value="CVT">{{ currentLanguage === 'th' ? 'CVT' : 'CVT' }}</option>
            <option value="e-CVT">{{ currentLanguage === 'th' ? 'e-CVT' : 'e-CVT' }}</option>
            <option value="DCT">{{ currentLanguage === 'th' ? 'DCT' : 'DCT' }}</option>
          </select>

          <!-- Car Type -->
          <select
            v-model="selectedCarType"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ประเภทรถทั้งหมด' : 'All Car Types' }}</option>
            <option v-for="carType in uniqueCarTypes" :key="carType" :value="carType">
              {{ carType }}
            </option>
          </select>

          <!-- Engine Size -->
          <select
            v-model="selectedEngineSize"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'ขนาดเครื่องยนต์ทั้งหมด' : 'All Engine Sizes' }}</option>
            <option v-for="engineSize in uniqueEngineSizes" :key="engineSize" :value="engineSize">
              {{ engineSize }} cc
            </option>
          </select>

          <!-- Min Price Input -->
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">{{ currentLanguage === 'th' ? 'ราคาเริ่มต้น:' : 'Min Price:' }}</span>
            <input
              v-model.number="minPriceInput"
              type="number"
              placeholder="฿0"
              class="px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all w-32"
            />
          </div>

          <!-- Max Price Input -->
          <div class="flex items-center gap-2">
            <span class="text-gray-400 text-sm">{{ currentLanguage === 'th' ? 'ราคาสูงสุด:' : 'Max Price:' }}</span>
            <input
              v-model.number="maxPriceInput"
              type="number"
              placeholder="฿999999999"
              class="px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500 transition-all w-32"
            />
          </div>

          <select
            v-model="selectedColor"
            class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
          >
            <option value="">{{ currentLanguage === 'th' ? 'สีทั้งหมด' : 'All Colors' }}</option>
            <option v-for="color in uniqueColors" :key="color" :value="color">
              {{ color }}
            </option>
          </select>
        </div>

        <!-- Cars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in-up">
          <div v-if="filteredCars.length === 0" class="col-span-full text-center py-16">
            <i class="fas fa-search text-6xl text-gray-600 mb-4"></i>
            <p class="text-gray-400 text-xl">{{ currentLanguage === 'th' ? 'ไม่พบ' : 'No' }} {{ selectedBrand }} {{ currentLanguage === 'th' ? 'รถ' : 'cars' }} found matching your criteria</p>
          </div>

          <div
            v-for="(car, index) in filteredCars"
            :key="car.id || car._id"
            class="bg-gray-900/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 opacity-0 animate-fade-in-up border border-gray-800 hover:border-red-500/50 group"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <!-- Image -->
            <div class="relative h-48 overflow-hidden rounded-t-2xl group/image">
              <img
                :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/400x250?text=No+Image'"
                :alt="car.model"
                class="w-full h-full object-cover group-hover/image:scale-110 transition-transform duration-500"
              />
              <!-- Status Badge -->
              <div v-if="!car.sold && !car.sold_out" class="absolute top-4 right-4 bg-green-600 px-3 py-1 rounded-full text-xs font-bold text-white">
                <i class="fas fa-check-circle mr-1"></i>{{ currentLanguage === 'th' ? 'ว่าง' : 'Available' }}
              </div>
              <!-- Sold Out Badge -->
              <div v-else class="absolute top-4 right-4 bg-red-600 px-3 py-1 rounded-full text-xs font-bold text-white">
                <i class="fas fa-times-circle mr-1"></i>{{ currentLanguage === 'th' ? 'หมด' : 'SOLD OUT' }}
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <!-- Title -->
              <h2 class="text-xl font-bold text-white mb-2 group-hover:text-red-400 transition-colors">
                {{ car.brand }} {{ car.model }}
              </h2>

              <!-- Year & Type -->
              <div class="flex justify-between items-center mb-3 text-sm text-gray-400">
                <span><i class="fas fa-calendar mr-2 text-red-500"></i>{{ car.year }}</span>
                <span v-if="car.car_type" class="bg-red-500/20 px-3 py-1 rounded-lg text-red-400 font-semibold text-xs">{{ car.car_type }}</span>
              </div>

              <!-- Fuel & Transmission -->
              <div v-if="car.fuel_type || car.transmission" class="flex gap-2 mb-4 flex-wrap">
                <span v-if="car.fuel_type" class="text-xs bg-blue-500/20 text-blue-400 px-3 py-1 rounded-lg font-semibold">
                  <i class="fas fa-gas-pump mr-1"></i>{{ car.fuel_type }}
                </span>
                <span v-if="car.transmission" class="text-xs bg-green-500/20 text-green-400 px-3 py-1 rounded-lg font-semibold">
                  <i class="fas fa-cog mr-1"></i>{{ car.transmission }}
                </span>
              </div>

              <!-- Additional Info -->
              <div class="grid grid-cols-2 gap-2 mb-4 text-xs text-gray-400">
                <div v-if="car.mileage" class="flex items-center">
                  <i class="fas fa-tachometer-alt text-red-500 mr-1"></i>
                  <span>{{ formatMileage(car.mileage) }} km</span>
                </div>
                <div v-if="car.color" class="flex items-center">
                  <i class="fas fa-palette text-pink-500 mr-1"></i>
                  <span>{{ car.color }}</span>
                </div>
              </div>

              <!-- Price -->
              <div class="flex items-baseline justify-between mb-4 pb-4 border-b border-gray-700">
                <p class="text-3xl font-bold text-red-500">
                  ฿{{ car.price.toLocaleString('th-TH') }}
                </p>
                <span class="text-xs text-gray-400">{{ currentLanguage === 'th' ? 'ราคาโดยประมาณ' : 'Est. Price' }}</span>
              </div>

              <!-- Description -->
              <p class="text-gray-400 text-sm mb-4 line-clamp-2">{{ car.description }}</p>

              <!-- Button -->
              <NuxtLink
                :to="`/car/${car.id || car._id}`"
                class="w-full inline-block py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 text-center shadow-lg"
              >
                <i class="fas fa-eye mr-2"></i>{{ currentLanguage === 'th' ? 'ดูรายละเอียด' : 'View Details' }}
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
import { useRoute } from 'vue-router'
import LoadingSpinner from '~/components/LoadingSpinner.vue'
import Beams from '~/components/Beams.vue'

const route = useRoute()
const { t, currentLanguage } = useLanguage()
const selectedBrand = ref('')
const brandLogo = ref('')
const brandCars = ref([])
const loading = ref(true)

const searchQuery = ref('')
const selectedYear = ref('')
const selectedFuelType = ref('')
const selectedGasSystem = ref('')
const selectedDriveSystem = ref('')
const selectedTransmission = ref('')
const selectedCarType = ref('')
const selectedEngineSize = ref('')
const selectedColor = ref('')
const minPriceInput = ref('')
const maxPriceInput = ref('')

// Brand logos mapping - fallback to public images
const brandLogos = {
  'Toyota': '/images/brands/Toyota.png',
  'Honda': '/images/brands/Honda.png',
  'BMW': '/images/brands/BMW.png',
  'Mercedes': '/images/brands/Mercedes.png',
  'Audi': '/images/brands/Audi.png',
  'Ford': '/images/brands/Ford.png',
  'Chevrolet': '/images/brands/Chevrolet.png',
  'Nissan': '/images/brands/Nissan.png',
  'Mazda': '/images/brands/Mazda.png',
  'Mitsubishi': '/images/brands/Mitsubishi.png'
}

const fetchBrandCars = async () => {
  loading.value = true
  try {
    const brandParam = route.params.id
    // Capitalize first letter of each word
    const brand = brandParam
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join('-')
    
    selectedBrand.value = brand

    // Fetch ALL cars from API
    const response = await fetch(`http://localhost:5000/api/cars`)
    const data = await response.json()

    console.log('Fetching cars for brand:', brand)
    console.log('Total cars in DB:', data.cars?.length || 0)

    if (data.success && data.cars && Array.isArray(data.cars)) {
      // Filter cars by brand - case insensitive
      const filteredByBrand = data.cars.filter(car => {
        return car.brand && car.brand.toLowerCase() === brand.toLowerCase()
      })
      
      brandCars.value = filteredByBrand
      console.log('Cars found for', brand, ':', brandCars.value.length)

      // Set brand logo from first car's image
      if (brandCars.value.length > 0) {
        // ✅ Use static brand logo from public folder instead of car image
        const brandName = brand.replace('-', '').toLowerCase()
        brandLogo.value = `/images/brands/${brand}.png`
        console.log('Brand logo set:', brandLogo.value)
      }
    } else {
      console.warn('No cars found in database')
      brandCars.value = []
    }
  } catch (error) {
    console.error('Error fetching cars:', error)
    brandCars.value = []
  } finally {
    loading.value = false
  }
}

const minPrice = computed(() => {
  if (filteredCars.value.length === 0) return 0
  return Math.min(...filteredCars.value.map(c => c.price))
})

const maxPrice = computed(() => {
  if (filteredCars.value.length === 0) return 0
  return Math.max(...filteredCars.value.map(c => c.price))
})

const availableCount = computed(() => {
  return brandCars.value.filter(car => !car.sold && !car.sold_out).length
})

const uniqueColors = computed(() => {
  const colors = [...new Set(brandCars.value
    .map((car) => car.color)
    .filter((color) => color && color.trim() !== '')
  )]
  return colors.sort()
})

const uniqueYears = computed(() => {
  const years = [...new Set(brandCars.value
    .map((car) => car.year)
    .filter((year) => year)
  )]
  return years.sort((a, b) => b - a)
})

const uniqueCarTypes = computed(() => {
  const carTypes = [...new Set(brandCars.value
    .map((car) => car.car_type)
    .filter((type) => type && type.trim() !== '')
  )]
  return carTypes.sort()
})

const uniqueEngineSizes = computed(() => {
  const sizes = [...new Set(brandCars.value
    .map((car) => car.engine_size)
    .filter((size) => size)
  )]
  return sizes.sort((a, b) => a - b)
})

const uniqueGasSystems = computed(() => {
  if (!selectedFuelType.value) return []
  const gasSystems = [...new Set(brandCars.value
    .filter((car) => car.fuel_type === selectedFuelType.value)
    .map((car) => car.gas_system)
    .filter((system) => system && system.trim() !== '')
  )]
  return gasSystems.sort()
})

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const filteredCars = computed(() => {
  return brandCars.value.filter(car => {
    // Hide sold cars
    if (car.sold || car.sold_out) return false
    
    // Search filter - search by model, color, fuel type
    if (searchQuery.value) {
      const search = searchQuery.value.toLowerCase()
      const matchesSearch = 
        car.model.toLowerCase().includes(search) ||
        car.brand.toLowerCase().includes(search) ||
        (car.color && car.color.toLowerCase().includes(search)) ||
        (car.fuel_type && car.fuel_type.toLowerCase().includes(search)) ||
        (car.car_type && car.car_type.toLowerCase().includes(search))
      
      if (!matchesSearch) return false
    }
    
    // Year filter
    if (selectedYear.value && car.year !== parseInt(selectedYear.value)) return false
    
    // Fuel type filter
    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false
    
    // Gas system filter (only if fuel type selected)
    if (selectedGasSystem.value && car.gas_system !== selectedGasSystem.value) return false
    
    // Drive system filter
    if (selectedDriveSystem.value && car.drive_system !== selectedDriveSystem.value) return false
    
    // Transmission filter
    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false
    
    // Car type filter
    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false
    
    // Engine size filter
    if (selectedEngineSize.value && car.engine_size !== parseInt(selectedEngineSize.value)) return false
    
    // Color filter
    if (selectedColor.value && car.color !== selectedColor.value) return false

    // Price range filter - with input fields
    if (minPriceInput.value && car.price < minPriceInput.value) return false
    if (maxPriceInput.value && car.price > maxPriceInput.value) return false

    return true
  })
})

onMounted(() => {
  fetchBrandCars()
})
</script>

<style scoped>
.brandcars-page {
  position: relative;
}

.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.3;
  pointer-events: none;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-down {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.animate-fade-in-up {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

.bg-gray-900\/80 {
  animation: fade-in 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
</style>
