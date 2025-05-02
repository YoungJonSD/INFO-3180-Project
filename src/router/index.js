import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import NewProfile from '../views/NewProfile.vue'
import ProfileDetails from '../views/ProfileDetails.vue'
import MyProfile from '../views/MyProfile.vue'
import Favourites from '../views/Favourites.vue'
import MatchReport  from '../views/MatchReport.vue'


const routes = [
  { path: '/register', name: 'Register', component: Register },
  { path: '/login', name: 'Login', component: Login },
  { path: '/profiles/new', name: 'NewProfile', component: NewProfile },
  { path: '/profiles/:profile_id', name: 'ProfileDetails', component: ProfileDetails },
  { path: '/', name: 'Home', component: Home },
  { path: '/users/:user_id', name: 'MyProfile', component: MyProfile },
  { path: '/profiles/:profile_id/matches', name: 'MatchReport', component: MatchReport },
  { path: '/profiles/favourites', name: 'Favourites', component: Favourites }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
