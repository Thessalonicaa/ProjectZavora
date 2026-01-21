<template>
  <div v-if="isLoading" class="fixed inset-0 flex items-center justify-center bg-gray-950/80 backdrop-blur-sm z-50">
    <div class="flex flex-col items-center gap-4">
      <!-- Spinner -->
      <div class="relative w-16 h-16">
        <div class="absolute inset-0 rounded-full border-4 border-gray-700"></div>
        <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-red-500 border-r-red-500 animate-spin"></div>
      </div>
      
      <!-- Text -->
      <div class="text-center">
        <p class="text-white font-semibold text-lg">{{ loadingText }}</p>
        <p class="text-gray-400 text-sm mt-2">Please wait...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isLoading: {
    type: Boolean,
    default: true
  },
  loadingText: {
    type: String,
    default: 'Loading...'
  }
})
</script>

<style scoped>
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