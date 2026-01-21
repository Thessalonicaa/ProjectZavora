<template>
  <!-- Global Dark Theme Wrapper -->
  <div class="min-h-screen bg-gray-950 text-white transition-colors duration-500">
    <Navbar />

    <!-- Page Transition -->
    <transition name="page" mode="out-in">
      <NuxtPage />
    </transition>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()    
const route = useRoute()

// Watch for route changes
watch(
  () => route.path,
  (newPath) => {
    const token = localStorage.getItem('token')
    const isAuthPage = ['/login', '/register', '/register-seller', '/reset-password'].includes(newPath)

    if (!token && !isAuthPage) {
      router.push('/login')
    } else if (token && isAuthPage) {
      router.push('/')
    }
  }
)

onMounted(() => {
  const token = localStorage.getItem('token')
  const isAuthPage = ['/login', '/register', '/register-seller', '/reset-password'].includes(route.path)

  if (!token && !isAuthPage) {
    router.push('/login')
  } else if (token && isAuthPage) {
    router.push('/')
  }
})
</script>

<style>
/* Transition ระหว่างเปลี่ยนหน้า */
.page-enter-active, .page-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Hide scrollbar on all browsers */
html {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  overflow-y: scroll; /* Reserve space */
}

html::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

body {
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
}
</style>
