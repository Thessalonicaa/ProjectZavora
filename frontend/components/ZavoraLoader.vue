<template>
  <Transition name="loader">
    <div v-if="show" class="zavora-loader">
      <div class="zavora-text">
        <span v-for="(letter, index) in letters" :key="index" :style="{ animationDelay: `${index * 0.1}s` }" class="letter">
          {{ letter }}
        </span>
      </div>
      <div class="loader-bar">
        <div class="loader-progress"></div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const props = defineProps({
  duration: { type: Number, default: 2500 }
})

const emit = defineEmits(['complete'])

const show = ref(true)
const letters = 'ZAVORA'.split('')

onMounted(() => {
  // Only show on home page (/) or first ever visit
  const isHomePage = route.path === '/'
  const isFirstEverVisit = !localStorage.getItem('app_initialized')
  
  // Check if just logged in
  const justLoggedIn = sessionStorage.getItem('just_logged_in')
  
  // Show loader if:
  // 1. Home page AND (first visit OR just logged in)
  // 2. OR first ever visit to app
  const shouldShowLoader = (isHomePage && (isFirstEverVisit || justLoggedIn)) || isFirstEverVisit
  
  if (!shouldShowLoader) {
    show.value = false
    emit('complete')
    return
  }
  
  // Mark app as initialized
  localStorage.setItem('app_initialized', 'true')
  
  // Clear just logged in flag
  if (justLoggedIn) {
    sessionStorage.removeItem('just_logged_in')
  }
  
  // Show loader for the specified duration
  setTimeout(() => {
    show.value = false
    setTimeout(() => {
      emit('complete')
    }, 600)
  }, props.duration)
})
</script>

<style scoped>
.zavora-loader {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: linear-gradient(135deg, #000000 0%, #1a0000 50%, #000000 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

.zavora-text {
  display: flex;
  gap: 0.5rem;
  font-size: 6rem;
  font-weight: 900;
  letter-spacing: 0.2rem;
}

.letter {
  display: inline-block;
  background: linear-gradient(135deg, #ff3c03, #ff8c00, #ff3c03);
  background-size: 200% 200%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: letterPop 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards,
             gradientShift 3s ease infinite;
  opacity: 0;
  transform: scale(0) rotateY(180deg);
  text-shadow: 0 0 30px rgba(255, 60, 3, 0.5);
}

@keyframes letterPop {
  0% {
    opacity: 0;
    transform: scale(0) rotateY(180deg);
  }
  50% {
    transform: scale(1.2) rotateY(0deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateY(0deg);
  }
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.loader-bar {
  width: 300px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  position: relative;
}

.loader-progress {
  height: 100%;
  background: linear-gradient(90deg, #ff3c03, #ff8c00);
  border-radius: 2px;
  animation: progress 2.5s ease-out forwards;
  box-shadow: 0 0 20px rgba(255, 60, 3, 0.8);
}

@keyframes progress {
  from {
    width: 0%;
  }
  to {
    width: 100%;
  }
}

.loader-enter-active,
.loader-leave-active {
  transition: all 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.loader-leave-to {
  opacity: 0;
  transform: translateY(-100%) scale(0.8);
}
</style>
