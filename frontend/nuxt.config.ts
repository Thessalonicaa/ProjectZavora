export default defineNuxtConfig({
  ssr: false,
  
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:5000'
    }
  },

  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  nitro: {
    compatibilityDate: '2025-08-22'
  },

  // เพิ่มการตั้งค่า pages
  pages: true,

  // เพิ่ม modules ที่จำเป็น
  modules: ['@nuxtjs/tailwindcss', 'reka-ui'],

  // ✅ Auth middleware disabled - using route-specific protection instead
  // router: {
  //   middleware: ['auth']
  // },

  // กำหนดค่า build
  build: {
    transpile: ['vue-router']

  }
})