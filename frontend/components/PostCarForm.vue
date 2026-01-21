<template>
  <div class="space-y-6">
    <!-- Brand with Autocomplete -->
    <div class="relative">
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-car mr-2 text-red-500"></i>Brand
      </label>
      <input
        v-model="form.brand"
        type="text"
        placeholder="Start typing brand name..."
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        @focus="showBrandSuggestions = true"
        @blur="setTimeout(() => showBrandSuggestions = false, 200)"
      />
      <!-- Brand Suggestions -->
      <div 
        v-if="showBrandSuggestions && filteredBrands.length > 0"
        class="absolute top-full left-0 right-0 mt-1 bg-gray-700 border border-gray-600 rounded-lg shadow-lg z-10 max-h-48 overflow-y-auto"
      >
        <button
          v-for="brand in filteredBrands"
          :key="brand"
          @click="selectBrand(brand)"
          class="w-full text-left px-4 py-2 hover:bg-gray-600 text-white transition-colors"
        >
          {{ brand }}
        </button>
      </div>
      <p v-if="!form.brand" class="text-gray-400 text-xs mt-1">
        <i class="fas fa-info-circle mr-1"></i>Popular brands: Toyota, Honda, BMW, Mercedes
      </p>
    </div>

    <!-- Model -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-cube mr-2 text-red-500"></i>Model
      </label>
      <input
        v-model="form.model"
        type="text"
        placeholder="e.g., Camry, Civic, X5"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      />
    </div>

    <!-- Year with validation -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-calendar mr-2 text-red-500"></i>Year
      </label>
      <input
        v-model.number="form.year"
        type="number"
        :min="1900"
        :max="currentYear"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      />
      <p v-if="form.year > currentYear" class="text-red-400 text-xs mt-1">
        <i class="fas fa-exclamation-circle mr-1"></i>Year cannot be in the future
      </p>
      <p v-else-if="form.year" class="text-green-400 text-xs mt-1">
        <i class="fas fa-check-circle mr-1"></i>Valid year
      </p>
    </div>

    <!-- Engine Size (Dropdown) -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-cog mr-2 text-red-500"></i>Engine Size (cc)
      </label>
      <select
        v-model="form.engineSize"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      >
        <option value="">-- Select Engine Size --</option>
        <option value="800">800 cc (Small)</option>
        <option value="1000">1000 cc</option>
        <option value="1200">1200 cc</option>
        <option value="1500">1500 cc</option>
        <option value="1600">1600 cc</option>
        <option value="1800">1800 cc</option>
        <option value="2000">2000 cc</option>
        <option value="2500">2500 cc</option>
        <option value="3000">3000 cc (Large)</option>
        <option value="3500">3500 cc</option>
        <option value="5000">5000 cc (Luxury)</option>
      </select>
    </div>

    <!-- Color (Dropdown) -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-palette mr-2 text-red-500"></i>Color
      </label>
      <select
        v-model="form.color"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      >
        <option value="">-- Select Color --</option>
        <option value="Black">Black</option>
        <option value="White">White</option>
        <option value="Silver">Silver</option>
        <option value="Gray">Gray</option>
        <option value="Red">Red</option>
        <option value="Blue">Blue</option>
        <option value="Green">Green</option>
        <option value="Brown">Brown</option>
        <option value="Gold">Gold</option>
        <option value="Beige">Beige</option>
        <option value="Orange">Orange</option>
        <option value="Purple">Purple</option>
        <option value="other">Other (please specify below)</option>
      </select>
    </div>

    <!-- Custom Color if "Other" selected -->
    <div v-if="form.color === 'other'">
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-pen mr-2 text-red-500"></i>Specify Color
      </label>
      <input
        v-model="form.customColor"
        type="text"
        placeholder="e.g., Dark Blue Metallic"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      />
    </div>

    <!-- Additional Features (Free text) -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-star mr-2 text-red-500"></i>Additional Features
      </label>
      <textarea
        v-model="form.additionalFeatures"
        placeholder="E.g., Leather seats, Sunroof, Navigation system, Premium sound system..."
        rows="3"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all resize-none"
      ></textarea>
      <p class="text-gray-400 text-xs mt-1">Optional: List any special features or upgrades</p>
    </div>

    <!-- Fuel Type -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-gas-pump mr-2 text-red-500"></i>Fuel Type
      </label>
      <select
        v-model="form.fuelType"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      >
        <option value="Petrol">Petrol</option>
        <option value="Diesel">Diesel</option>
        <option value="Hybrid">Hybrid</option>
        <option value="Electric">Electric</option>
      </select>
    </div>

    <!-- Transmission -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-gears mr-2 text-red-500"></i>Transmission
      </label>
      <select
        v-model="form.transmission"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      >
        <option value="Automatic">Automatic</option>
        <option value="Manual">Manual</option>
      </select>
    </div>

    <!-- Car Type -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">
        <i class="fas fa-car-side mr-2 text-red-500"></i>Car Type
      </label>
      <select
        v-model="form.carType"
        class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-red-500 focus:outline-none transition-all"
        required
      >
        <option value="Sedan">Sedan</option>
        <option value="SUV">SUV</option>
        <option value="Pickup">Pickup</option>
        <option value="Van">Van</option>
        <option value="Sports">Sports</option>
      </select>
    </div>

    <!-- Slot for additional content -->
    <slot></slot>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const form = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const showBrandSuggestions = ref(false)

const carBrands = [
  'Toyota', 'Honda', 'BMW', 'Mercedes-Benz', 'Audi', 'Volkswagen',
  'Ford', 'Chevrolet', 'GMC', 'Dodge', 'Jeep', 'RAM',
  'Hyundai', 'Kia', 'Mazda', 'Subaru', 'Nissan', 'Mitsubishi',
  'Volvo', 'Tesla', 'Porsche', 'Lamborghini', 'Ferrari',
  'Lexus', 'Acura', 'Infiniti', 'Cadillac', 'Lincoln', 'Buick'
]

const filteredBrands = computed(() => {
  if (!form.value.brand) return carBrands
  return carBrands.filter(b =>
    b.toLowerCase().includes(form.value.brand.toLowerCase())
  )
})

const currentYear = new Date().getFullYear()

const selectBrand = (brand) => {
  form.value.brand = brand
  showBrandSuggestions.value = false
}
</script>

<style scoped>
/* ...existing code... */
</style>