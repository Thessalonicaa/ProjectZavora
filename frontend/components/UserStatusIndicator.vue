<template>
  <div 
    :class="[
      'absolute -bottom-2 -right-2 w-8 h-8 rounded-full border-4 border-gray-950 flex items-center justify-center shadow-lg text-lg transition-all duration-300',
      statusColorClass
    ]"
    :title="statusText"
  >
    <i :class="[
      'fas text-white font-bold transition-all duration-300',
      statusIconClass
    ]"></i>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    default: 'online', // 'online', 'away', 'offline'
  }
})

const statusColorClass = computed(() => {
  switch (props.status) {
    case 'online':
      return 'bg-green-500 ring-2 ring-green-400 shadow-green-500/50'
    case 'away':
      return 'bg-yellow-500 ring-2 ring-yellow-400 shadow-yellow-500/50'
    case 'offline':
      return 'bg-gray-500 ring-2 ring-gray-400 shadow-gray-500/50'
    default:
      return 'bg-green-500 ring-2 ring-green-400 shadow-green-500/50'
  }
})

const statusIconClass = computed(() => {
  switch (props.status) {
    case 'online':
      return 'fa-check text-sm'
    case 'away':
      return 'fa-moon text-xs'
    case 'offline':
      return 'fa-circle text-xs'
    default:
      return 'fa-check text-sm'
  }
})

const statusText = computed(() => {
  switch (props.status) {
    case 'online':
      return 'Online'
    case 'away':
      return 'Away'
    case 'offline':
      return 'Offline'
    default:
      return 'Online'
  }
})
</script>

<style scoped>
.ring-2 {
  box-shadow: 0 0 0 2px currentColor;
}
</style>