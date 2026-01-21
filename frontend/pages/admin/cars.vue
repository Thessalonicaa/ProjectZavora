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

    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent">
            <i class="fas fa-car mr-3"></i>Car Listings Management
          </h1>
          <p class="text-gray-400 mt-2">View, edit, and manage car listings from MongoDB</p>
        </div>
        <NuxtLink to="/admin" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all flex items-center gap-2">
          <i class="fas fa-arrow-left"></i>Back to Dashboard
        </NuxtLink>
      </div>

      <div v-if="!isAdmin" class="text-center py-20">
        <p class="text-gray-400">Unauthorized</p>
        <NuxtLink to="/" class="text-red-400 mt-4 inline-block">Go Home</NuxtLink>
      </div>

      <div v-else>
        <!-- Search Bar -->
        <div class="mb-6 flex gap-4">
          <input 
            v-model="filter" 
            placeholder="Search by brand, model, or license plate..." 
            class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-red-500 focus:outline-none transition-all"
          />
          <button @click="fetchAll" class="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg transition-all flex items-center gap-2 font-semibold">
            <i class="fas fa-sync"></i>Refresh
          </button>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-4 gap-4 mb-6">
          <div class="bg-gradient-to-br from-blue-600/20 to-blue-700/20 border border-blue-500/30 rounded-xl p-4">
            <p class="text-gray-400 text-sm font-semibold">Total Cars</p>
            <p class="text-3xl font-bold text-blue-400">{{ cars.length }}</p>
          </div>
          <div class="bg-gradient-to-br from-green-600/20 to-green-700/20 border border-green-500/30 rounded-xl p-4">
            <p class="text-gray-400 text-sm font-semibold">Available</p>
            <p class="text-3xl font-bold text-green-400">{{ availableCars }}</p>
          </div>
          <div class="bg-gradient-to-br from-red-600/20 to-red-700/20 border border-red-500/30 rounded-xl p-4">
            <p class="text-gray-400 text-sm font-semibold">Sold Out</p>
            <p class="text-3xl font-bold text-red-400">{{ soldOutCars }}</p>
          </div>
          <div class="bg-gradient-to-br from-orange-600/20 to-orange-700/20 border border-orange-500/30 rounded-xl p-4">
            <p class="text-gray-400 text-sm font-semibold">Total Value</p>
            <p class="text-3xl font-bold text-orange-400">฿{{ formatPrice(totalValue) }}</p>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-16">
          <div class="inline-flex flex-col items-center">
            <div class="w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-gray-400 text-lg">Loading cars from database...</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="cars.length === 0" class="text-center py-16">
          <i class="fas fa-inbox text-6xl text-gray-600 mb-4"></i>
          <p class="text-gray-400 text-xl">No cars found in database</p>
        </div>

        <!-- Table -->
        <div v-else class="overflow-x-auto bg-gray-900/50 rounded-2xl border border-gray-700 shadow-xl">
          <table class="min-w-full text-left text-sm">
            <thead class="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700 sticky top-0">
              <tr>
                <th class="px-6 py-4 font-semibold text-gray-300">Brand/Model</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Year</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Price</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Fuel/Trans</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Engine/Mileage</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Type/Color</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Seller</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Views</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Status</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in filtered" :key="c._id" class="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                <td class="px-6 py-4 font-semibold text-white">
                  <div class="font-bold">{{ c.brand }} {{ c.model }}</div>
                  <div class="text-xs text-gray-400">{{ c.license_plate || '-' }}</div>
                </td>
                <td class="px-6 py-4 text-gray-300">{{ c.year || '-' }}</td>
                <td class="px-6 py-4 text-red-400 font-bold">฿{{ formatPrice(c.price) }}</td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-300">{{ c.fuel_type || '-' }}</div>
                  <div class="text-xs text-gray-400">{{ c.transmission || '-' }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-300">{{ c.engine_size ? c.engine_size + ' cc' : '-' }}</div>
                  <div class="text-xs text-gray-400">{{ c.mileage ? formatPrice(c.mileage) + ' km' : '-' }}</div>
                </td>
                <td class="px-6 py-4">
                  <div class="text-xs text-gray-300">{{ c.car_type || '-' }}</div>
                  <div class="text-xs text-gray-400">{{ c.color || '-' }}</div>
                </td>
                <td class="px-6 py-4 text-sm">
                  <div class="text-gray-300 font-semibold">{{ c.seller?.username || '-' }}</div>
                  <div class="text-xs text-gray-500">{{ c.seller?.business_name || '-' }}</div>
                </td>
                <td class="px-6 py-4">
                  <span class="inline-flex items-center gap-1 px-2 py-1 bg-blue-600/30 text-blue-300 rounded text-xs font-semibold">
                    <i class="fas fa-eye"></i>{{ c.views || 0 }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs font-bold inline-flex items-center gap-1',
                    c.sold_out || c.sold ? 'bg-red-600/30 text-red-300' : 'bg-green-600/30 text-green-300'
                  ]">
                    <i :class="c.sold_out || c.sold ? 'fas fa-times-circle' : 'fas fa-check-circle'"></i>
                    {{ c.sold_out || c.sold ? 'Sold Out' : 'Available' }}
                  </span>
                </td>
                <td class="px-6 py-4 flex gap-2">
                  <button @click="openEdit(c)" class="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1" title="Edit car">
                    <i class="fas fa-edit"></i>Edit
                  </button>
                  <button @click="confirmDelete(c)" class="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1" title="Delete car">
                    <i class="fas fa-trash"></i>Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ✅ Toast Notification - Top Center -->
    <transition
      enter-active-class="animate-slide-down"
      leave-active-class="animate-slide-up"
    >
      <div v-if="showNotification" :class="[
        'fixed top-6 left-1/2 transform -translate-x-1/2 z-[9999] px-8 py-4 rounded-2xl border shadow-2xl flex items-center gap-3',
        notificationType === 'success' ? 'bg-gradient-to-r from-green-600 to-green-700 border-green-500/50' :
        notificationType === 'error' ? 'bg-gradient-to-r from-red-600 to-red-700 border-red-500/50' :
        'bg-gradient-to-r from-blue-600 to-blue-700 border-blue-500/50'
      ]">
        <i :class="[
          'text-2xl',
          notificationType === 'success' ? 'fas fa-check-circle text-green-200' :
          notificationType === 'error' ? 'fas fa-times-circle text-red-200' :
          'fas fa-info-circle text-blue-200'
        ]"></i>
        <span class="text-white font-semibold text-lg">{{ notificationMessage }}</span>
      </div>
    </transition>

    <!-- Edit Modal -->
    <div v-if="editing" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-2xl border border-gray-700 shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6 sticky top-0">
          <h3 class="text-2xl font-bold text-white">Edit Car Listing</h3>
          <button @click="closeEdit" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Brand</label>
              <input v-model="editForm.brand" placeholder="Brand" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Model</label>
              <input v-model="editForm.model" placeholder="Model" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Year</label>
              <input v-model.number="editForm.year" type="number" placeholder="Year" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Price (฿)</label>
              <input v-model.number="editForm.price" type="number" placeholder="Price" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Fuel Type</label>
              <select v-model="editForm.fuel_type" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option value="">Select Fuel Type</option>
                <option value="Petrol">Petrol</option>
                <option value="Diesel">Diesel</option>
                <option value="Hybrid">Hybrid</option>
                <option value="Electric">Electric</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Transmission</label>
              <select v-model="editForm.transmission" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option value="">Select Transmission</option>
                <option value="Automatic">Automatic</option>
                <option value="Manual">Manual</option>
                <option value="CVT">CVT</option>
                <option value="DCT">DCT</option>
                <option value="e-CVT">e-CVT</option>
                <option value="Semi-Automatic">Semi-Automatic</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Engine Size (cc)</label>
              <input v-model.number="editForm.engine_size" type="number" placeholder="Engine Size" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Mileage (km)</label>
              <input v-model.number="editForm.mileage" type="number" placeholder="Mileage" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Color</label>
              <input v-model="editForm.color" placeholder="Color" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Car Type</label>
              <select v-model="editForm.car_type" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option value="">Select Car Type</option>
                <option value="Sedan">Sedan</option>
                <option value="SUV">SUV</option>
                <option value="Pickup">Pickup</option>
                <option value="Van">Van</option>
                <option value="Coupe">Coupe</option>
                <option value="Hatchback">Hatchback</option>
                <option value="MPV">MPV</option>
                <option value="Convertible">Convertible</option>
                <option value="Sports">Sports</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Drive System</label>
              <select v-model="editForm.drive_system" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option value="">Select Drive System</option>
                <option value="FWD">FWD (Front-Wheel)</option>
                <option value="RWD">RWD (Rear-Wheel)</option>
                <option value="AWD">AWD (All-Wheel)</option>
                <option value="4WD">4WD (Four-Wheel)</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Gas System</label>
              <select v-model="editForm.gas_system" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option value="">None</option>
                <option value="NGV">NGV</option>
                <option value="LPG">LPG</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Description</label>
            <textarea v-model="editForm.description" placeholder="Description" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" rows="3"></textarea>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">License Plate</label>
              <input v-model="editForm.license_plate" placeholder="License Plate" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-300 mb-2">Status</label>
              <select v-model="editForm.sold_out" class="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all">
                <option :value="false">Available</option>
                <option :value="true">Sold Out</option>
              </select>
            </div>
          </div>
        </div>

        <div class="mt-6 flex gap-3">
          <button @click="saveEdit" class="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg text-white font-bold transition-all transform hover:scale-105 flex items-center justify-center gap-2">
            <i class="fas fa-save"></i>Save Changes
          </button>
          <button @click="closeEdit" class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-red-500/50 shadow-2xl animate-scale-in">
        <div class="flex items-center justify-center w-12 h-12 rounded-full bg-red-600/20 mx-auto mb-4">
          <i class="fas fa-exclamation text-2xl text-red-500"></i>
        </div>
        
        <h3 class="text-2xl font-bold text-white text-center mb-2">Delete Car Listing?</h3>
        <p class="text-gray-400 text-center mb-6">
          Are you sure you want to delete <span class="font-semibold text-white">{{ deleteTarget?.brand }} {{ deleteTarget?.model }}</span>? This action cannot be undone.
        </p>

        <div class="flex gap-3">
          <button @click="performDelete" class="flex-1 px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 rounded-lg text-white font-bold transition-all transform hover:scale-105">
            Yes, Delete
          </button>
          <button @click="closeDeleteConfirm" class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const isAdmin = ref(false)
const cars = ref([])
const filter = ref('')
const loading = ref(false)
const editing = ref(false)
const editForm = ref({})
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)
const showNotification = ref(false)
const notificationMessage = ref('')
const notificationType = ref('success')

const fetchAll = async () => {
  loading.value = true
  try {
    console.log('Fetching cars from API...')
    const token = localStorage.getItem('token')
    
    const res = await fetch('http://localhost:5000/api/cars', {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
    const data = await res.json()
    console.log('API Response:', data)
    
    if (data.success && data.cars) {
      cars.value = data.cars
      console.log('✅ Loaded', cars.value.length, 'cars')
    } else {
      console.error('❌ API returned:', data)
      cars.value = []
    }
  } catch (e) { 
    console.error('❌ Error fetching cars:', e)
    cars.value = []
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  if (!filter.value) return cars.value
  const q = filter.value.toLowerCase()
  return cars.value.filter(c => 
    (c.brand || '').toLowerCase().includes(q) || 
    (c.model || '').toLowerCase().includes(q) || 
    (c.license_plate || '').toLowerCase().includes(q)
  )
})

const availableCars = computed(() => cars.value.filter(c => !c.sold_out && !c.sold).length)
const soldOutCars = computed(() => cars.value.filter(c => c.sold_out || c.sold).length)
const totalValue = computed(() => cars.value.reduce((sum, c) => sum + (c.price || 0), 0))

const formatPrice = (p) => p?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') || 0

// ✅ Notification function
const showToast = (message, type = 'success') => {
  notificationMessage.value = message
  notificationType.value = type
  showNotification.value = true
  
  // Auto hide after 4 seconds
  setTimeout(() => {
    showNotification.value = false
  }, 4000)
}

const openEdit = (c) => { editForm.value = { ...c }; editing.value = true }
const closeEdit = () => { editing.value = false; editForm.value = {} }

const saveEdit = async () => {
  try {
    // ✅ Get JWT token from localStorage
    const token = localStorage.getItem('token')
    if (!token) {
      showToast('Not authenticated. Please login again.', 'error')
      return
    }

    const url = `http://localhost:5000/api/cars/${editForm.value._id}`
    console.log('Saving car to:', url)
    console.log('Token present:', !!token)
    
    const res = await fetch(url, { 
      method: 'PUT', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }, 
      body: JSON.stringify(editForm.value) 
    })
    
    const data = await res.json()
    console.log('Response:', res.status, data)
    
    if (data.success || res.status === 200) { 
      fetchAll()
      closeEdit()
      showToast('✅ Car updated successfully!', 'success')
    } else {
      showToast('Error: ' + (data.message || data.error || 'Failed to update'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showToast('Error: ' + e.message, 'error')
  }
}

const confirmDelete = (c) => { deleteTarget.value = c; showDeleteConfirm.value = true }
const closeDeleteConfirm = () => { showDeleteConfirm.value = false; deleteTarget.value = null }

const performDelete = async () => {
  try {
    // ✅ Get JWT token from localStorage
    const token = localStorage.getItem('token')
    if (!token) {
      showToast('Not authenticated. Please login again.', 'error')
      return
    }

    const url = `http://localhost:5000/api/cars/${deleteTarget.value._id}`
    console.log('Deleting car from:', url)
    console.log('Token present:', !!token)
    
    const res = await fetch(url, { 
      method: 'DELETE',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await res.json()
    console.log('Response:', res.status, data)
    
    if (data.success || res.status === 200) { 
      fetchAll()
      closeDeleteConfirm()
      showToast('✅ Car deleted successfully!', 'success')
    } else {
      showToast('Error: ' + (data.message || data.error || 'Failed to delete'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showToast('Error: ' + e.message, 'error')
  }
}

onMounted(() => {
  if (process.client) {
    const role = localStorage.getItem('role')
    const isAdmin_value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    isAdmin.value = isAdmin_value
    console.log('Admin status:', isAdmin_value)
    
    if (!isAdmin_value) {
      console.log('Not admin, returning')
      return
    }
    
    console.log('Fetching cars on mount...')
    fetchAll()
  }
})
</script>

<style scoped>
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-scale-in { animation: scaleIn 0.3s ease-out; }

.beams-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

/* ✅ Toast Animations - Top Center */
@keyframes slideDown {
  from { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
  to { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
}

@keyframes slideUp {
  from { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
  to { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
}

.animate-slide-down { animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.animate-slide-up { animation: slideUp 0.3s ease-in; }
</style>