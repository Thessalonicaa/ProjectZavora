import { ref, computed } from 'vue'

// ✅ Global reactive language state
const currentLanguage = ref('th')

// ✅ Set initial language from localStorage
if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('language') || 'th'
  currentLanguage.value = saved
}

// ข้อมูลการแปลทั้งหมด
const translations = {
  th: {
    // Navbar
    'navbar.searchPlaceholder': 'ค้นหารถยนต์...',
    'navbar.messages': 'ข้อความ',
    'navbar.cars': 'รถยนต์',
    'navbar.sellYourCar': 'ขายรถของคุณ',
    'navbar.logout': 'ออกจากระบบ',
    'navbar.menu': 'เมนู',
    'navbar.home': 'หน้าแรก',

    // CarList
    'carlist.title': 'รถยนต์ที่มี',
    'carlist.noResults': 'ไม่พบรถยนต์ที่ตรงกับเกณฑ์',
    'carlist.viewDetails': 'ดูรายละเอียด',
    'carlist.available': 'พร้อมขาย',

    // Index/Home
    'index.featuredCars': 'รถยนต์พิเศษ',
    'index.popularBrands': 'แบรนด์ยอดนิยม',
    'index.exploreManufacturers': 'สำรวจรถยนต์จากผู้ผลิตชั้นนำ',
    'index.price': 'ราคา',
    'index.view': 'ดู',

    // Messages
    'messages.title': 'แชทกับผู้ซื้อและผู้ขาย',
    'messages.noConversations': 'ยังไม่มีการสนทนา',
    'messages.startChatting': 'เริ่มแชทกับผู้ขาย!',
    'messages.selectConversation': 'เลือกการสนทนา',
    'messages.chooseToChat': 'เลือกจากการสนทนาของคุณเพื่อเริ่มแชท',
    'messages.deleteChat': 'ลบแชท',
    'messages.deleteConfirm': 'ลบการสนทนา?',
    'messages.send': 'ส่ง',
    'messages.typeMessage': 'พิมพ์ข้อความของคุณ...',
    'messages.noMessages': 'ไม่มีข้อความ',
    'messages.contactSeller': 'ติดต่อผู้ขาย',

    // Profile
    'profile.accountInfo': 'ข้อมูลบัญชี',
    'profile.username': 'ชื่อผู้ใช้',
    'profile.accountType': 'ประเภทบัญชี',
    'profile.memberSince': 'สมาชิกตั้งแต่',
    'profile.businessInfo': 'ข้อมูลธุรกิจ',
    'profile.businessName': 'ชื่อธุรกิจ',
    'profile.email': 'อีเมล',
    'profile.phone': 'โทรศัพท์',
    'profile.address': 'ที่อยู่',
    'profile.activity': 'กิจกรรม',
    'profile.lastActive': 'ออนไลน์ล่าสุด',
    'profile.actions': 'การดำเนินการ',
    'profile.saveChanges': 'บันทึกการเปลี่ยนแปลง',
    'profile.backToDashboard': 'กลับไปแดชบอร์ด',
    'profile.carsForSale': 'รถสำหรับขาย',
    'profile.noCarsListed': 'ยังไม่มีรถที่ลงขาย',
    'profile.updateSuccess': 'อัปเดตโปรไฟล์สำเร็จ',

    // Calculator
    'calculator.title': 'เครื่องคำนวณการผ่อน',
    'calculator.subtitle': 'คำนวณการชำระรายเดือนของคุณได้อย่างง่ายดาย',
    'calculator.cartItems': 'รายการในการซื้อ',
    'calculator.totalPrice': 'ราคารวม',
    'calculator.downPayment': 'เงินดาวน์',
    'calculator.interestRate': 'อัตราดอก',
    'calculator.duration': 'ระยะเวลา (เดือน)',
    'calculator.calculate': 'คำนวณ',
    'calculator.result': 'ผลลัพธ์',
    'calculator.monthlyPayment': 'ค่างวดต่อเดือน',
    'calculator.remaining': 'ยอดคงเหลือ',
    'calculator.totalInterest': 'ดอกเบี้ยรวม',
    'calculator.totalPayment': 'ยอดชำระทั้งหมด',
    'calculator.months': 'เดือน',
    'calculator.moreCards': 'ดูรถอื่นๆ',

    // PostCar
    'postcar.title': 'ลงขายรถของคุณ',
    'postcar.subtitle': 'แบ่งปันรถของคุณกับผู้ซื้อนับพันคน',
    'postcar.sellerAccount': 'บัญชีผู้ขาย',
    'postcar.vehicleInfo': 'ข้อมูลรถยนต์',
    'postcar.vehicleType': 'ประเภทรถ',
    'postcar.brand': 'ยี่ห้อ',
    'postcar.model': 'รุ่น',
    'postcar.color': 'สี',
    'postcar.year': 'ปี',
    'postcar.price': 'ราคา',
    'postcar.fuelType': 'ประเภทเชื้อเพลิง',
    'postcar.gasSystem': 'ระบบแก๊ส',
    'postcar.engineSize': 'ขนาดเครื่องยนต์',
    'postcar.transmission': 'การส่งกำลัง',
    'postcar.driveSystem': 'ระบบขับเคลื่อน',
    'postcar.carType': 'ประเภทรถ',
    'postcar.mileage': 'เลขไมล์',
    'postcar.licensePlate': 'เลขทะเบียน',
    'postcar.description': 'รายละเอียด',
    'postcar.uploadImages': 'อัปโหลดรูปภาพ',
    'postcar.postListing': 'ลงประกาศขายรถ',
    'postcar.success': 'ลงขายเสร็จสิ้น!',

    // Car Details
    'car.specifications': 'ข้อมูลจำเพาะ',
    'car.carType': 'ประเภทรถ',
    'car.color': 'สี',
    'car.mileage': 'เลขไมล์',
    'car.contactSeller': 'ติดต่อผู้ขาย',
    'car.year': 'ปี',
    'car.fuel': 'เชื้อเพลิง',
    'car.price': 'ราคา',

    // Dashboard
    'dashboard.welcome': 'ยินดีต้อนรับ',
    'dashboard.carsListed': 'รถที่ลงขาย',
    'dashboard.myListings': 'รายการของฉัน',
    'dashboard.postCar': 'ลงขายรถ',
    'dashboard.noListings': 'ยังไม่มีรถที่ลงขาย',

    // MyListings
    'mylistings.title': 'รายการรถของฉัน / My Car Listings',
    'mylistings.subtitle': 'จัดการและติดตามรายการรถของคุณ / Manage and Monitor Your Listings',
    'mylistings.noListings': 'ยังไม่มีรถที่ลงทะเบียน / No Cars Listed Yet',
    'mylistings.postCar': 'ลงประกาศขายรถ / Post a Car for Sale',
    'mylistings.view': 'ดู / View',
    'mylistings.markSold': 'ทำเครื่องหมายว่าเป็นขายแล้ว / Mark Sold',
    'mylistings.reactivate': 'ทำเครื่องหมายว่าเป็นเปิดใช้งาน / Reactivate',
    'mylistings.delete': 'ลบ / Delete',
    'mylistings.processing': 'กำลังประมวลผล... / Processing...',
    'mylistings.deleteConfirm': 'ลบรายการ? / Delete Listing?',
    'mylistings.deleteMessage': 'คุณแน่ใจหรือไม่ว่าต้องการลบรายการนี้? / Are you sure you want to delete this listing?',
    'mylistings.cancel': 'ยกเลิก / Cancel',
    'mylistings.deleting': 'กำลังลบ... / Deleting...',
    'mylistings.active': 'ว่าง / Active',
    'mylistings.sold': 'ขายแล้ว / Sold',
    'mylistings.price': 'ราคา / Price',
    'mylistings.license': 'ทะเบียน: / License: ',

    // Brand Page
    'brand.browseVehicles': 'เรียกรถยนต์ / Browse Vehicles',
    'brand.filterVehicles': 'กรองและค้นหารถยนต์ที่สมบูรณ์แบบของคุณ / Filter and find your perfect',
    'brand.searchPlaceholder': 'ค้นหาตามรุ่น สี ประเภทเชื้อเพลิง... / Search by model, color, fuel type...',
    'brand.totalCars': 'จำนวนรถทั้งหมด / Total Cars',
    'brand.minPrice': 'ราคาต่ำสุด / Min Price',
    'brand.maxPrice': 'ราคาสูงสุด / Max Price',
    'brand.allFuelTypes': 'ประเภทเชื้อเพลิงทั้งหมด / All Fuel Types',
    'brand.petrol': 'เบนซิน / Petrol',
    'brand.diesel': 'ดีเซล / Diesel',
    'brand.hybrid': 'ไฮบริด / Hybrid',
    'brand.electric': 'ไฟฟ้า / Electric',
    'brand.allGasSystems': 'ระบบแก๊สทั้งหมด / All Gas Systems',
    'brand.allDriveSystems': 'ระบบขับเคลื่อนทั้งหมด / All Drive Systems',
    'brand.allTransmissions': 'ประเภทเกียร์ทั้งหมด / All Transmissions',
    'brand.automatic': 'อัตโนมัติ / Automatic',
    'brand.manual': 'ธรรมดา / Manual',
    'brand.semiAutomatic': 'กึ่งอัตโนมัติ / Semi-Automatic',
    'brand.allCarTypes': 'ประเภทรถทั้งหมด / All Car Types',
    'brand.allEngineSizes': 'ขนาดเครื่องยนต์ทั้งหมด / All Engine Sizes',
    'brand.minPriceLabel': 'ราคาเริ่มต้น: / Min Price:',
    'brand.maxPriceLabel': 'ราคาสูงสุด: / Max Price:',
    'brand.allColors': 'สีทั้งหมด / All Colors',
    'brand.noResults': 'ไม่พบ / No',
    'brand.cars': 'รถ / cars',
    'brand.matching': 'found matching your criteria',
    'brand.estPrice': 'ราคาโดยประมาณ / Est. Price',
    'brand.viewDetails': 'ดูรายละเอียด / View Details',
  },
  en: {
    // Navbar
    'navbar.searchPlaceholder': 'Search cars...',
    'navbar.messages': 'Messages',
    'navbar.cars': 'Cars',
    'navbar.sellYourCar': 'Sell Your Car',
    'navbar.logout': 'Logout',
    'navbar.menu': 'Menu',
    'navbar.home': 'Home',

    // CarList
    'carlist.title': 'Available Cars',
    'carlist.noResults': 'No cars found matching your criteria',
    'carlist.viewDetails': 'View Details',
    'carlist.available': 'Available',

    // Index/Home
    'index.featuredCars': 'Featured Cars',
    'index.popularBrands': 'Popular Brands',
    'index.exploreManufacturers': 'Explore vehicles from top manufacturers',
    'index.price': 'Price',
    'index.view': 'View',

    // Messages
    'messages.title': 'Chat with Buyers and Sellers',
    'messages.noConversations': 'No conversations yet',
    'messages.startChatting': 'Start chatting with sellers!',
    'messages.selectConversation': 'Select a conversation',
    'messages.chooseToChat': 'Choose from your conversations to start chatting',
    'messages.deleteChat': 'Delete Chat',
    'messages.deleteConfirm': 'Delete conversation?',
    'messages.send': 'Send',
    'messages.typeMessage': 'Type your message...',
    'messages.noMessages': 'No messages',
    'messages.contactSeller': 'Contact Seller',

    // Profile
    'profile.accountInfo': 'Account Info',
    'profile.username': 'Username',
    'profile.accountType': 'Account Type',
    'profile.memberSince': 'Member Since',
    'profile.businessInfo': 'Business Info',
    'profile.businessName': 'Business Name',
    'profile.email': 'Email',
    'profile.phone': 'Phone',
    'profile.address': 'Address',
    'profile.activity': 'Activity',
    'profile.lastActive': 'Last Active',
    'profile.actions': 'Actions',
    'profile.saveChanges': 'Save Changes',
    'profile.backToDashboard': 'Back to Dashboard',
    'profile.carsForSale': 'Cars for Sale',
    'profile.noCarsListed': 'No cars listed yet',
    'profile.updateSuccess': 'Profile Updated!',

    // Calculator
    'calculator.title': 'Installment Calculator',
    'calculator.subtitle': 'Calculate your monthly payment easily',
    'calculator.cartItems': 'Cart Items',
    'calculator.totalPrice': 'Total Price',
    'calculator.downPayment': 'Down Payment',
    'calculator.interestRate': 'Interest Rate',
    'calculator.duration': 'Duration (Months)',
    'calculator.calculate': 'Calculate',
    'calculator.result': 'Result',
    'calculator.monthlyPayment': 'Monthly Payment',
    'calculator.remaining': 'Remaining',
    'calculator.totalInterest': 'Total Interest',
    'calculator.totalPayment': 'Total Payment',
    'calculator.months': 'months',
    'calculator.moreCards': 'More Cars',

    // PostCar
    'postcar.title': 'Post Your Car',
    'postcar.subtitle': 'Share your vehicle with thousands of buyers',
    'postcar.sellerAccount': 'Seller Account',
    'postcar.vehicleInfo': 'Vehicle Information',
    'postcar.vehicleType': 'Vehicle Type',
    'postcar.brand': 'Brand',
    'postcar.model': 'Model',
    'postcar.color': 'Color',
    'postcar.year': 'Year',
    'postcar.price': 'Price',
    'postcar.fuelType': 'Fuel Type',
    'postcar.gasSystem': 'Gas System',
    'postcar.engineSize': 'Engine Size',
    'postcar.transmission': 'Transmission',
    'postcar.driveSystem': 'Drive System',
    'postcar.carType': 'Car Type',
    'postcar.mileage': 'Mileage',
    'postcar.licensePlate': 'License Plate',
    'postcar.description': 'Description',
    'postcar.uploadImages': 'Upload Images',
    'postcar.postListing': 'Post Car Listing',
    'postcar.success': 'Car Posted Successfully!',

    // Car Details
    'car.specifications': 'Specifications',
    'car.carType': 'Car Type',
    'car.color': 'Color',
    'car.mileage': 'Mileage',
    'car.contactSeller': 'Contact Seller',
    'car.year': 'Year',
    'car.fuel': 'Fuel',
    'car.price': 'Price',

    // Dashboard
    'dashboard.welcome': 'Welcome',
    'dashboard.carsListed': 'Cars Listed',
    'dashboard.myListings': 'My Listings',
    'dashboard.postCar': 'Post Car',
    'dashboard.noListings': 'No cars listed yet',

    // MyListings
    'mylistings.title': 'รายการรถของฉัน / My Car Listings',
    'mylistings.subtitle': 'จัดการและติดตามรายการรถของคุณ / Manage and Monitor Your Listings',
    'mylistings.noListings': 'ยังไม่มีรถที่ลงทะเบียน / No Cars Listed Yet',
    'mylistings.postCar': 'ลงประกาศขายรถ / Post a Car for Sale',
    'mylistings.view': 'ดู / View',
    'mylistings.markSold': 'ทำเครื่องหมายว่าเป็นขายแล้ว / Mark Sold',
    'mylistings.reactivate': 'ทำเครื่องหมายว่าเป็นเปิดใช้งาน / Reactivate',
    'mylistings.delete': 'ลบ / Delete',
    'mylistings.processing': 'กำลังประมวลผล... / Processing...',
    'mylistings.deleteConfirm': 'ลบรายการ? / Delete Listing?',
    'mylistings.deleteMessage': 'คุณแน่ใจหรือไม่ว่าต้องการลบรายการนี้? / Are you sure you want to delete this listing?',
    'mylistings.cancel': 'ยกเลิก / Cancel',
    'mylistings.deleting': 'กำลังลบ... / Deleting...',
    'mylistings.active': 'ว่าง / Active',
    'mylistings.sold': 'ขายแล้ว / Sold',
    'mylistings.price': 'ราคา / Price',
    'mylistings.license': 'ทะเบียน: / License: ',

    // Brand Page
    'brand.browseVehicles': 'เรียกรถยนต์ / Browse Vehicles',
    'brand.filterVehicles': 'กรองและค้นหารถยนต์ที่สมบูรณ์แบบของคุณ / Filter and find your perfect',
    'brand.searchPlaceholder': 'ค้นหาตามรุ่น สี ประเภทเชื้อเพลิง... / Search by model, color, fuel type...',
    'brand.totalCars': 'จำนวนรถทั้งหมด / Total Cars',
    'brand.minPrice': 'ราคาต่ำสุด / Min Price',
    'brand.maxPrice': 'ราคาสูงสุด / Max Price',
    'brand.allFuelTypes': 'ประเภทเชื้อเพลิงทั้งหมด / All Fuel Types',
    'brand.petrol': 'เบนซิน / Petrol',
    'brand.diesel': 'ดีเซล / Diesel',
    'brand.hybrid': 'ไฮบริด / Hybrid',
    'brand.electric': 'ไฟฟ้า / Electric',
    'brand.allGasSystems': 'ระบบแก๊สทั้งหมด / All Gas Systems',
    'brand.allDriveSystems': 'ระบบขับเคลื่อนทั้งหมด / All Drive Systems',
    'brand.allTransmissions': 'ประเภทเกียร์ทั้งหมด / All Transmissions',
    'brand.automatic': 'อัตโนมัติ / Automatic',
    'brand.manual': 'ธรรมดา / Manual',
    'brand.semiAutomatic': 'กึ่งอัตโนมัติ / Semi-Automatic',
    'brand.allCarTypes': 'ประเภทรถทั้งหมด / All Car Types',
    'brand.allEngineSizes': 'ขนาดเครื่องยนต์ทั้งหมด / All Engine Sizes',
    'brand.minPriceLabel': 'ราคาเริ่มต้น: / Min Price:',
    'brand.maxPriceLabel': 'ราคาสูงสุด: / Max Price:',
    'brand.allColors': 'สีทั้งหมด / All Colors',
    'brand.noResults': 'ไม่พบ / No',
    'brand.cars': 'รถ / cars',
    'brand.matching': 'found matching your criteria',
    'brand.estPrice': 'ราคาโดยประมาณ / Est. Price',
    'brand.viewDetails': 'ดูรายละเอียด / View Details',
  }
}

export const useLanguage = () => {
  // ✅ Change language and save to localStorage
  const setLanguage = (lang) => {
    if (lang === 'th' || lang === 'en') {
      currentLanguage.value = lang
      if (typeof window !== 'undefined') {
        localStorage.setItem('language', lang)
        // ✅ Notify all components of language change
        window.dispatchEvent(new CustomEvent('language-changed', { detail: { language: lang } }))
      }
      console.log('🌐 Language changed to:', lang)
    }
  }

  // ✅ Get translation by key
  const t = (key) => {
    const keys = key.split('.')
    let translation = translations[currentLanguage.value]
    
    for (const k of keys) {
      if (translation && typeof translation === 'object') {
        translation = translation[k]
      } else {
        return key
      }
    }
    
    return translation || key
  }

  // ✅ Initialize language from localStorage
  const initLanguage = () => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('language') || 'th'
      currentLanguage.value = saved
    }
  }

  return {
    currentLanguage: computed(() => currentLanguage.value),
    setLanguage,
    t,
    initLanguage
  }
}
