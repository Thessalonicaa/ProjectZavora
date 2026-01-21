<template>
  <transition name="notice-fade">
    <div 
      class="fixed inset-0 bg-gradient-to-br from-black/90 via-black/80 to-red-950/40 backdrop-blur-xl flex items-center justify-center z-50 overflow-hidden"
      @click="handleClick"
    >
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-1/2 -left-1/2 w-96 h-96 bg-red-600/10 rounded-full blur-3xl animate-float"></div>
        <div class="absolute -bottom-1/2 -right-1/2 w-96 h-96 bg-red-600/10 rounded-full blur-3xl animate-float-reverse"></div>
      </div>

      <!-- Content -->
      <div class="relative z-10 text-center p-8 md:p-12 transform transition-all duration-500 scale-100 max-w-md md:max-w-lg">
        <!-- Icon Container -->
        <div class="relative mb-8">
          <div class="absolute inset-0 bg-gradient-to-r from-red-600/20 to-orange-600/20 rounded-full blur-2xl"></div>
          <div class="relative flex items-center justify-center">
            <div class="text-red-500 text-8xl animate-icon-bounce drop-shadow-lg">
              <i class="fas fa-exclamation-circle"></i>
            </div>
            <!-- Floating Particles -->
            <div class="absolute w-2 h-2 bg-red-500 rounded-full animate-pulse" style="top: -20px; left: 10px;"></div>
            <div class="absolute w-1.5 h-1.5 bg-orange-500 rounded-full animate-pulse" style="top: 10px; right: -20px; animation-delay: 0.5s;"></div>
            <div class="absolute w-2 h-2 bg-red-500 rounded-full animate-pulse" style="bottom: -20px; right: 10px; animation-delay: 1s;"></div>
          </div>
        </div>

        <!-- Title -->
        <h2 class="text-white text-3xl md:text-4xl font-extrabold mb-4 bg-gradient-to-r from-red-500 to-orange-500 bg-clip-text text-transparent drop-shadow-lg">
          {{ title }}
        </h2>

        <!-- Message -->
        <p class="text-gray-300 text-base md:text-lg mb-8 leading-relaxed font-medium">
          {{ message }}
        </p>

        <!-- Action Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
          <button
            @click.stop="handleClick"
            class="px-8 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold rounded-xl transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg hover:shadow-red-600/50 flex items-center gap-2"
          >
            <i class="fas fa-arrow-left"></i>
            Go Back
          </button>
          <button
            @click.stop="goToDashboard"
            class="px-8 py-3 bg-gradient-to-r from-gray-700 to-gray-800 hover:from-gray-600 hover:to-gray-700 text-white font-bold rounded-xl transition-all duration-300 transform hover:scale-105 active:scale-95 shadow-lg border border-gray-600"
          >
            <i class="fas fa-home mr-2"></i>Dashboard
          </button>
        </div>

        <!-- Click Hint -->
        <div class="flex items-center justify-center gap-2 text-gray-400 text-sm">
          <i class="fas fa-mouse"></i>
          <p class="animate-pulse">Click anywhere or use buttons above</p>
        </div>

        <!-- Decorative Line -->
        <div class="mt-8 flex items-center gap-3 justify-center opacity-50">
          <div class="w-12 h-0.5 bg-gradient-to-r from-transparent to-red-500 rounded"></div>
          <i class="fas fa-circle text-red-500 text-xs"></i>
          <div class="w-12 h-0.5 bg-gradient-to-l from-transparent to-red-500 rounded"></div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  title: {
    type: String,
    default: 'Access Denied'
  },
  message: {
    type: String,
    default: 'You do not have permission to access this page. Please register as a seller first.'
  },
  redirectTo: {
    type: String,
    default: '/dashboard'
  }
})

const router = useRouter()

const handleClick = () => {
  router.push(props.redirectTo)
}

const goToDashboard = () => {
  router.push('/dashboard')
}
</script>

<style scoped>
/* Animations */
@keyframes iconBounce {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.05);
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(20px, -20px) rotate(90deg);
  }
  50% {
    transform: translate(0, -40px) rotate(180deg);
  }
  75% {
    transform: translate(-20px, -20px) rotate(270deg);
  }
}

@keyframes floatReverse {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(-20px, 20px) rotate(-90deg);
  }
  50% {
    transform: translate(0, 40px) rotate(-180deg);
  }
  75% {
    transform: translate(20px, 20px) rotate(-270deg);
  }
}

.animate-icon-bounce {
  animation: iconBounce 3s ease-in-out infinite;
}

.animate-float {
  animation: float 20s ease-in-out infinite;
}

.animate-float-reverse {
  animation: floatReverse 25s ease-in-out infinite;
}

/* Transition */
.notice-fade-enter-active,
.notice-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.notice-fade-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.notice-fade-leave-to {
  opacity: 0;
  transform: scale(1.1);
}

/* Pulse Animation */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>