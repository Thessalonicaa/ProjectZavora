<template>
  <div class="relative inline-block w-full group">
    <!-- Trigger Content -->
    <slot />

    <!-- Hover Card - Positioned on the right, outside the container -->
    <div
      class="absolute -right-96 top-0 w-80 bg-gray-900/95 backdrop-blur-xl rounded-2xl border border-gray-700/50 shadow-2xl shadow-red-600/20 p-6 z-50 invisible opacity-0 group-hover:visible group-hover:opacity-100 transition-all duration-300 pointer-events-none group-hover:pointer-events-auto"
    >
      <!-- Close Button -->
      <button
        class="absolute top-3 right-3 text-gray-400 hover:text-white transition"
      >
        <i class="fas fa-times"></i>
      </button>

      <!-- Profile Header -->
      <div class="flex flex-col items-center text-center mb-4">
        <img
          v-if="profileImage"
          :src="profileImage"
          :alt="username"
          class="w-20 h-20 rounded-full border-3 border-red-500 mb-3 object-cover"
        />
        <div v-else class="w-20 h-20 rounded-full bg-gradient-to-br from-red-600 to-red-700 flex items-center justify-center border-3 border-red-500 mb-3">
          <i class="fas fa-store text-white text-3xl"></i>
        </div>

        <h3 class="text-lg font-bold text-white mb-1">{{ businessName }}</h3>
        <p class="text-red-500 text-sm font-semibold mb-2">@{{ username }}</p>
        <p class="text-xs text-gray-400">{{ lastActivity }}</p>
      </div>

      <!-- Divider -->
      <div class="h-px bg-gradient-to-r from-transparent via-red-500 to-transparent mb-4"></div>

      <!-- Info Section -->
      <div class="space-y-3 mb-4">
        <div class="flex items-center gap-2">
          <i class="fas fa-envelope text-red-500 w-5"></i>
          <div class="min-w-0 flex-1">
            <p class="text-xs text-gray-400">Email</p>
            <p class="text-sm text-white truncate">{{ email }}</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <i class="fas fa-phone text-red-500 w-5"></i>
          <div class="min-w-0 flex-1">
            <p class="text-xs text-gray-400">Phone</p>
            <p class="text-sm text-white font-medium">{{ phoneNumber }}</p>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <i class="fas fa-car text-red-500 w-5"></i>
          <div class="min-w-0 flex-1">
            <p class="text-xs text-gray-400">Cars Listed</p>
            <p class="text-sm text-white font-medium">{{ carsListed }} available</p>
          </div>
        </div>
      </div>

      <!-- Visit Profile Button -->
      <NuxtLink
        :to="`/profile?user=${username}`"
        class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold py-2 px-4 rounded-lg transition-all transform hover:scale-105 text-center block"
      >
        Visit Profile
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
defineProps({
  username: String,
  businessName: String,
  phoneNumber: String,
  email: String,
  profileImage: String,
  lastActivity: String,
  carsListed: Number
})
</script>

<style scoped>
/* Ensure overflow is visible for the hover card */
div {
  overflow: visible !important;
}
</style>
