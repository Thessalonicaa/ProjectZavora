<!-- Enhanced Loading Spinner Component -->
<template>
  <div v-if="show" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center animate-fade-in">
    <div class="bg-gradient-to-br from-gray-900 to-gray-950 rounded-2xl p-8 border border-red-500/30 shadow-2xl text-center space-y-4 animate-scale-in">
      <!-- Animated Spinner -->
      <div class="relative w-16 h-16 mx-auto">
        <div class="absolute inset-0 rounded-full border-4 border-gray-700"></div>
        <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-red-600 border-r-orange-600 animate-rotate-slow"></div>
      </div>

      <!-- Text -->
      <div class="space-y-1">
        <p class="text-white font-bold text-lg">{{ title }}</p>
        <p class="text-gray-400 text-sm">{{ message }}</p>
      </div>

      <!-- Progress Bar -->
      <div v-if="showProgress" class="w-48 h-1 bg-gray-800 rounded-full overflow-hidden">
        <div class="h-full bg-gradient-to-r from-red-600 to-orange-600 animate-shimmer" style="width: 65%"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Loading...'
  },
  message: {
    type: String,
    default: 'Please wait'
  },
  showProgress: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
/* Animations are imported from global animations.css */
</style>