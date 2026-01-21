<template>
  <div class="carlist-page min-h-screen bg-gray-950 p-8 text-gray-100 relative overflow-hidden">
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

    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Header -->
      <div class="mb-12 animate-fade-in">
        <h1 class="text-5xl font-extrabold text-white mb-3 tracking-wide">
          {{ currentLanguage === 'th' ? 'รายการรถยนต์' : 'Car List' }}
        </h1>
        <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'ค้นหาและค้นพบรถยนต์ที่สมบูรณ์แบบของคุณ' : 'Find and discover your perfect car' }}</p>
      </div>

      <!-- Filters -->
      <div class="mb-8 flex flex-wrap gap-4 animate-fade-in-up">
        <select
          v-model="selectedVehicleType"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ประเภทยานพาหนะทั้งหมด' : 'All Vehicle Types' }}</option>
          <option value="Car">{{ currentLanguage === 'th' ? 'รถยนต์' : 'Car' }}</option>
          <option value="Motorcycle">{{ currentLanguage === 'th' ? 'มอเตอร์ไซค์' : 'Motorcycle' }}</option>
          <option value="Bike">{{ currentLanguage === 'th' ? 'จักรยาน' : 'Bike' }}</option>
        </select>

        <select
          v-model="selectedBrand"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'แบรนด์ทั้งหมด' : 'All Brands' }}</option>
          <option v-for="brand in brands" :key="brand" :value="brand">
            {{ brand }}
          </option>
        </select>

        <select
          v-model="selectedFuelType"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ประเภทเชื้อเพลิงทั้งหมด' : 'All Fuel Types' }}</option>
          <option v-for="fuel in fuelTypes" :key="fuel" :value="fuel">
            {{ fuel }}
          </option>
        </select>

        <select
          v-model="selectedTransmission"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Transmissions' }}</option>
          <option v-for="transmission in transmissions" :key="transmission" :value="transmission">
            {{ transmission }}
          </option>
        </select>

        <!--  Drive System -->
        <select
          v-model="selectedDriveSystem"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Drive Systems' }}</option>
          <option v-for="system in driveSystems" :key="system" :value="system">
            {{ system }}
          </option>
        </select>

        <select
          v-model="selectedCarType"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Car Types' }}</option>
          <option v-for="type in carTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>

        <!-- Dynamic Filter: MPV Size -->
        <select
          v-if="selectedCarType === 'MPV'"
          v-model="selectedMpvSize"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All MPV Sizes' }}</option>
          <option value="Compact">{{ currentLanguage === 'th' ? 'MPV ขนาดกะทัดรัด' : 'Compact MPV' }}</option>
          <option value="Mid-Size">{{ currentLanguage === 'th' ? 'MPV ขนาดกลาง' : 'Mid-Size MPV' }}</option>
          <option value="Full-Size">{{ currentLanguage === 'th' ? 'MPV ขนาดใหญ่' : 'Full-Size MPV' }}</option>
        </select>

        <!-- Dynamic Filter: Convertible Options -->
        <select
          v-if="selectedCarType === 'Convertible'"
          v-model="selectedConvertibleTop"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Top Types' }}</option>
          <option value="Soft Top">{{ currentLanguage === 'th' ? 'หลังคาผ้า' : 'Soft Top' }}</option>
          <option value="Retractable Hard Top">{{ currentLanguage === 'th' ? 'หลังคาแข็งพับได้' : 'Retractable Hard Top' }}</option>
        </select>

        <!-- Dynamic Filter: Van Type -->
        <select
          v-if="selectedCarType === 'Van'"
          v-model="selectedVanType"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Van Types' }}</option>
          <option value="Cargo Van">{{ currentLanguage === 'th' ? 'รถตู้ขนของ' : 'Cargo Van' }}</option>
          <option value="Minivan">{{ currentLanguage === 'th' ? 'มินิแวน' : 'Minivan' }}</option>
        </select>

        <!-- Dynamic Filter: SUV Seats -->
        <select
          v-if="selectedCarType === 'SUV'"
          v-model="selectedSuvSeats"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Seat Capacities' }}</option>
          <option value="2 Seats">{{ currentLanguage === 'th' ? '2 ที่นั่ง' : '2 Seats' }}</option>
          <option value="4 Seats">{{ currentLanguage === 'th' ? '4 ที่นั่ง' : '4 Seats' }}</option>
        </select>

        <!-- Dynamic Filter: Pickup Cab -->
        <select
          v-if="selectedCarType === 'Pickup'"
          v-model="selectedPickupCab"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Cab Types' }}</option>
          <option value="Single Cab">{{ currentLanguage === 'th' ? 'Single Cab – 2 ที่นั่ง' : 'Single Cab – 2 Seats' }}</option>
          <option value="Extra Cab">{{ currentLanguage === 'th' ? 'Extra Cab – 2 ที่นั่ง' : 'Extra Cab – 2 Seats' }}</option>
          <option value="Double Cab">{{ currentLanguage === 'th' ? 'Double Cab – 4 ที่นั่ง' : 'Double Cab – 4 Seats' }}</option>
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

        <!-- Color Filter -->
        <select
          v-model="selectedColor"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Colors' }}</option>
          <option v-for="color in colors" :key="color" :value="color">
            {{ color }}
          </option>
        </select>

        <!-- Engine Size Filter -->
        <select
          v-model="selectedEngineSize"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Engine Sizes' }}</option>
          <option v-for="engine in engineSizes" :key="engine" :value="engine">
            {{ engine }}
          </option>
        </select>

        <!-- Year Filter -->
        <select
          v-model="selectedYear"
          class="px-6 py-3 bg-gray-800/50 border border-gray-700 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-gray-600"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Years' }}</option>
          <option v-for="year in years" :key="year" :value="year">
            {{ year }}
          </option>
        </select>

        <!-- Dynamic Filter: Gas System (shown after Fuel Type selection) -->
        <select
          v-if="selectedFuelType"
          v-model="selectedGasSystem"
          class="px-6 py-3 bg-gray-800/50 border border-red-600 rounded-xl text-gray-200 focus:ring-2 transition-all hover:border-red-500"
        >
          <option value="">{{ currentLanguage === 'th' ? 'ทั้งหมด' : 'All Gas Systems' }}</option>
          <option v-for="system in gasSystems" :key="system" :value="system">
            {{ system }}
          </option>
        </select>
      </div>

      <!-- Car Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in-up">
        <div v-if="loading" class="col-span-full text-center py-16">
          <div class="inline-flex flex-col items-center">
            <div class="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'กำลังโหลดรถ...' : 'Loading cars...' }}</p>
          </div>
        </div>

        <div
          v-for="(car, index) in filteredCars"
          :key="car.id || car._id"
          class="bg-gray-900/80 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 hover:scale-105 opacity-0 animate-fade-in-up border border-gray-800 hover:border-red-500/50 group overflow-hidden relative"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Image -->
          <div class="relative h-48 overflow-hidden rounded-t-2xl group/image">
            <img
              :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/400x250?text=No+Image'"
              :alt="car.model"
              class="w-full h-full object-cover group-hover/image:scale-110 transition-transform duration-500"
            />
            <!-- Available Badge -->
            <div v-if="!car.sold" class="absolute top-4 right-4 bg-green-600 px-4 py-2 rounded-full text-xs font-bold text-white shadow-lg">
              <i class="fas fa-check-circle mr-1"></i>{{ currentLanguage === 'th' ? 'ว่าง' : 'Available' }}
            </div>
            <!-- Sold Out Badge -->
            <div v-else class="absolute top-4 right-4 bg-red-600 px-4 py-2 rounded-full text-xs font-bold text-white shadow-lg">
              <i class="fas fa-ban mr-1"></i>{{ currentLanguage === 'th' ? 'หมดแล้ว' : 'SOLD OUT' }}
            </div>
            <!-- Car Type Badge -->
            <div v-if="car.car_type" class="absolute bottom-4 right-4 bg-red-600/80 px-4 py-2 rounded-lg text-xs font-bold text-white shadow-lg">
              {{ car.car_type }}
            </div>
          </div>

          <!-- Content -->
          <div class="p-6">
            <!-- Title -->
            <h2 class="text-xl font-bold text-white mb-4">
              {{ car.brand }} {{ car.model }}
            </h2>

            <!-- Specs Row -->
            <div class="flex flex-wrap gap-2 mb-4">
              <span v-if="car.fuel_type" class="text-xs bg-blue-600/30 text-blue-300 px-3 py-1 rounded-lg font-semibold">
                <i class="fas fa-gas-pump mr-1"></i>{{ car.fuel_type }}
              </span>
              <span v-if="car.transmission" class="text-xs bg-green-600/30 text-green-300 px-3 py-1 rounded-lg font-semibold">
                <i class="fas fa-cog mr-1"></i>{{ car.transmission }}
              </span>
            </div>

            <!-- Info Grid -->
            <div class="grid grid-cols-2 gap-3 mb-4 text-xs text-gray-400">
              <div v-if="car.mileage">
                <i class="fas fa-tachometer-alt text-red-500 mr-1"></i>
                <span>{{ formatMileage(car.mileage) }} {{ currentLanguage === 'th' ? '' : 'km' }}</span>
              </div>
              <div v-if="car.color">
                <i class="fas fa-palette text-pink-500 mr-1"></i>
                <span>{{ car.color }}</span>
              </div>
            </div>

            <!-- Price Section -->
            <div class="flex items-center justify-between pt-4 border-t border-gray-700">
              <div v-if="!car.sold">
                <p class="text-gray-400 text-xs uppercase font-bold mb-1">{{ currentLanguage === 'th' ? 'ราคา' : 'Price' }}</p>
                <p class="text-3xl font-extrabold text-red-500">
                  ฿{{ car.price.toLocaleString('th-TH') }}
                </p>
              </div>
              <div v-else class="flex-1">
                <p class="text-2xl font-extrabold text-gray-500">
                  SOLD OUT
                </p>
              </div>
              <span v-if="!car.sold" class="text-gray-400 text-xs">{{ currentLanguage === 'th' ? 'ราคาโดยประมาณ:' : 'Est. Price:' }}</span>
            </div>

            <!-- View Button / Sold Out Message -->
            <NuxtLink
              v-if="!car.sold"
              :to="`/car/${car.id || car._id}`"
              class="w-full block mt-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all transform hover:scale-105 duration-300 text-center shadow-lg"
            >
              <i class="fas fa-eye mr-2"></i>{{ currentLanguage === 'th' ? 'ดูรายละเอียด' : 'View Details' }}
            </NuxtLink>
            <div v-else class="w-full block mt-4 py-3 bg-gradient-to-r from-gray-600 to-gray-700 text-gray-300 font-bold rounded-xl text-center shadow-lg cursor-not-allowed opacity-70">
              <i class="fas fa-lock mr-2"></i>{{ currentLanguage === 'th' ? 'ไม่สามารถใช้งานได้' : 'Not Available' }}
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredCars.length === 0 && !loading" class="col-span-full text-center py-16">
          <i class="fas fa-search text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400 text-xl">{{ t('carlist.noResults') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import Beams from "~/components/Beams.vue"
import { useLanguage } from "~/composables/useLanguage"

const { t, currentLanguage } = useLanguage()

const selectedBrand = ref("");
const priceRange = ref("");
const selectedFuelType = ref("");
const selectedTransmission = ref("");
const selectedDriveSystem = ref("");
const selectedCarType = ref("");
const selectedMpvSize = ref("");
const selectedConvertibleTop = ref("");
const selectedVanType = ref("");
const selectedSuvSeats = ref("");
const selectedPickupCab = ref("");
const selectedColor = ref("");
const selectedEngineSize = ref("");
const selectedVehicleType = ref("");
const selectedGasSystem = ref("");
const selectedYear = ref("");
const minPriceInput = ref("");
const maxPriceInput = ref("");
const cars = ref([]);
const loading = ref(true);
const route = useRoute();
const rerender = ref(0);

const fetchCars = async () => {
  loading.value = true;
  try {
    console.log('Fetching cars from API...');
    const response = await fetch('http://localhost:5000/api/cars');
    console.log('Response status:', response.status);
    
    const data = await response.json();
    console.log('Cars data:', data);
    console.log('Engine sizes in data:', data.cars?.map(c => c.engine_size).filter(e => e));

    if (data.success) {
      cars.value = data.cars || [];
      console.log('Cars loaded:', cars.value.length);
      console.log('Unique engine sizes:', [...new Set(cars.value.map(c => c.engine_size).filter(e => e))]);
    } else {
      console.log('API returned success: false');
      cars.value = [];
    }
  } catch (error) {
    console.error('Error fetching cars:', error);
    cars.value = [];
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  console.log('CarList mounted - fetching cars');
  await fetchCars();
  // Refetch cars every 10 seconds to stay updated
  setInterval(fetchCars, 10000);
  
  // ✅ Listen for language changes
  if (typeof window !== 'undefined') {
    window.addEventListener('language-changed', () => {
      rerender.value += 1
    })
  }
});

watch(
  () => route.path,
  async () => {
    console.log('Route changed - refetching cars');
    await fetchCars();
  },
  { immediate: false }
);

// ✅ Watch for language changes
watch(() => currentLanguage.value, () => {
  console.log('🌐 Language changed in CarList:', currentLanguage.value)
  rerender.value += 1
})

// ✅ Dynamic Brands
const brands = computed(() => {
  const brandList = [...new Set(cars.value
    .map((car) => car.brand)
    .filter((brand) => brand && brand.trim() !== '')
  )];
  return brandList.sort();
});

// ✅ Dynamic Colors
const colors = computed(() => {
  const uniqueColors = [...new Set(cars.value
    .map((car) => car.color)
    .filter((color) => color && color.trim() !== '')
  )];
  return uniqueColors.sort();
});

// ✅ Dynamic Engine Sizes
const engineSizes = computed(() => {
  const uniqueEngineSizes = [...new Set(cars.value
    .map((car) => car.engine_size)
    .filter((engine) => engine)
  )];
  return uniqueEngineSizes.sort((a, b) => a - b);
});

// ✅ Dynamic Years
const years = computed(() => {
  const uniqueYears = [...new Set(cars.value
    .map((car) => car.year)
    .filter((year) => year && year > 0)
  )];
  return uniqueYears.sort((a, b) => b - a); // Newest first
});

// ✅ Dynamic Car Types
const carTypes = computed(() => {
  const types = [...new Set(cars.value
    .map((car) => car.car_type)
    .filter((type) => type && type.trim() !== '')
  )];
  return types.sort();
});

// ✅ Dynamic Fuel Types
const fuelTypes = computed(() => {
  const types = [...new Set(cars.value
    .map((car) => car.fuel_type)
    .filter((type) => type && type.trim() !== '')
  )];
  return types.sort();
});

// ✅ Dynamic Transmissions
const transmissions = computed(() => {
  const types = [...new Set(cars.value
    .map((car) => car.transmission)
    .filter((type) => type && type.trim() !== '')
  )];
  return types.sort();
});

// ✅ Dynamic Drive Systems
const driveSystems = computed(() => {
  const types = [...new Set(cars.value
    .map((car) => car.drive_system)
    .filter((type) => type && type.trim() !== '')
  )];
  return types.sort();
});

// ✅ Dynamic Gas Systems (filtered by selected fuel type)
const gasSystems = computed(() => {
  if (!selectedFuelType.value) return [];
  const systems = [...new Set(cars.value
    .filter((car) => car.fuel_type === selectedFuelType.value)
    .map((car) => car.gas_system)
    .filter((system) => system && system.trim() !== '')
  )];
  return systems.sort();
});

const formatMileage = (mileage) => {
  if (!mileage) return '0'
  return mileage.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

const filteredCars = computed(() => {
  return cars.value.filter((car) => {
    // ✅ Hide sold out cars first
    if (car.sold || car.sold_out) return false;

    // Vehicle Type filter
    if (selectedVehicleType.value && car.vehicle_type !== selectedVehicleType.value) return false;

    if (selectedBrand.value && car.brand !== selectedBrand.value) return false;

    if (selectedFuelType.value && car.fuel_type !== selectedFuelType.value) return false;

    if (selectedTransmission.value && car.transmission !== selectedTransmission.value) return false;

    if (selectedDriveSystem.value && car.drive_system !== selectedDriveSystem.value) return false;

    if (selectedCarType.value && car.car_type !== selectedCarType.value) return false;

    // Dynamic filter: MPV Size
    if (selectedMpvSize.value && car.mpv_size !== selectedMpvSize.value) return false;

    // Dynamic filter: Convertible Top
    if (selectedConvertibleTop.value && car.convertible_top !== selectedConvertibleTop.value) return false;

    // Dynamic filter: Van Type
    if (selectedVanType.value && car.van_type !== selectedVanType.value) return false;

    // Dynamic filter: SUV Seats
    if (selectedSuvSeats.value && car.suv_seats !== selectedSuvSeats.value) return false;

    // Dynamic filter: Pickup Cab
    if (selectedPickupCab.value && car.pickup_cab !== selectedPickupCab.value) return false;

    // Color filter (exact match)
    if (selectedColor.value && car.color !== selectedColor.value) return false;

    // Engine Size filter (exact match)
    if (selectedEngineSize.value && car.engine_size !== selectedEngineSize.value) return false;

    // Year filter
    if (selectedYear.value && car.year !== parseInt(selectedYear.value)) return false;

    // Gas System filter
    if (selectedGasSystem.value && car.gas_system !== selectedGasSystem.value) return false;

    // Price range filter - with input fields
    if (minPriceInput.value && car.price < minPriceInput.value) return false;
    if (maxPriceInput.value && car.price > maxPriceInput.value) return false;

    return true;
  });
});
</script>

<style scoped>
.carlist-page {
  position: relative;
}

/* Fade-in animations */
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
.animate-fade-in {
  animation: fade-in 1s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.animate-fade-in-up {
  animation: fade-in 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

/* Card hover effect enhancement */
.group:hover {
  box-shadow: 0 0 30px rgba(239, 68, 68, 0.2);
}
</style>
