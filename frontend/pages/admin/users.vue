<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 to-gray-900 text-white p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-4xl font-extrabold bg-gradient-to-r from-blue-500 to-blue-400 bg-clip-text text-transparent">
            <i class="fas fa-users mr-3"></i>Users & Sellers Management
          </h1>
          <p class="text-gray-400 mt-2">View, edit, and manage user accounts</p>
        </div>
        <NuxtLink to="/admin" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all flex items-center gap-2">
          <i class="fas fa-arrow-left"></i>Back to Dashboard
        </NuxtLink>
      </div>

      <div v-if="!isAdmin" class="text-center py-20">
        <p class="text-gray-400">Unauthorized</p>
        <NuxtLink to="/" class="text-red-400 mt-4 inline-block">Go Home</NuxtLink>
      </div>

      <div v-else>
        <!-- Search Bar & Add Button -->
        <div class="mb-6 flex gap-4">
          <input 
            v-model="filter" 
            placeholder="Search by username or email..." 
            class="flex-1 px-4 py-3 rounded-lg bg-gray-800 border border-gray-700 text-white focus:border-blue-500 focus:outline-none transition-all"
          />
          <button @click="fetchAll" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all flex items-center gap-2 font-semibold">
            <i class="fas fa-sync"></i>Refresh
          </button>
          <button @click="openAddUser" class="px-6 py-3 bg-green-600 hover:bg-green-700 rounded-lg transition-all flex items-center gap-2 font-semibold">
            <i class="fas fa-plus"></i>Add User
          </button>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto bg-gray-900/50 rounded-2xl border border-gray-700 shadow-xl">
          <table class="min-w-full text-left text-sm">
            <thead class="bg-gradient-to-r from-gray-800 to-gray-900 border-b border-gray-700">
              <tr>
                <th class="px-6 py-4 font-semibold text-gray-300">Username</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Role</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Created Date</th>
                <th class="px-6 py-4 font-semibold text-gray-300">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in filtered" :key="u._id" class="border-t border-gray-800 hover:bg-gray-800/50 transition-colors">
                <td class="px-6 py-4 font-semibold">{{ u.username }}</td>
                <td class="px-6 py-4">
                  <span :class="[
                    'px-3 py-1 rounded-full text-xs font-bold',
                    u.role === 'admin' ? 'bg-red-600/30 text-red-300' : u.role === 'seller' ? 'bg-blue-600/30 text-blue-300' : 'bg-gray-600/30 text-gray-300'
                  ]">
                    {{ u.role || 'user' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-400">{{ formatDate(u.created_at) }}</td>
                <td class="px-6 py-4 flex gap-2">
                  <button @click="openEdit(u)" class="px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
                    <i class="fas fa-edit"></i>Edit
                  </button>
                  <button @click="confirmDelete(u)" class="px-3 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition-all text-sm font-semibold flex items-center gap-1">
                    <i class="fas fa-trash"></i>Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddUser" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-gray-700 shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-white">Add New User</h3>
          <button @click="closeAddUser" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        
        <div class="space-y-4">
          <!-- Username -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Username</label>
            <input 
              v-model="addForm.username" 
              @blur="checkUsernameExists(addForm.username)"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
            />
            <p v-if="usernameError" class="text-red-400 text-xs mt-1">
              <i class="fas fa-exclamation-circle mr-1"></i>{{ usernameError }}
            </p>
            <p v-else-if="addForm.username && !usernameError" class="text-green-400 text-xs mt-1">
              <i class="fas fa-check-circle mr-1"></i>Username available
            </p>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Password</label>
            <input 
              v-model="addForm.password" 
              type="password"
              
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
            />
          </div>

          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Role</label>
            <select 
              v-model="addForm.role"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
            >
              <option value="user">User</option>
              <option value="seller">Seller</option>
            </select>
          </div>

          <!-- Dynamic Fields for Seller Role -->
          <transition name="fade">
            <div v-if="addForm.role === 'seller'" class="space-y-4 pt-4 border-t border-gray-700">
              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Email</label>
                <input 
                  v-model="addForm.email" 
                  type="email" 
                
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Shop Name</label>
                <input 
                  v-model="addForm.business_name" 
               
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Phone Number</label>
                <input 
                  v-model="addForm.phonenumber" 
                
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Address</label>
                <textarea 
                  v-model="addForm.address" 
                 
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all resize-none"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </transition>
        </div>

        <div class="mt-6 flex gap-3">
          <button 
            @click="performAddUser" 
            :disabled="!addForm.username || !addForm.password || usernameError"
            class="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg text-white font-bold transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            <i class="fas fa-user-plus"></i>Add User
          </button>
          <button 
            @click="closeAddUser" 
            class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editing" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-gray-700 shadow-2xl animate-scale-in max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-white">Edit User Account</h3>
          <button @click="closeEdit" class="text-gray-400 hover:text-white text-2xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        
        <div class="space-y-4">
          <!-- Username (readonly) -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Username</label>
            <input 
              v-model="editForm.username" 
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-400 cursor-not-allowed" 
              readonly 
            />
          </div>
          
          <!-- Role Selection -->
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Role</label>
            <select 
              v-model="editForm.role" 
              @change="onRoleChange"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
            >
              <option value="user">User</option>
              <option value="seller">Seller</option>
            </select>
          </div>

          <!-- Dynamic Fields for Seller Role -->
          <transition name="fade">
            <div v-if="editForm.role === 'seller'" class="space-y-4 pt-4 border-t border-gray-700">
              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Email</label>
                <input 
                  v-model="editForm.email" 
                  type="email" 
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Shop Name</label>
                <input 
                  v-model="editForm.business_name" 
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Phone Number</label>
                <input 
                  v-model="editForm.phonenumber" 
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Address</label>
                <textarea 
                  v-model="editForm.address" 
                  class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none transition-all resize-none"
                  rows="3"
                ></textarea>
              </div>
            </div>
          </transition>
        </div>

        <div class="mt-6 flex gap-3">
          <button 
            @click="saveEdit" 
            class="flex-1 px-4 py-3 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 rounded-lg text-white font-bold transition-all transform hover:scale-105 flex items-center justify-center gap-2"
          >
            <i class="fas fa-save"></i>Save Changes
          </button>
          <button 
            @click="closeEdit" 
            class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-3xl p-8 w-full max-w-md border border-red-500/50 shadow-2xl animate-scale-in">
        <div class="flex items-center justify-center w-12 h-12 rounded-full bg-red-600/20 mx-auto mb-4">
          <i class="fas fa-trash text-2xl text-red-500"></i>
        </div>
        
        <h3 class="text-2xl font-bold text-white text-center mb-2">Delete Account?</h3>
        <p class="text-gray-400 text-center mb-6">
          Are you sure you want to delete <span class="font-semibold text-white">{{ deleteTarget?.username }}</span>? This action cannot be undone.
        </p>

        <div class="flex gap-3">
          <button @click="performDelete" class="flex-1 px-4 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 rounded-lg text-white font-bold transition-all transform hover:scale-105">
            Yes, Delete
          </button>
          <button @click="closeDeleteConfirm" class="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-white font-semibold transition-all">
            Cancel
          </button>
        </div>
      </div>
    </div>

    <!-- Notification Toast -->
    <transition name="slide-down">
      <div 
        v-if="notification.show"
        :class="[
          'fixed top-6 left-1/2 transform -translate-x-1/2 z-[100] px-8 py-4 rounded-2xl border shadow-2xl flex items-center gap-3 animate-slide-down',
          notification.type === 'success' 
            ? 'bg-gradient-to-r from-green-600 to-green-700 border-green-500/50 text-white' 
            : 'bg-gradient-to-r from-red-600 to-red-700 border-red-500/50 text-white'
        ]"
      >
        <i :class="[
          'text-2xl',
          notification.type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'
        ]"></i>
        <span class="font-semibold text-lg">{{ notification.message }}</span>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const isAdmin = ref(false)
const users = ref([])
const filter = ref('')
const editing = ref(false)
const editForm = ref({})
const showDeleteConfirm = ref(false)
const deleteTarget = ref(null)
const notification = ref({ show: false, message: '', type: 'success' })
const showAddUser = ref(false)
const addForm = ref({
  username: '',
  password: '',
  role: 'user',
  email: '',
  business_name: '',
  phonenumber: '',
  address: ''
})
const usernameError = ref('')

const fetchAll = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('No token found')
      return
    }

    const res = await fetch('http://localhost:5000/api/admin/users', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    const data = await res.json()
    if (data.success) users.value = data.users || []
    else console.error('Error fetching users:', data.error)
  } catch (e) { console.error('Fetch error:', e) }
}

const filtered = computed(() => {
  if (!filter.value) return users.value
  return users.value.filter(u => 
    (u.username || '').toLowerCase().includes(filter.value.toLowerCase())
  )
})

const formatDate = (d) => d ? new Date(d).toLocaleDateString('th-TH') : '-'

const openEdit = (u) => { editForm.value = { ...u }; editing.value = true }
const closeEdit = () => { editing.value = false; editForm.value = {} }

const openAddUser = () => { 
  showAddUser.value = true
  addForm.value = {
    username: '',
    password: '',
    role: 'user',
    email: '',
    business_name: '',
    phonenumber: '',
    address: ''
  }
  usernameError.value = ''
}

const closeAddUser = () => { 
  showAddUser.value = false
  usernameError.value = ''
}

const checkUsernameExists = async (username) => {
  if (!username) {
    usernameError.value = ''
    return
  }
  try {
    const res = await fetch(`http://localhost:5000/api/check-username/${username}`)
    const data = await res.json()
    if (data.exists) {
      usernameError.value = 'ชื่อผู้ใช้นี้ถูกใช้ไปแล้ว กรุณาลองชื่อแอื่น'
    } else {
      usernameError.value = ''
    }
  } catch (e) {
    console.error(e)
    usernameError.value = 'ไม่สามารถตรวจสอบชื่อผู้ใช้ได้'
  }
}

const performAddUser = async () => {
  try {
    // Validate required fields
    if (!addForm.value.username || !addForm.value.password) {
      showNotification('❌ Please fill in username and password', 'error')
      return
    }

    // Check for duplicate username
    if (usernameError.value) {
      showNotification('❌ Username already exists', 'error')
      return
    }

    // Validate password length
    if (addForm.value.password.length < 6) {
      showNotification('❌ Password must be at least 6 characters', 'error')
      return
    }

    const payload = {
      username: addForm.value.username,
      password: addForm.value.password,
      role: addForm.value.role
    }

    // If seller, validate and add seller fields
    if (addForm.value.role === 'seller') {
      if (!addForm.value.email || !addForm.value.business_name) {
        showNotification('❌ Please fill in email and shop name for sellers', 'error')
        return
      }
      
      // Validate email format
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(addForm.value.email)) {
        showNotification('❌ Please enter a valid email', 'error')
        return
      }

      payload.email = addForm.value.email
      payload.business_name = addForm.value.business_name
      payload.phonenumber = addForm.value.phonenumber
      payload.address = addForm.value.address
    }

    const res = await fetch('http://localhost:5000/api/admin/users', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(payload)
    })

    const data = await res.json()
    if (data.success) {
      fetchAll()
      closeAddUser()
      showNotification('✅ User added successfully!', 'success')
    } else {
      showNotification('❌ ' + (data.message || 'Error adding user'), 'error')
    }
  } catch (e) {
    console.error(e)
    showNotification('❌ Error adding user', 'error')
  }
}

// Watch for username changes in add form
watch(() => addForm.value.username, (newVal) => {
  if (newVal) {
    checkUsernameExists(newVal)
  }
})

const onRoleChange = () => {
  // When switching to seller, initialize seller fields if not present
  if (editForm.value.role === 'seller') {
    if (!editForm.value.email) editForm.value.email = ''
    if (!editForm.value.business_name) editForm.value.business_name = ''
    if (!editForm.value.phonenumber) editForm.value.phonenumber = ''
    if (!editForm.value.address) editForm.value.address = ''
  }
}

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

const saveEdit = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/admin/users/${editForm.value._id}`, {
      method: 'PUT', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }, 
      body: JSON.stringify(editForm.value)
    })
    const data = await res.json()
    if (data.success) { 
      fetchAll()
      closeEdit()
      showNotification('✅ User updated successfully!', 'success')
    } else {
      showNotification('❌ ' + (data.message || data.error || 'Error updating user'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showNotification('❌ Error updating user', 'error')
  }
}

const confirmDelete = (u) => { deleteTarget.value = u; showDeleteConfirm.value = true }
const closeDeleteConfirm = () => { showDeleteConfirm.value = false; deleteTarget.value = null }

const performDelete = async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await fetch(`http://localhost:5000/api/admin/users/${deleteTarget.value._id}`, { 
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    const data = await res.json()
    if (data.success) { 
      fetchAll()
      closeDeleteConfirm()
      showNotification('✅ User deleted successfully!', 'success')
    } else {
      showNotification('❌ ' + (data.message || data.error || 'Error deleting user'), 'error')
    }
  } catch (e) { 
    console.error(e)
    showNotification('❌ Error deleting user', 'error')
  }
}

onMounted(() => {
  if (process.client) {
    const role = localStorage.getItem('role')
    isAdmin.value = role === 'admin' || localStorage.getItem('is_admin') === 'true'
    if (!isAdmin.value) return
    fetchAll()
  }
})
</script>

<style scoped>
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes slideDown {
  from { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
  to { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
}

@keyframes slideUp {
  from { 
    opacity: 1; 
    transform: translate(-50%, 0); 
  }
  to { 
    opacity: 0; 
    transform: translate(-50%, -30px); 
  }
}

.animate-scale-in { animation: scaleIn 0.3s ease-out; }
.animate-slide-down { animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }

.slide-down-enter-active { animation: slideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1); }
.slide-down-leave-active { animation: slideUp 0.3s ease-in; }

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>