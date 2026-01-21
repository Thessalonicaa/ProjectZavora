<!-- filepath: e:\ProjectFainal\frontend\components\SuccessRegistrationModal.vue -->
<template>
  <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm" @click="handleClose">
    <div
      @click.stop
      class="success-modal bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8 rounded-2xl text-center max-w-md w-full mx-4 border border-orange-500/30 shadow-2xl"
    >
      <div class="success-icon mb-4">
        <svg class="w-20 h-20 mx-auto text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h3 class="text-white text-2xl font-bold mb-2">
        {{ title }}
      </h3>
      <p class="text-gray-300 mb-4">
        System will redirect in <span class="text-orange-500 font-bold text-xl">{{ countdown }}</span> seconds
      </p>
      <div class="countdown-bar">
        <div class="countdown-progress" :style="{ width: `${(countdown / 5) * 100}%` }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Registration Successful'
  },
  duration: {
    type: Number,
    default: 5000
  }
})

const emit = defineEmits(['close', 'redirect'])

const countdown = ref(5)
let countdownInterval = null

watch(() => props.show, (newVal) => {
  if (newVal) {
    countdown.value = 5
    countdownInterval = setInterval(() => {
      countdown.value = Math.max(0, countdown.value - 1)
      
      if (countdown.value === 0) {
        clearInterval(countdownInterval)
        emit('redirect')
      }
    }, 1000)
  } else {
    clearInterval(countdownInterval)
  }
})

const handleClose = () => {
  clearInterval(countdownInterval)
  emit('close')
  emit('redirect')
}

onBeforeUnmount(() => {
  clearInterval(countdownInterval)
})
</script>

<style scoped>
.success-modal {
  animation: modalPop 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.success-icon svg {
  animation: checkPop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) 0.2s both;
}

.countdown-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 1rem;
}

.countdown-progress {
  height: 100%;
  background: linear-gradient(90deg, #ff3c03, #ff8c00);
  border-radius: 3px;
  transition: width 1s linear;
  box-shadow: 0 0 10px rgba(255, 60, 3, 0.8);
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

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
</style>
