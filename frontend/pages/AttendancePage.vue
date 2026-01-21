<template>
  <div class="min-h-screen bg-gray-950 text-white p-6">
    <div class="max-w-4xl mx-auto">
      <div class="mb-8">
        <h1 class="text-4xl font-bold mb-2 text-gradient">Attendance Tracking</h1>
        <p class="text-gray-400">Track your attendance with check-in and check-out times</p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-4 mb-8">
        <button
          @click="markAttendance('in')"
          class="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg font-semibold transition-all transform hover:scale-105"
        >
          <i class="fas fa-sign-in-alt mr-2"></i>Check In
        </button>
        <button
          @click="markAttendance('out')"
          class="px-6 py-3 bg-red-600 hover:bg-red-700 rounded-lg font-semibold transition-all transform hover:scale-105"
        >
          <i class="fas fa-sign-out-alt mr-2"></i>Check Out
        </button>
      </div>

      <!-- Attendance Logs Table -->
      <div class="bg-gray-900/50 rounded-xl border border-gray-700 overflow-hidden">
        <table class="w-full text-left">
          <thead class="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700">
            <tr>
              <th class="px-6 py-4 font-semibold">Date & Time</th>
              <th class="px-6 py-4 font-semibold">Type</th>
              <th class="px-6 py-4 font-semibold">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(log, idx) in attendanceLogs" :key="idx" class="border-t border-gray-700 hover:bg-gray-800/50 transition-colors">
              <td class="px-6 py-4">{{ formatDate(log.timestamp) }}</td>
              <td class="px-6 py-4">
                <span :class="[
                  'px-3 py-1 rounded-full text-xs font-bold',
                  log.type === 'in' ? 'bg-green-600/30 text-green-400' : 'bg-red-600/30 text-red-400'
                ]">
                  {{ log.type === 'in' ? 'Check In' : 'Check Out' }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-300">✓ Recorded</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const attendanceLogs = ref([])

const fetchLogs = async () => {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get('http://localhost:5000/api/attendance', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    attendanceLogs.value = res.data
  } catch (e) {
    console.error('Fetch attendance logs failed:', e)
  }
}

const markAttendance = async (type) => {
  const token = localStorage.getItem('token')
  try {
    await axios.post(
      'http://localhost:5000/api/attendance',
      { type }, // type: 'in' or 'out'
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
    fetchLogs()
  } catch (e) {
    console.error('Mark attendance failed:', e)
  }
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString('th-TH', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

onMounted(fetchLogs)
</script>

<style scoped>
.text-gradient {
  background: linear-gradient(to right, #ff6b6b, #ff8e53);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
