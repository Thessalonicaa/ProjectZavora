import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/login.vue'
import Register from '../pages/Register.vue'
import RegisterSeller from '../pages/RegisterSeller.vue'
import CarList from "../Veiws/CarList.vue"
import CarDetail from "../Veiws/CarDetail.vue"


const routes = [
  { 
    path: '/', 
    redirect: to => {
      return localStorage.getItem('token') ? '/cars' : '/login'
    }
  },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/register-seller', component: RegisterSeller },
  { 
    path: "/cars", 
    name: "car-list",
    component: CarList,
    meta: { requiresAuth: true }
  },
  { 
    path: "/cars/:id", 
    name: "car-detail", 
    component: CarDetail, 
    props: true,
    meta: { requiresAuth: true }
  },
  { 
    path: "/brand/:id", 
    name: "brand-detail", 
    component: BrandDetail, 
    props: true,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router