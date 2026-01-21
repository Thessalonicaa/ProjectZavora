
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

    <div class="max-w-4xl mx-auto relative z-10">
     

      <!-- Page Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-4">
          {{ currentLanguage === 'th' ? 'แก้ไขรายการรถ' : 'Edit Car Listing' }}
        </h1>
        <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'อัปเดตข้อมูลรถของคุณ' : 'Update Your Car Information' }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <i class="fas fa-spinner animate-spin text-4xl text-red-500 mb-4"></i>
        <p class="text-gray-400">{{ currentLanguage === 'th' ? 'กำลังโหลด...' : 'Loading...' }}</p>
      </div>

      <!-- Form Section -->
      <div v-else-if="carData" class="bg-gradient-to-br from-gray-900/80 via-gray-800/50 to-gray-950/80 backdrop-blur-xl rounded-3xl p-8 border border-gray-800/50 hover:border-red-500/30 transition-all duration-300 shadow-xl">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Brand & Model Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-car text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ยี่ห้อ' : 'Brand' }} *
              </label>
              <input
                v-model="carData.brand"
                type="text"
                placeholder="e.g., Toyota"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              />
            </div>
            <div>
              <label class="block text-white font-semibold mb-2">
                {{ currentLanguage === 'th' ? 'รุ่น' : 'Model' }} *
              </label>
              <input
                v-model="carData.model"
                type="text"
                placeholder="e.g., Camry"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              />
            </div>
          </div>

          <!-- Year & Price Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-calendar text-blue-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ปี' : 'Year' }} *
              </label>
              <input
                v-model.number="carData.year"
                type="number"
                :min="new Date().getFullYear() - 50"
                :max="new Date().getFullYear()"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              />
            </div>
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-tag text-green-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ราคา' : 'Price' }} (฿) *
              </label>
              <input
                v-model.number="carData.price"
                type="number"
                placeholder="0"
                min="0"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              />
            </div>
          </div>

          <!-- Fuel Type & Transmission Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-gas-pump text-orange-500 mr-2"></i>{{ currentLanguage === 'th' ? 'เชื้อเพลิง' : 'Fuel Type' }} *
              </label>
              <select
                v-model="carData.fuel_type"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              >
                <option value="">Select Fuel Type</option>
                <option value="Petrol">Petrol</option>
                <option value="Diesel">Diesel</option>
                <option value="Hybrid">Hybrid</option>
                <option value="Electric">Electric</option>
              </select>
            </div>
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-cog text-purple-500 mr-2"></i>{{ currentLanguage === 'th' ? 'เกียร์' : 'Transmission' }} *
              </label>
              <select
                v-model="carData.transmission"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
                required
              >
                <option value="">Select Transmission</option>
                <option value="Automatic">Automatic</option>
                <option value="Manual">Manual</option>
              </select>
            </div>
          </div>

          <!-- Car Type -->
          <div>
            <label class="block text-white font-semibold mb-2">
              <i class="fas fa-cube text-indigo-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทรถ' : 'Car Type' }} *
            </label>
            <select
              v-model="carData.car_type"
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
              required
            >
              <option value="">Select Car Type</option>
              <option value="Sedan">Sedan</option>
              <option value="SUV">SUV</option>
              <option value="Pickup">Pickup</option>
              <option value="Van">Van</option>
              <option value="Sports">Sports</option>
              <option value="Convertible">Convertible</option>
              <option value="MPV">MPV</option>
              <option value="Truck">Truck</option>
              <option value="Hatchback">Hatchback</option>
            </select>
          </div>

          <!-- License Plate & Mileage Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-white font-semibold mb-2">
                {{ currentLanguage === 'th' ? 'หมายเลขทะเบียน' : 'License Plate' }}
              </label>
              <input
                v-model="carData.license_plate"
                type="text"
                placeholder="e.g., ABC 1234"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label class="block text-white font-semibold mb-2">
                <i class="fas fa-tachometer-alt text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'เลขไมล์' : 'Mileage' }} (km)
              </label>
              <input
                v-model.number="carData.mileage"
                type="number"
                placeholder="0"
                min="0"
                class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all"
              />
            </div>
          </div>

          <!-- Description -->
          <div>
            <label class="block text-white font-semibold mb-2">
              <i class="fas fa-align-left text-yellow-500 mr-2"></i>{{ currentLanguage === 'th' ? 'รายละเอียด' : 'Description' }}
            </label>
            <textarea
              v-model="carData.description"
              rows="4"
              placeholder="Describe your car..."
              class="w-full p-3 border border-gray-600 bg-gray-800/50 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all resize-none"
            ></textarea>
          </div>

          <!-- Submit Button -->
          <div class="flex gap-4 pt-6 border-t border-gray-700">
            <button
              type="button"
              @click="goBack"
              class="flex-1 p-4 rounded-lg bg-gray-700 hover:bg-gray-600 text-white font-bold text-lg shadow-lg transition-all transform hover:scale-105 active:scale-95"
            >
              <i class="fas fa-arrow-left mr-2"></i>{{ currentLanguage === 'th' ? 'ยกเลิก' : 'Cancel' }}
            </button>
            <button
              type="submit"
              :disabled="isSubmitting"
              class="flex-1 p-4 rounded-lg bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white font-bold text-lg shadow-lg hover:shadow-orange-500/50 transition-all transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              <i v-if="!isSubmitting" class="fas fa-save mr-2"></i>
              <i v-else class="fas fa-spinner animate-spin mr-2"></i>
              {{ isSubmitting ? (currentLanguage === 'th' ? 'กำลังบันทึก...' : 'Saving...') : (currentLanguage === 'th' ? 'บันทึก' : 'Save Changes') }}
            </button>
          </div>
        </form>

        <!-- Error Message -->
        <div v-if="errorMsg" class="mt-6 p-4 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 flex items-start gap-3">
          <i class="fas fa-exclamation-circle mt-1"></i>
          <span>{{ errorMsg }}</span>
        </div>

        <!-- Success Message -->
        <div v-if="successMsg" class="mt-6 p-4 bg-green-900/20 border border-green-500/50 rounded-lg text-green-400 flex items-start gap-3">
          <i class="fas fa-check-circle mt-1"></i>
          <span>{{ successMsg }}</span>
        </div>
      </div>

      <!-- Car Not Found -->
      <div v-else class="text-center py-12">
        <i class="fas fa-exclamation-triangle text-4xl text-red-500 mb-4"></i>
        <p class="text-gray-400 text-xl">{{ currentLanguage === 'th' ? 'ไม่พบรถ' : 'Car not found' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useLanguage } from '~/composables/useLanguage'
import Beams from '~/components/Beams.vue'

const router = useRouter()
const route = useRoute()
const { currentLanguage } = useLanguage()

const carData = ref(null)
const isLoading = ref(true)
const isSubmitting = ref(false)
const errorMsg = ref('')
const successMsg = ref('')
const carId = route.params.id

const goBack = () => {
  router.back()
}

onMounted(async () => {
  await fetchCarData()
})

const fetchCarData = async () => {
  try {
    isLoading.value = true
    const token = localStorage.getItem('token')
    
    const response = await fetch(`http://localhost:5000/api/cars/${carId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (data.success && data.car) {
      carData.value = {
        brand: data.car.brand || '',
        model: data.car.model || '',
        year: data.car.year || new Date().getFullYear(),
        price: data.car.price || 0,
        fuel_type: data.car.fuel_type || '',
        transmission: data.car.transmission || '',
        car_type: data.car.car_type || '',
        license_plate: data.car.license_plate || '',
        mileage: data.car.mileage || 0,
        description: data.car.description || ''
      }
    } else {
      errorMsg.value = currentLanguage.value === 'th' ? 'ไม่พบรถ' : 'Car not found'
    }
  } catch (error) {
    console.error('Error fetching car:', error)
    errorMsg.value = currentLanguage.value === 'th' ? 'เกิดข้อผิดพลาด' : 'An error occurred'
  } finally {
    isLoading.value = false
  }
}

const handleSubmit = async () => {
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    successMsg.value = ''

    // Validate required fields
    if (!carData.value.brand || !carData.value.model || !carData.value.year || !carData.value.price || !carData.value.fuel_type || !carData.value.transmission || !carData.value.car_type) {
      errorMsg.value = currentLanguage.value === 'th' ? 'กรุณากรอกข้อมูลที่จำเป็น' : 'Please fill in all required fields'
      return
    }

    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/cars/${carId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(carData.value)
    })

    const data = await response.json()

    if (response.ok && data.success) {
      successMsg.value = currentLanguage.value === 'th' ? 'บันทึกสำเร็จ!' : 'Changes saved successfully!'
      
      setTimeout(() => {
        router.back()
      }, 1500)
    } else {
      errorMsg.value = data.message || data.error || (currentLanguage.value === 'th' ? 'เกิดข้อผิดพลาด' : 'An error occurred')
    }
  } catch (error) {
    console.error('Update car error:', error)
    errorMsg.value = currentLanguage.value === 'th' ? 'เกิดข้อผิดพลาดในการเชื่อมต่อ' : 'Connection error'
  } finally {
    isSubmitting.value = false
  }
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

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
