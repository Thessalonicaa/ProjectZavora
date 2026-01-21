<template>
  <div class="mylistings-page min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
    <!-- Beams Background -->
    <div class="beams-background">
      <Beams
        :beamWidth="3"
        :beamHeight="25"
        :beamNumber="10"
        lightColor="#ff3c03"
        :speed="1.2"
        :noiseIntensity="1.7"
        :scale="0.22"
        :rotation="10"
        :width="1920"
        :height="1080"
      />
    </div>

    <div class="max-w-6xl mx-auto relative z-10">
      <!-- Header -->
      <div class="text-center mb-12 animate-slide-down">
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2 drop-shadow-lg">
          <i class="fas fa-list mr-3"></i>{{ currentLanguage === 'th' ? 'รายการรถของฉัน' : 'My Car Listings' }}
        </h1>
        <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'จัดการและติดตามรายการรถของคุณ' : 'Manage and Monitor Your Car Listings' }}</p>
      </div>

      <!-- No Listings -->
      <div v-if="sellerCars.length === 0" class="text-center py-16 animate-fade-in">
        <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
        <p class="text-2xl text-gray-400 mb-6">{{ currentLanguage === 'th' ? 'ยังไม่มีรถที่ลงทะเบียน' : 'No Cars Listed Yet' }}</p>
        <NuxtLink
          to="/seller/PostCar"
          class="inline-block px-8 py-3 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white rounded-xl transition-all transform hover:scale-105 font-semibold shadow-lg"
        >
          <i class="fas fa-plus mr-2"></i>{{ currentLanguage === 'th' ? 'ลงประกาศขายรถ' : 'Post a Car for Sale' }}
        </NuxtLink>
      </div>

      <!-- Listings Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 animate-fade-in">
        <div
          v-for="(car, index) in sellerCars"
          :key="car.id || car._id"
          :to="`/car/${car._id || car.id}`"
          class="group relative bg-gradient-to-br from-gray-900/80 via-gray-900/80 to-gray-950/80 backdrop-blur-xl rounded-2xl overflow-hidden border border-gray-800 hover:border-red-500/50 transition-all transform hover:-translate-y-2 duration-300 shadow-lg hover:shadow-2xl hover:shadow-red-600/30 animate-card-appear"
          :style="{ 'animation-delay': `${index * 0.1}s` }"
        >
          <!-- Image Container -->
          <div class="relative h-56 overflow-hidden">
            <img
              :src="car.images && car.images.length > 0 ? car.images[0] : 'https://via.placeholder.com/400x300?text=No+Image'"
              :alt="car.model"
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            
            <!-- Status Overlay for Sold Out -->
            <transition name="fade-overlay">
              <div v-if="car.sold_out" class="absolute inset-0 bg-black/70 flex items-center justify-center backdrop-blur-sm">
                <div class="text-center animate-bounce-soft">
                  <i class="fas fa-check-circle text-4xl text-green-400 mb-2 block"></i>
                  <span class="text-3xl font-extrabold text-green-400">{{ currentLanguage === 'th' ? 'ขายแล้ว' : 'SOLD OUT' }}</span>
                </div>
              </div>
            </transition>

            <!-- Status Badge -->
            <div class="absolute top-4 right-4">
              <span v-if="!car.sold_out" class="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-green-700 rounded-full text-xs font-bold text-white shadow-lg hover:shadow-green-600/50 transition-all">
                <i class="fas fa-circle text-green-300 animate-pulse"></i>{{ currentLanguage === 'th' ? 'มีจำหน่าย' : 'Available' }}
              </span>
              <span v-else class="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 rounded-full text-xs font-bold text-white shadow-lg">
                <i class="fas fa-check-circle"></i>{{ currentLanguage === 'th' ? 'ขายแล้ว' : 'Sold' }}
              </span>
            </div>

            <!-- Car Type Badge -->
            <div v-if="car.car_type" class="absolute bottom-4 left-4 px-3 py-1 bg-blue-600/80 backdrop-blur-sm rounded-lg text-xs font-bold text-white shadow-lg">
              {{ car.car_type }}
            </div>
          </div>

          <!-- Content -->
          <div class="p-6 space-y-4">
            <!-- Title & Year -->
            <div>
              <h3 class="text-xl font-extrabold text-white group-hover:text-red-400 transition-colors">
                {{ car.brand }} {{ car.model }}
              </h3>
              <p class="text-sm text-gray-400 mt-1">
                <i class="fas fa-calendar text-red-500 mr-2"></i>{{ car.year }}
              </p>
            </div>

            <!-- Price & Status -->
            <div class="flex items-center justify-between pt-3 border-t border-gray-700">
              <div>
                <p v-if="!car.sold_out" class="text-gray-400 text-xs uppercase font-bold mb-1">{{ currentLanguage === 'th' ? 'ราคา' : 'Price' }}</p>
                <p v-if="!car.sold_out" class="text-3xl font-extrabold text-red-500">
                  ฿{{ formatPrice(car.price) }}
                </p>
                <p v-else class="text-2xl font-extrabold text-gray-500 line-through opacity-50">
                  ฿{{ formatPrice(car.price) }}
                </p>
              </div>
            </div>

            <!-- License Plate -->
            <p class="text-xs text-gray-500 bg-gray-800/50 rounded px-3 py-2">
              <i class="fas fa-car mr-1"></i>{{ currentLanguage === 'th' ? 'ทะเบียน: ' : 'License: ' }} {{ car.license_plate }}
            </p>

            <!-- Actions -->
            <div class="flex gap-2 pt-2">
              <!-- Edit Button -->
              <NuxtLink
                :to="`/seller/EditCar/${car._id || car.id}`"
                class="flex-1 px-3 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-lg transition-all transform hover:scale-105 duration-300 text-sm font-bold text-center shadow-lg"
              >
                <i class="fas fa-edit mr-1"></i>{{ currentLanguage === 'th' ? 'แก้ไข' : 'Edit' }}
              </NuxtLink>

              <!-- Sold Out / Reactivate Button -->
              <button
                v-if="!car.sold_out"
                @click="markAsSoldOut(car._id)"
                :disabled="loadingStates[car._id]"
                class="flex-1 px-3 py-3 bg-gradient-to-r from-yellow-600 to-yellow-700 hover:from-yellow-700 hover:to-yellow-800 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all transform hover:scale-105 duration-300 text-sm font-bold shadow-lg hover:shadow-yellow-600/50"
              >
                <i v-if="!loadingStates[car._id]" class="fas fa-check mr-1"></i>
                <i v-else class="fas fa-spinner animate-spin mr-1"></i>
                {{ loadingStates[car._id] ? (currentLanguage === 'th' ? 'กำลังประมวลผล...' : 'Processing...') : (currentLanguage === 'th' ? 'ทำเครื่องหมายว่าเป็นขายแล้ว' : 'Mark Sold') }}
              </button>

              <button
                v-else
                @click="markAsActive(car._id)"
                :disabled="loadingStates[car._id]"
                class="flex-1 px-3 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all transform hover:scale-105 duration-300 text-sm font-bold shadow-lg hover:shadow-green-600/50"
              >
                <i v-if="!loadingStates[car._id]" class="fas fa-redo mr-1"></i>
                <i v-else class="fas fa-spinner animate-spin mr-1"></i>
                {{ loadingStates[car._id] ? (currentLanguage === 'th' ? 'กำลังประมวลผล...' : 'Processing...') : (currentLanguage === 'th' ? 'ทำเครื่องหมายว่าเป็นเปิดใช้งาน' : 'Reactivate') }}
              </button>

              <!-- Delete Button -->
              <button
                @click="deleteListing(car._id)"
                :disabled="loadingStates[car._id]"
                class="flex-1 px-3 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-all transform hover:scale-105 duration-300 text-sm font-bold shadow-lg hover:shadow-red-600/50"
              >
                <i v-if="!loadingStates[car._id]" class="fas fa-trash mr-1"></i>
                <i v-else class="fas fa-spinner animate-spin mr-1"></i>
                {{ currentLanguage === 'th' ? 'ลบ' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Confirm Modal -->
  <teleport to="body">
    <transition name="modal-fade">
      <div v-if="showDeleteModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm">
        <div class="bg-gradient-to-br from-gray-900 to-gray-950 rounded-2xl p-8 max-w-sm w-full mx-4 border border-red-500/30 shadow-2xl animate-pop-in">
          <div class="flex items-center gap-3 mb-4">
            <i class="fas fa-exclamation-circle text-3xl text-red-500"></i>
            <h2 class="text-2xl font-bold text-white">{{ currentLanguage === 'th' ? 'ลบรายการ?' : 'Delete Listing?' }}</h2>
          </div>
          <p class="text-gray-300 mb-6">{{ currentLanguage === 'th' ? 'คุณแน่ใจหรือไม่ว่าต้องการลบรายการนี้? การกระทำนี้ไม่สามารถย้อนกลับได้' : 'Are you sure you want to delete this listing? This action cannot be undone.' }}</p>
          <div class="flex gap-3">
            <button
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-all transform hover:scale-105 font-semibold"
            >
              {{ currentLanguage === 'th' ? 'ยกเลิก' : 'Cancel' }}
            </button>
            <button
              @click="confirmDelete"
              :disabled="isDeleting"
              class="flex-1 px-4 py-2 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 disabled:opacity-50 text-white rounded-lg transition-all transform hover:scale-105 font-semibold"
            >
              <i v-if="!isDeleting" class="fas fa-trash mr-1"></i>
              <i v-else class="fas fa-spinner animate-spin mr-1"></i>
              {{ isDeleting ? (currentLanguage === 'th' ? 'กำลังลบ...' : 'Deleting...') : (currentLanguage === 'th' ? 'ลบ' : 'Delete') }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>

  <!-- Success Modal -->
  <SuccessModal
    :show="showSuccessModal"
    :title="successMessage.title"
    :message="successMessage.message"
    icon=""
    :duration="3"
    @close="showSuccessModal = false"
  />
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'
import { useLanguage } from '~/composables/useLanguage'

const router = useRouter()
const { t, currentLanguage } = useLanguage()

const sellerCars = ref([])
const showDeleteModal = ref(false)
const showSuccessModal = ref(false)
const deletingCarId = ref(null)
const successMessage = ref({ title: '', message: '' })
const loadingStates = reactive({})
const isDeleting = ref(false)

const formatPrice = (price) => {
  return new Intl.NumberFormat('th-TH').format(price)
}

onMounted(async () => {
  await fetchSellerCars()
})

const fetchSellerCars = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.log('No token found')
      sellerCars.value = []
      return
    }

    console.log('Fetching seller cars...')
    const response = await fetch('http://localhost:5000/api/cars/my-listings', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()
    console.log('Response:', data)

    if (data.success && Array.isArray(data.cars)) {
      // Sort cars: Active first, then Sold Out
      sellerCars.value = data.cars.sort((a, b) => {
        const aSoldOut = a.sold_out ? 1 : 0
        const bSoldOut = b.sold_out ? 1 : 0
        return aSoldOut - bSoldOut
      })
      console.log('Loaded cars:', sellerCars.value.length)
    } else {
      sellerCars.value = []
    }
  } catch (error) {
    console.error('Error fetching cars:', error)
    sellerCars.value = []
  }
}

const markAsSoldOut = async (carId) => {
  loadingStates[carId] = true
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/cars/${carId}/sold`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sold_out: true })
    })

    const data = await response.json()
    
    if (response.ok && data.success) {
      const car = sellerCars.value.find(c => (c.id || c._id) === carId)
      if (car) {
        car.sold_out = true
        
        // Re-sort the list
        sellerCars.value = sellerCars.value.sort((a, b) => {
          const aSoldOut = a.sold_out ? 1 : 0
          const bSoldOut = b.sold_out ? 1 : 0
          return aSoldOut - bSoldOut
        })
        
        // Show success notification
        successMessage.value = {
          title: ' Marked as Sold Out!',
          message: 'This car status has been updated in database'
        }
        showSuccessModal.value = true
      }
    } else {
      alert('❌ Error: ' + (data.message || 'Failed to update status'))
    }
  } catch (error) {
    console.error('Error marking as sold:', error)
    alert('❌ Error: ' + error.message)
  } finally {
    loadingStates[carId] = false
  }
}

const markAsActive = async (carId) => {
  loadingStates[carId] = true
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/cars/${carId}/sold`, {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sold_out: false })
    })

    const data = await response.json()
    
    if (response.ok && data.success) {
      const car = sellerCars.value.find(c => (c.id || c._id) === carId)
      if (car) {
        car.sold_out = false
        
        // Re-sort the list
        sellerCars.value = sellerCars.value.sort((a, b) => {
          const aSoldOut = a.sold_out ? 1 : 0
          const bSoldOut = b.sold_out ? 1 : 0
          return aSoldOut - bSoldOut
        })
        
        successMessage.value = {
          title: ' Reactivated!',
          message: 'This car has been reactivated for sale'
        }
        showSuccessModal.value = true
      }
    } else {
      alert('❌ Error: ' + (data.message || 'Failed to reactivate'))
    }
  } catch (error) {
    console.error('Error marking as active:', error)
    alert('❌ Error: ' + error.message)
  } finally {
    loadingStates[carId] = false
  }
}

const deleteListing = (carId) => {
  deletingCarId.value = carId
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  isDeleting.value = true
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      alert('❌ No authentication token')
      return
    }

    const response = await fetch(`http://localhost:5000/api/cars/${deletingCarId.value}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    const data = await response.json()

    if (response.ok && data.success) {
      sellerCars.value = sellerCars.value.filter(car => (car.id || car._id) !== deletingCarId.value)
      showDeleteModal.value = false
      deletingCarId.value = null
      
      successMessage.value = {
        title: ' Deleted Successfully!',
        message: 'This listing has been removed from database'
      }
      showSuccessModal.value = true
    } else {
      alert('❌ Error: ' + (data.message || 'Failed to delete'))
    }
  } catch (error) {
    console.error('Error deleting car:', error)
    alert('❌ Error: ' + error.message)
  } finally {
    isDeleting.value = false
  }
}
</script>

<style scoped>
.mylistings-page {
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

.animate-slide-down {
  animation: slideDown 0.6s ease-out both;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out both;
}

.animate-card-appear {
  animation: cardAppear 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  opacity: 0;
}

.animate-bounce-soft {
  animation: bounceSoft 0.8s ease-in-out infinite;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { 
    opacity: 0; 
  }
  to { 
    opacity: 1; 
  }
}

@keyframes cardAppear {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bounceSoft {
  0%, 100% { 
    transform: scale(1);
  }
  50% { 
    transform: scale(1.05);
  }
}

@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.8) rotateZ(-5deg);
  }
  50% {
    transform: scale(1.05) rotateZ(2deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateZ(0);
  }
}

.animate-pop-in {
  animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Modal Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.fade-overlay-enter-active,
.fade-overlay-leave-active {
  transition: opacity 0.5s ease;
}

.fade-overlay-enter-from,
.fade-overlay-leave-to {
  opacity: 0;
}

/* Button Loading State */
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

/* Responsive */
@media (max-width: 768px) {
  .mylistings-page {
    padding: 1rem;
  }
}
</style>
