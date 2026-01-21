<template>
  <div class="min-h-screen bg-gray-950 text-white p-6 relative overflow-hidden">
    <Beams
      :beamWidth="3"
      :beamHeight="25"
      :beamNumber="20"
      lightColor="#ff3c03"
      :speed="2"
      :noiseIntensity="1.75"
      :scale="0.2"
      :rotation="30"
      :width="1920"
      :height="1080"
    />
    <div class="max-w-3xl mx-auto relative z-10">
      <!-- Header with Animation -->
      <div class="text-center mb-12 animate-slide-down">
        <div class="inline-block mb-4">
          <div class="w-16 h-16 bg-gradient-to-br  rounded-full flex items-center justify-center shadow-lg">
            <i class="fas fa-car-side text-3xl text-white"></i>
          </div>
        </div>
        <h1 class="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-red-500 via-orange-500 to-red-500 bg-clip-text text-transparent mb-3 drop-shadow-lg">
          {{ currentLanguage === 'th' ? 'โพสต์รถของคุณ' : 'Post Your Car' }}
        </h1>
        <p class="text-gray-400 text-lg">{{ currentLanguage === 'th' ? 'แชร์รถของคุณกับผู้ซื้อหลายพันคน' : 'Share your vehicle with thousands of buyers' }}</p>
      </div>

      <!-- Seller Info Card -->
      <div class="bg-gradient-to-r from-red-600/20 via-red-500/10 to-orange-600/20 border border-red-500/30 rounded-2xl p-6 mb-8 animate-fade-in backdrop-blur-sm hover:border-red-500/50 transition-all duration-300 shadow-lg">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 bg-gradient-to-br from-red-600 to-orange-600 rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform duration-300">
            <i class="fas fa-user-check text-white text-lg"></i>
          </div>
          <div>
            <p class="text-gray-400 text-sm font-semibold uppercase tracking-wide">Seller Account</p>
            <p class="text-white font-bold text-xl">{{ sellerName }}</p>
          </div>
        </div>
      </div>

      <!-- Form Container with Enhanced Styling -->
      <form @submit.prevent="handleSubmit" class="bg-gradient-to-br from-gray-900/80 to-gray-950/80 border border-gray-800/50 hover:border-red-500/20 rounded-2xl p-10 backdrop-blur-sm space-y-8 animate-slide-up shadow-2xl transition-all duration-300">
        
        <!-- Section Title Helper -->
        <div class="border-b border-gray-700/50 pb-4 mb-6">
          <h2 class="text-2xl font-bold text-white flex items-center gap-3">
            <i class="fas fa-info-circle text-red-500"></i>
            {{ currentLanguage === 'th' ? 'ข้อมูลรถยนต์' : 'Vehicle Information' }}
          </h2>
        </div>
        
        <!-- Vehicle Type Selection -->
        <div class="form-group animate-form-item" style="animation-delay: 0.05s">
          <label class="flex items-center gap-2 text-gray-300 font-semibold mb-3">
            <i class="fas fa-cube text-red-500 text-lg"></i>{{ currentLanguage === 'th' ? 'ประเภทของรถ' : 'Vehicle Type' }} <span class="text-red-500"></span>
          </label>
          <select
            v-model="carData.vehicleType"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 hover:border-red-500/50 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all duration-300 shadow-sm"
            required
          >
            <option value="">{{ currentLanguage === 'th' ? 'เลือกประเภทของรถ' : 'Select Vehicle Type' }}</option>
            <option value="Car">{{ currentLanguage === 'th' ? 'รถยนต์' : 'Car' }}</option>
            <!--<option value="Motorcycle">Motorcycle </option>
            <option value="Bike">Bike </option>--> 
          </select>
        </div>
        
        <!-- Car Brand with Autocomplete -->
        <div class="form-group animate-form-item" style="animation-delay: 0.1s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-tag text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'แบรนด์' : 'Brand' }}<span class="text-red-500"></span>
          </label>
          <div class="relative">
            <input
              v-model="carData.brand"
              type="text"
              placeholder="e.g., Toyota, Honda, BMW"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              :class="{ 'border-red-500 ring-2 ring-red-500/50': isBrandInvalid }"
              @input="filterBrands"
              required
            />
            <!-- Brand Error Alert -->
            <div v-if="isBrandInvalid" class="absolute -bottom-8 left-0 bg-red-600 text-white px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-2 whitespace-nowrap">
              <i class="fas fa-exclamation-circle"></i>
              {{ currentLanguage === 'th' ? 'กรุณาตรงกับชื่อแบรนด์อย่างถูกต้อง' : 'Please match brand name exactly' }}
            </div>
            <!-- Brand Suggestions - Fixed Modal Style -->
            <div v-if="showBrandSuggestions && filteredBrands.length > 0" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800 border border-gray-700 rounded-xl max-w-sm w-80 max-h-48 overflow-y-auto z-50 shadow-2xl">
              <div class="sticky top-0 bg-gray-800 px-4 py-2 border-b border-gray-700">
                <p class="text-gray-400 text-xs font-semibold">{{ currentLanguage === 'th' ? 'เลือกแบรนด์' : 'SELECT BRAND' }}</p>
              </div>
              <div
                v-for="brand in filteredBrands"
                :key="brand"
                @click="selectBrand(brand)"
                class="px-4 py-2 hover:bg-gray-700 cursor-pointer text-white transition-colors border-b border-gray-700 last:border-b-0"
              >
                {{ brand }}
              </div>
            </div>
          </div>
        </div>
        <!-- Car Model -->
        <div class="form-group animate-form-item" style="animation-delay: 0.2s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-edit text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'รุ่น' : 'Model' }} <span class="text-red-500"></span>
          </label>
          <input
            v-model="carData.model"
            type="text"
            placeholder="e.g., Camry, Civic, X5"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          />
        </div>

        <!-- Car Color -->
        <div class="form-group animate-form-item" style="animation-delay: 0.25s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-palette text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'สี' : 'Color' }} <span class="text-red-500"></span>
          </label>
          <select
            v-model="carData.color"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          >
            <option value="">{{ currentLanguage === 'th' ? 'เลือกสี' : 'Select Color' }}</option>
            <option value="White">{{ currentLanguage === 'th' ? 'ขาว' : 'White' }}</option>
            <option value="Black">{{ currentLanguage === 'th' ? 'ดำ' : 'Black' }}</option>
            <option value="Silver">{{ currentLanguage === 'th' ? 'เงิน' : 'Silver' }}</option>
            <option value="Gray">{{ currentLanguage === 'th' ? 'เทา' : 'Gray' }}</option>
            <option value="Red">{{ currentLanguage === 'th' ? 'แดง' : 'Red' }}</option>
            <option value="Blue">{{ currentLanguage === 'th' ? 'น้ำเงิน' : 'Blue' }}</option>
            <option value="Green">{{ currentLanguage === 'th' ? 'เขียว' : 'Green' }}</option>
            <option value="Yellow">{{ currentLanguage === 'th' ? 'เหลือง' : 'Yellow' }}</option>
            <option value="Orange">{{ currentLanguage === 'th' ? 'ส้ม' : 'Orange' }}</option>
            <option value="Brown">{{ currentLanguage === 'th' ? 'น้ำตาล' : 'Brown' }}</option>
            <option value="Gold">{{ currentLanguage === 'th' ? 'ทอง' : 'Gold' }}</option>
            <option value="Beige">{{ currentLanguage === 'th' ? 'เบจ' : 'Beige' }}</option>
            <option value="Purple">{{ currentLanguage === 'th' ? 'ม่วง' : 'Purple' }}</option>
            <option value="Pink">{{ currentLanguage === 'th' ? 'ชมพู' : 'Pink' }}</option>
            <option value="Maroon">{{ currentLanguage === 'th' ? 'น้ำตาลแดง' : 'Maroon' }}</option>
            <option value="Navy">{{ currentLanguage === 'th' ? 'น้ำเงิน' : 'Navy' }}</option>
            <option value="Turquoise">{{ currentLanguage === 'th' ? 'เทอร์ควอยซ์' : 'Turquoise' }}</option>
            <option value="Cream">{{ currentLanguage === 'th' ? 'ครีม' : 'Cream' }}</option>
          </select>
        </div>
        <!-- Year and Price Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group animate-form-item" style="animation-delay: 0.3s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-calendar text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ปี' : 'Year' }} <span class="text-red-500"></span>
            </label>
            <input
              v-model.number="carData.year"
              type="number"
              :placeholder="`${currentYear}`"
              :max="currentYear"
              :min="1900"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            />
            <p v-if="carData.year > currentYear" class="text-red-400 text-xs mt-1">
              <i class="fas fa-exclamation-circle mr-1"></i>{{ currentLanguage === 'th' ? 'ปี' : 'Year' }} cannot exceed {{ currentYear }}
            </p>
          </div>
          <div class="form-group animate-form-item" style="animation-delay: 0.4s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-dollar-sign text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ราคา (฿)' : 'Price (฿)' }} <span class="text-red-500"></span>
            </label>
            <input
              v-model="carData.price"
              type="number"
              placeholder="100000"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            />
          </div>
        </div>
        <!-- Fuel Type & Gas System Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group animate-form-item" style="animation-delay: 0.45s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-gas-pump text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทเชื้อเพลิง' : 'Fuel Type' }} <span class="text-red-500"></span>
            </label>
            <select
              v-model="carData.fuelType"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกประเภทเชื้อเพลิง' : 'Select Fuel Type' }}</option>
              <option value="Petrol">{{ currentLanguage === 'th' ? 'เบนซิน' : 'Petrol' }}</option>
              <option value="Diesel">{{ currentLanguage === 'th' ? 'ดีเซล' : 'Diesel' }}</option>
              <option value="Hybrid">{{ currentLanguage === 'th' ? 'ไฮบริด' : 'Hybrid' }}</option>
              <option value="Electric">{{ currentLanguage === 'th' ? 'ไฟฟ้า' : 'Electric' }}</option>
            </select>
          </div>
          <div class="form-group animate-form-item" style="animation-delay: 0.5s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-water text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ระบบแก๊ส' : 'Gas System' }}
            </label>
            <select
              v-model="carData.gasSystem"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกระบบแก๊ส' : 'Select Gas System' }}</option>
              <option value="NGV">{{ currentLanguage === 'th' ? 'NGV' : 'NGV' }}</option>
              <option value="LPG">{{ currentLanguage === 'th' ? 'LPG' : 'LPG' }}</option>
              <option value="None">{{ currentLanguage === 'th' ? 'ไม่มีระบบแก๊ส' : 'Not equipped gas system' }}</option>
            </select>
          </div>
        </div>

        <!-- Engine Size -->
        <div class="form-group animate-form-item" style="animation-delay: 0.52s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-cube text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ขนาดเครื่องยนต์ (cc) / อื่นๆ' : 'Engine Size (cc) / Other' }}
          </label>
          <input
            v-model="carData.engineSize"
            type="text"
            placeholder="e.g., 2000cc, 3.5L, Hybrid"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          />
        </div>
        <!-- Transmission & Drive System Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="form-group animate-form-item" style="animation-delay: 0.55s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-cog text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ระบบส่งกำลัง' : 'Transmission' }} <span class="text-red-500"></span>
            </label>
            <select
              v-model="carData.transmission"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
              required
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกระบบส่งกำลัง' : 'Select Transmission' }}</option>
              <option value="Automatic">{{ currentLanguage === 'th' ? 'อัตโนมัติ' : 'Automatic' }}</option>
              <option value="Semi-Automatic">{{ currentLanguage === 'th' ? 'กึ่งอัตโนมัติ' : 'Semi-Automatic' }}</option>
              <option value="Manual">{{ currentLanguage === 'th' ? 'ธรรมดา' : 'Manual' }}</option>
              <option value="CVT">{{ currentLanguage === 'th' ? 'CVT' : 'CVT' }}</option>
              <option value="e-CVT">{{ currentLanguage === 'th' ? 'e-CVT' : 'e-CVT' }}</option>
              <option value="DCT">{{ currentLanguage === 'th' ? 'DCT' : 'DCT' }}</option>
            </select>
          </div>
          
          <div class="form-group animate-form-item" style="animation-delay: 0.58s">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-car text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ระบบขับเคลื่อน' : 'Drive System' }}
            </label>
            <select
              v-model="carData.driveSystem"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกระบบขับเคลื่อน' : 'Select Drive System' }}</option>
              <option value="FWD">{{ currentLanguage === 'th' ? 'FWD' : 'FWD' }}</option>
              <option value="RWD">{{ currentLanguage === 'th' ? 'RWD' : 'RWD' }}</option>
              <option value="AWD">{{ currentLanguage === 'th' ? 'AWD' : 'AWD' }}</option>
              <option value="4WD">{{ currentLanguage === 'th' ? '4WD' : '4WD' }}</option>
            </select>
          </div>
        </div>
        <!-- Car Type -->
        <div class="form-group animate-form-item" style="animation-delay: 0.6s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-car-side text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทของรถ' : 'Car Type' }} <span class="text-red-500"></span>
          </label>
          <select
            v-model="carData.carType"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            required
          >
            <option value="">{{ currentLanguage === 'th' ? 'ประเภทของรถ' : 'Select Car Type' }}</option>
            <option value="Sedan">{{ currentLanguage === 'th' ? 'รถเก๋ง' : 'Sedan' }}</option>
            <option value="Coupe">{{ currentLanguage === 'th' ? 'รถคูเป้' : 'Coupe' }}</option>
            <option value="Convertible">{{ currentLanguage === 'th' ? 'รถเปิดประทุน' : 'Convertible' }}</option>
            <option value="Hatchback">{{ currentLanguage === 'th' ? 'แฮทช์แบ็ก' : 'Hatchback' }}</option>
            <option value="MPV">{{ currentLanguage === 'th' ? 'รถยนต์อเนกประสงค์' : 'MPV' }}</option>
            <option value="Roadster">{{ currentLanguage === 'th' ? 'โรดสเตอร์' : 'Roadster' }}</option>
            <option value="SUV">{{ currentLanguage === 'th' ? 'รถสปอร์ตอเนกประสงค์' : 'SUV' }}</option>
            <option value="Pickup">{{ currentLanguage === 'th' ? 'รถกะบะ' : 'Pickup' }}</option>
            <option value="Van">{{ currentLanguage === 'th' ? 'รถตู้' : 'Van' }}</option>
            <option value="Sports">{{ currentLanguage === 'th' ? 'รถสปอร์ต' : 'Sports' }}</option>
          </select>
        </div>

        <!-- Dynamic Fields: MPV Options -->
        <div v-if="carData.carType === 'MPV'" class="form-group animate-form-item" style="animation-delay: 0.65s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-bars text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ขนาด MPV' : 'MPV Size' }}
          </label>
          <select
            v-model="carData.mpvSize"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          >
            <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบ MPV' : 'Select MPV Size' }}</option>
            <option value="Compact">{{ currentLanguage === 'th' ? 'MPV ขนาดกะทัดรัด' : 'Compact MPV' }}</option>
            <option value="Mid-Size">{{ currentLanguage === 'th' ? 'MPV ขนาดกลาง' : 'Mid-Size MPV' }}</option>
            <option value="Full-Size">{{ currentLanguage === 'th' ? 'MPV ขนาดใหญ่' : 'Full-Size MPV' }}</option>
          </select>
        </div>

        <!-- Dynamic Fields: Convertible Options -->
        <div v-if="carData.carType === 'Convertible'" class="space-y-4 animate-form-item" style="animation-delay: 0.65s">
          <div class="form-group">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-umbrella text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทหลังคา' : 'Top Type' }}
            </label>
            <select
              v-model="carData.convertibleTop"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบหลังคา' : 'Select Top Type' }}</option>
              <option value="Soft Top">{{ currentLanguage === 'th' ? 'หลังคาแบบนิ่ม' : 'Soft Top' }}</option>
              <option value="Retractable Hard Top">{{ currentLanguage === 'th' ? 'หลังคาแข็งแบบพับได้' : 'Retractable Hard Top' }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-chair text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ความจุที่นั่ง' : 'Seat Capacity' }}
            </label>
            <select
              v-model="carData.convertibleSeats"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบที่นั่ง' : 'Select Seat Capacity' }}</option>
              <option value="2 Seats">{{ currentLanguage === 'th' ? '2 ที่นั่ง' : '2 Seats' }}</option>
              <option value="4 Seats">{{ currentLanguage === 'th' ? '4 ที่นั่ง' : '4 Seats' }}</option>
            </select>
          </div>
        </div>

        <!-- Dynamic Fields: Van Options -->
        <div v-if="carData.carType === 'Van'" class="form-group animate-form-item" style="animation-delay: 0.65s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-cube text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทตู้' : 'Van Type' }}
          </label>
          <select
            v-model="carData.vanType"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          >
            <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบตู้' : 'Select Van Type' }}</option>
            <option value="Cargo Van">{{ currentLanguage === 'th' ? 'ตู้สินค้า' : 'Cargo Van' }}</option>
            <option value="Minivan">{{ currentLanguage === 'th' ? 'มินิแวน' : 'Minivan' }}</option>
          </select>
        </div>

        <!-- Dynamic Fields: SUV Options -->
        <div v-if="carData.carType === 'SUV'" class="form-group animate-form-item" style="animation-delay: 0.65s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-chair text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ความจุที่นั่ง' : 'Seat Capacity' }}
          </label>
          <select
            v-model="carData.suvSeats"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          >
            <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบที่นั่ง' : 'Select Seat Capacity' }}</option>
            <option value="2 Seats">{{ currentLanguage === 'th' ? '2 ที่นั่ง' : '2 Seats' }}</option>
            <option value="4 Seats">{{ currentLanguage === 'th' ? '4 ที่นั่ง' : '4 Seats' }}</option>
          </select>
        </div>

        <!-- Dynamic Fields: Pickup Options -->
        <div v-if="carData.carType === 'Pickup'" class="space-y-4 animate-form-item" style="animation-delay: 0.65s">
          <div class="form-group">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-truck text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทแค็บ' : 'Cab Type' }}
            </label>
            <select
              v-model="carData.pickupCab"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบแค็บ' : 'Select Cab Type' }}</option>
              <option value="Single Cab">{{ currentLanguage === 'th' ? 'แค็บเดี่ยว – 2 ที่นั่ง' : 'Single Cab – 2 Seats' }}</option>
              <option value="Extra Cab">{{ currentLanguage === 'th' ? 'แค็บพิเศษ – 2 ที่นั่ง' : 'Extra Cab – 2 Seats' }}</option>
              <option value="Double Cab">{{ currentLanguage === 'th' ? 'แค็บคู่ – 4 ที่นั่ง' : 'Double Cab – 4 Seats' }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="block text-gray-300 font-semibold mb-2">
              <i class="fas fa-box text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ประเภทตัวถัง' : 'Body Type' }}
            </label>
            <select
              v-model="carData.pickupBodyType"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            >
              <option value="">{{ currentLanguage === 'th' ? 'เลือกรูปแบบตัวถัง' : 'Select Body Type' }}</option>
              <option value="Box Body">{{ currentLanguage === 'th' ? 'ตู้บรรทุก' : 'Box Body' }}</option>
              <option value="Flatbed">{{ currentLanguage === 'th' ? 'แผ่นเรียบ' : 'Flatbed' }}</option>
              <option value="Dropside">{{ currentLanguage === 'th' ? 'ข้างเปิด' : 'Dropside' }}</option>
              <option value="Chassis Cab">{{ currentLanguage === 'th' ? 'ปกติ' : 'Normal' }}</option>
            </select>
          </div>
        </div>

        <!-- Mileage -->
        <div class="form-group animate-form-item" style="animation-delay: 0.7s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-tachometer-alt text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'ระยะทาง (กม.)' : 'Mileage (km)' }}
          </label>
          <input
            v-model.number="carData.mileage"
            type="number"
            placeholder="e.g., 50000"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
            min="0"
          />
        </div>
        <!-- License Plate -->
        <div class="form-group animate-form-item" style="animation-delay: 0.75s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-id-card text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'หมายเลขทะเบียน' : 'License Plate' }}
          </label>
          <input
            v-model="carData.licensePlate"
            type="text"
            placeholder="ABC 1234"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all"
          />
        </div>
        <!-- Description -->
        <div class="form-group animate-form-item" style="animation-delay: 0.8s">
          <label class="block text-gray-300 font-semibold mb-2">
            <i class="fas fa-align-left text-red-500 mr-2"></i>{{ currentLanguage === 'th' ? 'คำอธิบาย' : 'Description' }}
          </label>
          <textarea
            v-model="carData.description"
            placeholder="Describe your car in detail..."
            rows="4"
            class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-xl text-white focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/50 transition-all resize-none"
          ></textarea>
        </div>
        <!-- Image Upload -->
        <div class="form-group animate-form-item" style="animation-delay: 0.85s">
          <label class="flex items-center gap-2 text-gray-300 font-semibold mb-3">
            <i class="fas fa-image text-red-500 text-lg"></i>{{ currentLanguage === 'th' ? 'อัปโหลดรูปภาพ' : 'Upload Images' }}
          </label>
          <label class="flex flex-col items-center justify-center w-full px-4 py-8 border-2 border-dashed border-gray-700 rounded-xl cursor-pointer hover:border-red-500 hover:bg-red-600/10 transition-all group bg-gray-800/50">
            <div class="text-center">
              <i class="fas fa-cloud-upload-alt text-4xl text-gray-500 group-hover:text-red-500 transition-colors mb-3"></i>
              <p class="text-gray-300 font-semibold">{{ currentLanguage === 'th' ? 'คลิกเพื่ออัปโหลดรูปภาพ' : 'Click to upload images' }}</p>
              <p class="text-gray-500 text-sm mt-1">PNG, JPG up to 10MB each</p>
            </div>
            <input
              type="file"
              multiple
              accept="image/*"
              class="hidden"
              @change="onFilesSelected"
            />
          </label>
        </div>
        <!-- Image Previews -->
        <div v-if="previewImages.length > 0" class="form-group animate-form-item" style="animation-delay: 0.9s">
          <div class="flex items-center gap-2 mb-3">
            <i class="fas fa-check-circle text-green-500"></i>
            <p class="text-gray-300 font-semibold">Preview Images ({{ previewImages.length }})</p>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div
              v-for="(image, index) in previewImages"
              :key="index"
              class="relative group/image rounded-lg overflow-hidden border-2 border-gray-700 hover:border-red-500 transition-all shadow-lg"
            >
              <img :src="image" :alt="`Preview ${index}`" class="w-full h-32 object-cover group-hover/image:scale-110 transition-transform duration-300" />
              <div class="absolute inset-0 bg-black/0 group-hover/image:bg-black/50 transition-all duration-300 flex items-center justify-center">
                <button
                  type="button"
                  @click="removeImage(index)"
                  class="bg-red-600 hover:bg-red-700 text-white rounded-full w-10 h-10 flex items-center justify-center opacity-0 group-hover/image:opacity-100 transition-opacity transform hover:scale-110"
                >
                  <i class="fas fa-trash text-sm"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-bold py-4 px-6 rounded-xl transition-all transform hover:scale-105 duration-200 submitBtn animate-form-item shadow-lg hover:shadow-red-600/50 flex items-center justify-center gap-2 text-lg"
          id="submitBtn"
          style="animation-delay: 0.95s"
        >
          <i class="fas fa-upload"></i>{{ currentLanguage === 'th' ? 'โพสต์ประกาศรถ' : 'Post Car Listing' }}
        </button>
      </form>
    </div>

    <!-- Success Modal -->
    <SuccessModal
      :show="showSuccessModal"
      title="Car Post Completed!"
      message="Your car has been successfully registered."
      icon=""
      :duration="3"
      @close="handleSuccessClose"
    />

    <!-- Brand Warning Modal -->
    <teleport to="body">
      <transition name="modal-fade">
        <div v-if="showBrandWarningModal" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/70 backdrop-blur-sm" @click="showBrandWarningModal = false">
          <div class="bg-gradient-to-br from-gray-900/90 via-gray-900/90 to-gray-950/90 backdrop-blur-xl rounded-3xl p-10 max-w-md w-full mx-4 animate-warning-pop border border-red-500/30 shadow-2xl" @click.stop>
            <!-- Warning Icon -->
            <div class="flex justify-center mb-6">
              <div class="relative">
                <div class="absolute inset-0 bg-gradient-to-r from-red-600/20 to-orange-600/20 rounded-full blur-2xl"></div>
                <div class="relative animate-warning-icon text-7xl">
                  ⚠️
                </div>
              </div>
            </div>

            <!-- Title -->
            <h2 class="text-2xl font-extrabold text-white text-center mb-3 bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
              {{ currentLanguage === 'th' ? 'แบรนด์ไม่ถูกต้อง' : 'Invalid Brand' }}
            </h2>

            <!-- Message -->
            <p class="text-gray-300 text-center mb-6 leading-relaxed">
              The brand <span class="text-red-400 font-bold">"{{ carData.brand }}"</span> does not match our database.
            </p>

            <!-- Instructions -->
            <div class="bg-red-600/10 border border-red-500/30 rounded-xl p-4 mb-6">
              <p class="text-gray-300 text-sm font-semibold flex items-start gap-2">
                <i class="fas fa-lightbulb text-yellow-500 mt-1 flex-shrink-0"></i>
                <span>{{ currentLanguage === 'th' ? 'กรุณาเลือกแบรนด์จากข้อเสนอหรือพิมพ์เพื่อให้ตรงกัน' : 'Please select a brand from the suggestions or type to match exactly.' }}</span>
              </p>
            </div>

            <!-- Action Button - Removed, click anywhere to close -->
            <div class="text-center text-gray-400 text-sm">
              <p class="flex items-center justify-center gap-2">
                <i class="fas fa-mouse text-gray-500"></i>
                <span>{{ currentLanguage === 'th' ? 'กลับไปแก้ไข' : 'Go Back & Fix' }}</span>
              </p>
            </div>

            <!-- Decorative Elements -->
            <div class="mt-6 flex items-center justify-center gap-3 opacity-50">
              <div class="w-8 h-0.5 bg-gradient-to-r from-transparent to-red-500 rounded"></div>
              <i class="fas fa-exclamation text-red-500 text-xs"></i>
              <div class="w-8 h-0.5 bg-gradient-to-l from-transparent to-red-500 rounded"></div>
            </div>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Beams from '~/components/Beams.vue'
import { useLanguage } from '~/composables/useLanguage'

const router = useRouter()
const { t, currentLanguage } = useLanguage()

const carData = ref({
  vehicleType: '',
  brand: '',
  model: '',
  color: '',
  year: new Date().getFullYear(),
  price: '',
  licensePlate: '',
  description: '',
  fuelType: '',
  transmission: '',
  carType: '',
  mileage: '',
  gasSystem: '',
  engineSize: '',
  mpvSize: '',
  convertibleTop: '',
  convertibleSeats: '',
  vanType: '',
  suvSeats: '',
  pickupCab: '',
  pickupBodyType: ''
})
const previewImages = ref([])
const sellerName = ref('')
const showSuccessModal = ref(false)
const showBrandWarningModal = ref(false)
const currentYear = new Date().getFullYear()
const isBrandInvalid = ref(false)

// Car brands list
const carBrands = [
  'Audi', 'BMW', 'Ford', 'Honda', 'Hyundai', 'Kia', 'Lexus', 'Mazda', 'Mercedes-Benz',
  'Mitsubishi', 'Nissan', 'Subaru', 'Toyota', 'Volkswagen', 'Volvo', 'Chevrolet',
  'Jeep', 'Ram', 'Tesla', 'Porsche', 'Ferrari', 'Lamborghini', 'Rolls-Royce',
  'Bentley', 'Bugatti', 'Pagani', 'Koenigsegg', 'McLaren', 'Jaguar', 'Alfa Romeo',
  'Fiat', 'Peugeot', 'Renault', 'Citroen', 'SEAT', 'Skoda', 'Suzuki', 'Daihatsu',
  'Isuzu', 'Geely', 'BYD', 'Chery', 'GAC Aion', 'Li Auto', 'NIO', 'XPeng', 'BrydRider',
  // ✅ Motorcycle Brands
  'Honda', 'Yamaha', 'Suzuki', 'Kawasaki', 'Ducati', 'KTM', 'Harley-Davidson',
  'BMW', 'Royal Enfield', 'Triumph', 'Aprilia', 'MV Agusta', 'Husqvarna',
  'Bajaj', 'Hero', 'TVS', 'Mahindra', 'Piaggio', 'Vespa', 'Lamborghini Motorcycle',
  // ✅ Bike Brands
  'Trek', 'Specialized', 'Giant', 'Cannondale', 'Scott', 'Cube', 'Focus',
  'Merida', 'Kona', 'Santa Cruz', 'YT Industries', 'Transition', 'Evil Bikes',
  'Pivot', 'Ibis', 'Yeti', 'Trek', 'Felt', 'Diamondback', 'Huffy'
]

const filteredBrands = ref([])
const showBrandSuggestions = ref(false)

const filterBrands = () => {
  const input = carData.value.brand.toLowerCase()
  if (input.length > 0) {
    filteredBrands.value = carBrands.filter(brand =>
      brand.toLowerCase().includes(input)
    )
    showBrandSuggestions.value = true
  } else {
    showBrandSuggestions.value = false
  }
}

const selectBrand = (brand) => {
  carData.value.brand = brand
  showBrandSuggestions.value = false
  filteredBrands.value = []
}

// Watch for brand validation
watch(() => carData.value.brand, (newBrand) => {
  if (newBrand && newBrand.length > 0) {
    // ✅ Check if brand matches exactly with database
    const isValidBrand = carBrands.includes(newBrand)
    isBrandInvalid.value = !isValidBrand
  } else {
    isBrandInvalid.value = false
  }
})
onMounted(() => {
  if (process.client) {
    sellerName.value = localStorage.getItem('username') || 'Seller'
  }
})
const onFilesSelected = (event) => {
  const files = event.target.files
  if (files) {
    Array.from(files).forEach((file) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        previewImages.value.push(e.target.result)
      }
      reader.readAsDataURL(file)
    })
  }
}
const removeImage = (index) => {
  previewImages.value.splice(index, 1)
}
const handleSuccessClose = () => {
  showSuccessModal.value = false
  router.push('/dashboard')
}
const handleSubmit = async () => {
  // ✅ Validate brand matches database
  if (!carData.value.brand || !carBrands.includes(carData.value.brand)) {
    isBrandInvalid.value = true
    showBrandWarningModal.value = true
    return
  }
  
  isBrandInvalid.value = false

  try {
    // ... rest of submission code
    // Validate required fields
    if (!carData.value.brand || !carData.value.model || !carData.value.year || !carData.value.price) {
      alert('Please fill in all required fields')
      return
    }
    const token = localStorage.getItem('token')
    if (!token) {
      alert('You must be logged in to post a car')
      return
    }
    // Show loading animation
    const submitBtn = document.getElementById('submitBtn')
    if (submitBtn) {
      submitBtn.classList.add('animate-post-loading')
      submitBtn.disabled = true
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Posting...'
    }
    // Create payload with car data including new fields
    const payload = {
      vehicle_type: carData.value.vehicleType,
      brand: carData.value.brand,
      model: carData.value.model,
      color: carData.value.color,
      year: parseInt(carData.value.year),
      licensePlate: carData.value.licensePlate,
      description: carData.value.description,
      price: parseFloat(carData.value.price),
      fuel_type: carData.value.fuelType,
      transmission: carData.value.transmission,
      car_type: carData.value.carType,
      mileage: parseInt(carData.value.mileage || 0),
      gas_system: carData.value.gasSystem || 'None',
      engine_size: carData.value.engineSize,
      drive_system: carData.value.driveSystem,
      mpv_size: carData.value.mpvSize,
      convertible_top: carData.value.convertibleTop,
      convertible_seats: carData.value.convertibleSeats,
      van_type: carData.value.vanType,
      suv_seats: carData.value.suvSeats,
      pickup_cab: carData.value.pickupCab,
      pickup_body_type: carData.value.pickupBodyType,
      images: previewImages.value
    }
    // Send to backend using /api proxy
    const response = await fetch('http://localhost:5000/api/cars', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    const data = await response.json()
    
    if (response.ok && data.success) {
      // Show success animation
      if (submitBtn) {
        submitBtn.classList.remove('animate-post-loading')
        submitBtn.classList.add('animate-post-success')
        submitBtn.innerHTML = '<i class="fas fa-check mr-2"></i>Posted Successfully!'
      }
      setTimeout(() => {
        showSuccessModal.value = true
      }, 500)
    } else {
      if (submitBtn) {
        submitBtn.classList.remove('animate-post-loading')
        submitBtn.disabled = false
        submitBtn.innerHTML = '<i class="fas fa-upload mr-2"></i>Post Car Listing'
      }
      alert('Error: ' + (data.message || data.error || 'Failed to post car'))
    }
  } catch (error) {
    console.error('Error posting car:', error)
    const submitBtn = document.getElementById('submitBtn')
    if (submitBtn) {
      submitBtn.classList.remove('animate-post-loading')
      submitBtn.disabled = false
      submitBtn.innerHTML = '<i class="fas fa-upload mr-2"></i>Post Car Listing'
    }
    alert('Failed to post car: ' + error.message)
  }
}
</script>
<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

.animate-slide-down {
  animation: slideDown 0.6s ease-out;
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out;
}

.animate-form-item {
  animation: formItem 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes formItem {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes postLoading {
  0% {
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
  50% {
    background: linear-gradient(to right, #f97316, #ea580c);
  }
  100% {
    background: linear-gradient(to right, #dc2626, #b91c1c);
  }
}

@keyframes postSuccess {
  0% {
    background: linear-gradient(to right, #dc2626, #b91c1c);
    transform: scale(1);
  }
  50% {
    background: linear-gradient(to right, #22c55e, #16a34a);
    transform: scale(1.05);
  }
  100% {
    background: #22c55e;
    transform: scale(1);
  }
}

.animate-post-loading {
  animation: postLoading 0.6s ease-in-out infinite !important;
}

.animate-post-success {
  animation: postSuccess 1s ease-in-out forwards !important;
  background-color: #22c55e !important;
}

/* Form Group Styling */
.form-group {
  transition: all 0.3s ease;
}

.form-group:hover {
  transform: translateY(-2px);
}

/* Input Focus Effects */
input:focus,
select:focus,
textarea:focus {
  background-color: rgba(30, 41, 59, 0.8) !important;
}

/* Improved Select Styling */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23ef4444' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  padding-right: 2.5rem;
}

/* Textarea Styling */
textarea {
  font-family: 'Inter', sans-serif;
  resize: none;
}

textarea:focus {
  resize: vertical;
}

/* Badge Animation */
@keyframes badgeFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.badge-float {
  animation: badgeFloat 3s ease-in-out infinite;
}

/* Warning Modal Animation */
@keyframes warningPop {
  0% {
    opacity: 0;
    transform: scale(0.5) rotateZ(-15deg);
  }
  50% {
    transform: scale(1.1) rotateZ(5deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotateZ(0deg);
  }
}

@keyframes warningIcon {
  0% {
    opacity: 0;
    transform: scale(0) rotate(-180deg);
  }
  50% {
    transform: scale(1.3) rotate(10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

@keyframes warningShake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.animate-warning-pop {
  animation: warningPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-warning-icon {
  animation: warningIcon 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s both;
}

/* Modal Fade Transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
