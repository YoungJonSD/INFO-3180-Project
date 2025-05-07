// router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import UserProfile from '../views/UserProfile.vue'
import NewProfile from '../views/NewProfile.vue'
import ProfileDetails from '../views/ProfileDetails.vue'
import FavouritesReport from '../views/FavouritesReport.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('../views/Logout.vue')
  },
  {
    path: '/users/:user_id',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/new',
    name: 'NewProfile',
    component: NewProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:profile_id',
    name: 'ProfileDetails',
    component: ProfileDetails,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/favourites',
    name: 'FavouritesReport',
    component: FavouritesReport,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  // Fix here: Using an empty string instead of process.env.BASE_URL
  history: createWebHashHistory(''),
  routes
})

// Navigation guard for authenticated routes
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const isAuthenticated = localStorage.getItem('jwt')
  
  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router