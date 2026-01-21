<template>
  <teleport to="body">
    <transition name="modal-fade">
      <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center bg-gradient-to-br from-black/80 via-black/70 to-green-950/20 backdrop-blur-xl overflow-hidden" @click="handleClose">
        <!-- Animated Background Elements -->
        <div class="absolute inset-0 overflow-hidden pointer-events-none">
          <div class="absolute -top-1/2 -left-1/2 w-96 h-96 bg-green-600/10 rounded-full blur-3xl animate-pulse"></div>
          <div class="absolute -bottom-1/2 -right-1/2 w-96 h-96 bg-green-600/10 rounded-full blur-3xl animate-pulse" style="animation-delay: 0.5s;"></div>
        </div>

        <!-- Modal Content -->
        <div 
          class="relative bg-gradient-to-br from-gray-900/90 via-gray-900/90 to-gray-950/90 backdrop-blur-xl rounded-3xl p-10 max-w-md w-full mx-4 animate-pop-in border border-green-500/30 shadow-2xl"
          @click.stop
        >
          <!-- Success Icon with Animation -->
          <div class="flex justify-center mb-8">
            <div class="relative">
              <div class="absolute inset-0 bg-gradient-to-r from-green-600/20 to-emerald-600/20 rounded-full blur-2xl"></div>
              <div class="relative animate-success-icon text-7xl drop-shadow-lg">
                <svg class="w-20 h-20 mx-auto text-green-500 animate-check-pop" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <!-- Confetti Animation -->
              <div class="absolute -top-2 -left-2 w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 0s;"></div>
              <div class="absolute -top-4 right-0 w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 0.2s;"></div>
              <div class="absolute -bottom-2 right-4 w-2 h-2 bg-green-600 rounded-full animate-bounce" style="animation-delay: 0.4s;"></div>
            </div>
          </div>

          <!-- Title -->
          <h2 class="text-3xl font-extrabold text-white text-center mb-3 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent drop-shadow-lg">
            {{ title }}
          </h2>

          <!-- Message -->
          <p class="text-gray-300 text-center mb-8 leading-relaxed font-medium text-base">
            {{ message }}
          </p>

          <!-- Progress Bar -->
          <div class="w-full bg-gray-800/50 rounded-full h-2 overflow-hidden mb-4 border border-gray-700/50">
            <div 
              class="bg-gradient-to-r from-green-500 to-emerald-500 h-full animate-countdown rounded-full shadow-lg shadow-green-500/50"
              :style="{ '--countdown-duration': `${duration}s` }"
            ></div>
          </div>

          <!-- Auto close text -->
          <p class="text-gray-400 text-sm text-center font-semibold mb-8">
            <i class="fas fa-hourglass-end text-green-500 mr-2"></i>
            Auto closing in <span class="text-green-400 font-bold">{{ remainingTime }}</span>s
          </p>

          <!-- Click anywhere to close hint -->
          <p class="text-gray-500 text-xs text-center">
            <i class="fas fa-mouse text-gray-600 mr-1"></i>Click anywhere to continue
          </p>

          <!-- Decorative Elements -->
          <div class="mt-8 flex items-center justify-center gap-3 opacity-50">
            <div class="w-8 h-0.5 bg-gradient-to-r from-transparent to-green-500 rounded"></div>
            <i class="fas fa-star text-green-500 text-xs"></i>
            <div class="w-8 h-0.5 bg-gradient-to-l from-transparent to-green-500 rounded"></div>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  show: Boolean,
  title: String,
  message: String,
  icon: {
    type: String,
    default: ''
  },
  duration: {
    type: Number,
    default: 5
  }
})

const emit = defineEmits(['close'])
const remainingTime = ref(props.duration)

watch(() => props.show, (newVal) => {
  if (newVal) {
    remainingTime.value = props.duration
    const interval = setInterval(() => {
      remainingTime.value--
      if (remainingTime.value <= 0) {
        clearInterval(interval)
        emit('close')
      }
    }, 1000)
  }
})

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
/* Pop In Animation */
@keyframes popIn {
  0% {
    opacity: 0;
    transform: scale(0.5) translateY(-50px);
  }
  50% {
    transform: scale(1.08);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

/* Success Icon Animation */
@keyframes successIcon {
  0% {
    transform: scale(0) rotate(-45deg);
  }
  50% {
    transform: scale(1.25) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }
}

/* Check Pop Animation - SVG Checkmark */
@keyframes checkPop {
  from {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

/* Countdown Animation */
@keyframes countdown {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

/* Bounce Animation */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    opacity: 1;
  }
  50% {
    transform: translateY(-15px);
    opacity: 0.5;
  }
}

/* Pulse Animation */
@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
}

/* Animation Classes */
.animate-pop-in {
  animation: popIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-success-icon {
  animation: successIcon 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-check-pop {
  animation: checkPop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.2s both;
}

.animate-countdown {
  animation: countdown var(--countdown-duration, 5s) linear forwards;
}

.animate-bounce {
  animation: bounce 1.4s ease-in-out infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Modal Fade Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-fade-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.modal-fade-leave-to {
  opacity: 0;
  transform: scale(1.1);
}
</style>
