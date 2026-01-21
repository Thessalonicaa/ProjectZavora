// filepath: e:\ProjectFainal\frontend\components\ProfileCard.vue
<template>
  <div class="bg-gray-800/50 p-6 rounded-xl border border-gray-700 hover:border-red-500 transition-all transform hover:-translate-y-1 duration-300 animate-slide-down-slow">
    <div class="flex items-center gap-4">
      <!-- Profile Image -->
      <div class="relative">
        <div 
          v-if="profileImage"
          class="w-16 h-16 rounded-full bg-red-500 overflow-hidden"
        >
          <img 
            :src="profileImage" 
            :alt="username"
            class="w-full h-full object-cover"
          />
        </div>
        <div 
          v-else
          class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center"
        >
          <i class="fas fa-user text-white text-2xl"></i>
        </div>
        <!-- Badge -->
        <div 
          v-if="badge"
          class="absolute -bottom-1 -right-1 bg-green-500 rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold text-white"
        >
          <i :class="badge === 'seller' ? 'fas fa-store' : 'fas fa-user-check'"></i>
        </div>
      </div>

      <!-- Info -->
      <div class="flex-1">
        <p class="text-gray-400 text-sm">{{ type }}</p>
        <h3 class="text-white font-bold text-lg">{{ username }}</h3>
        <p v-if="businessName" class="text-red-500 text-sm">{{ businessName }}</p>
      </div>

      <!-- View Profile Button -->
      <button
        @click="goToProfile"
        class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors text-sm font-semibold whitespace-nowrap"
      >
        <i class="fas fa-arrow-right mr-1"></i>View
      </button>
    </div>

    <!-- Additional Info -->
    <div v-if="showDetails" class="mt-4 pt-4 border-t border-gray-700 space-y-2 text-sm">
      <div v-if="email" class="flex items-center text-gray-300">
        <i class="fas fa-envelope text-red-500 mr-2 w-4"></i>
        <span>{{ email }}</span>
      </div>
      <div v-if="phone" class="flex items-center text-gray-300">
        <i class="fas fa-phone text-red-500 mr-2 w-4"></i>
        <span>{{ phone }}</span>
      </div>
      <div v-if="address" class="flex items-center text-gray-300">
        <i class="fas fa-map-marker-alt text-red-500 mr-2 w-4"></i>
        <span>{{ address }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  username: {
    type: String,
    required: true
  },
  type: {
    type: String,
    enum: ['Seller', 'Buyer'],
    default: 'Seller'
  },
  profileImage: {
    type: String,
    default: ''
  },
  businessName: {
    type: String,
    default: ''
  },
  email: {
    type: String,
    default: ''
  },
  phone: {
    type: String,
    default: ''
  },
  address: {
    type: String,
    default: ''
  },
  badge: {
    type: String,
    enum: ['seller', 'buyer', null],
    default: 'seller'
  },
  showDetails: {
    type: Boolean,
    default: true
  }
})

const goToProfile = () => {
  router.push(`/profile?user=${props.username}`)
}
</script>

<style scoped>
/* Smooth transitions */
.animate-slide-down-slow {
  animation: slideDownSlow 5s ease-out;
}

@keyframes slideDownSlow {
  0% {
    opacity: 0;
    transform: translateY(-40px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
