<template>
  <div class="admin-index-page min-h-screen bg-gray-950 text-white p-8 relative overflow-hidden">
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
      <div class="text-center mb-12 animate-slide-down">
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent mb-2">
          <i class="fas fa-shield-alt mr-3"></i>Admin Dashboard
        </h1>
        <p class="text-gray-400 text-lg">Manage users, sellers, and car listings</p>
      </div>

      <div v-if="!isAdmin" class="text-center py-20">
        <div class="inline-block">
          <i class="fas fa-lock text-6xl text-red-500 mb-4"></i>
          <p class="text-gray-400 text-xl">You are not authorized to view this page.</p>
          <NuxtLink to="/" class="inline-block mt-6 px-6 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all">
            Go Home
          </NuxtLink>
        </div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Data Users Card -->
        <NuxtLink 
          to="/admin/users" 
          class="group relative bg-gradient-to-br from-blue-600/20 to-blue-800/10 border border-blue-500/30 hover:border-blue-500/60 rounded-3xl p-8 transition-all transform hover:scale-105 duration-300 shadow-xl hover:shadow-2xl hover:shadow-blue-500/30 overflow-hidden cursor-pointer"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-blue-600/0 to-blue-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="text-5xl text-blue-500 mb-4">
              <i class="fas fa-users"></i>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">Data Users</h2>
            <p class="text-gray-400">View and manage user and seller accounts</p>
            <div class="mt-4 flex items-center text-blue-400 group-hover:translate-x-2 transition-transform">
              <span>Manage Users</span>
              <i class="fas fa-arrow-right ml-2"></i>
            </div>
          </div>
        </NuxtLink>

        <!-- Data Cars Card -->
        <NuxtLink 
          to="/admin/cars" 
          class="group relative bg-gradient-to-br from-red-600/20 to-red-800/10 border border-red-500/30 hover:border-red-500/60 rounded-3xl p-8 transition-all transform hover:scale-105 duration-300 shadow-xl hover:shadow-2xl hover:shadow-red-500/30 overflow-hidden cursor-pointer"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative z-10">
            <div class="text-5xl text-red-500 mb-4">
              <i class="fas fa-car"></i>
            </div>
            <h2 class="text-2xl font-bold text-white mb-2">Data Cars</h2>
            <p class="text-gray-400">View and manage car listings</p>
            <div class="mt-4 flex items-center text-red-400 group-hover:translate-x-2 transition-transform">
              <span>Manage Cars</span>
              <i class="fas fa-arrow-right ml-2"></i>
            </div>
          </div>
        </NuxtLink>
      </div>

      <!-- Stats Section -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Total Users</p>
          <p class="text-4xl font-bold text-blue-400">{{ stats.users }}</p>
        </div>
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Total Cars</p>
          <p class="text-4xl font-bold text-red-400">{{ stats.cars }}</p>
        </div>
        <div class="bg-gray-800/50 border border-gray-700 rounded-2xl p-6">
          <p class="text-gray-400 text-sm uppercase font-semibold mb-2">Time</p>
          <p class="text-lg font-bold text-green-400">{{ lastUpdate }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Beams from '~/components/Beams.vue'

const isAdmin = ref(false)
const stats = ref({ users: 0, cars: 0 })
const lastUpdate = ref('just now')

const fetchStats = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found')
      return
    }

    console.log('Fetching stats from MongoDB...')

    // ✅ Fetch users with token
    const usersRes = await fetch('http://localhost:5000/api/admin/users', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    // ✅ Fetch cars with token
    const carsRes = await fetch('http://localhost:5000/api/cars', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    const usersData = await usersRes.json()
    const carsData = await carsRes.json()
    
    console.log('Users Response:', usersData)
    console.log('Cars Response:', carsData)
    
    // ✅ Update stats
    if (usersData.success && usersData.users) {
      stats.value.users = usersData.users.length
      console.log('✅ Loaded users:', stats.value.users)
    } else {
      console.error('❌ Failed to load users:', usersData)
    }
    
    if (carsData.success && carsData.cars) {
      stats.value.cars = carsData.cars.length
      console.log('✅ Loaded cars:', stats.value.cars)
    } else {
      console.error('❌ Failed to load cars:', carsData)
    }
    
    lastUpdate.value = new Date().toLocaleTimeString('th-TH')
  } catch (e) { 
    console.error('❌ Error fetching stats:', e)
  }
}

onMounted(() => {
  if (process.client) {
    const role = localStorage.getItem('role')
    isAdmin.value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    if (isAdmin.value) fetchStats()
  }
})
</script>

<style scoped>
.admin-index-page {
  position: relative;
}

.beams-background {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 0;
  opacity: 0.25;
  pointer-events: none;
}

.animate-slide-down {
  animation: slideDown 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-30px); }
  to { opacity: 1; transform: translateY(0); }
}

.grid > * {
  animation: fadeIn 0.8s ease-out both;
}

.grid > *:nth-child(2) { animation-delay: 0.2s; }
.grid > *:nth-child(3) { animation-delay: 0.4s; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>