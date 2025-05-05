// Home.vue (Fixed Version)
<template>
  <div class="home">
    <div class="navbar bg-dark text-white py-2 mb-4" v-if="isLoggedIn">
      <div class="container">
        <div class="d-flex justify-content-between align-items-center w-100">
          <router-link to="/" class="navbar-brand text-warning fw-bold">
            <span class="me-1">J</span> Jam+Date
          </router-link>
          <div>
            <button @click="logout" class="btn btn-link text-white text-decoration-none">Logout</button>
            <button class="btn btn-secondary rounded-circle ms-2 btn-sm">
              <i class="fas fa-lock"></i>
            </button>
            <button class="btn btn-secondary rounded-circle ms-2 btn-sm">
              <i class="fas fa-user"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="jumbotron text-center p-5 mb-4" v-if="!isLoggedIn">
      <h1 class="display-4">Jam-Date</h1>
      <p class="lead">Finding your perfect match in Jamaica</p>
      <p>Place people with people in Jamrock</p>
      
      <div class="mt-4">
        <router-link to="/register" class="btn btn-primary btn-lg mx-2">Register</router-link>
        <router-link to="/login" class="btn btn-success btn-lg mx-2">Login</router-link>
      </div>
    </div>
    
    <div class="container" v-if="isLoggedIn">
 
      <div class="bg-warning rounded mb-4 py-2 px-3">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <router-link to="/" class="btn btn-warning">My</router-link>
            <router-link :to="`/users/${userId}`" class="btn btn-warning ms-2">My Profile</router-link>
          </div>
          <div>
            <button @click="logout" class="btn btn-warning me-2">Logout</button>
            <router-link to="/profiles/favourites" class="btn btn-danger">Show Report</router-link>
          </div>
        </div>
      </div>

    
      <search-form @search="handleSearch" />

      
      <div class="d-flex justify-content-center mb-4">
        <button @click="filterBy('name')" class="btn btn-light mx-1">Name</button>
        <button @click="filterBy('birth')" class="btn btn-light mx-1">Birth</button>
        <button @click="filterBy('sex')" class="btn btn-light mx-1">Sex</button>
        <button @click="filterBy('race')" class="btn btn-light mx-1">Race</button>
      </div>

     
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <div v-if="isSearching">
          <h3>Search Results</h3>
          
          <div v-if="searchResults.length === 0" class="alert alert-info">
            No profiles found matching your search criteria.
          </div>
          
          <div v-else class="row">
            <div 
              v-for="result in searchResults" 
              :key="result.profile.id" 
              class="col-md-4 mb-4"
            >
              <profile-card 
                :profile="result.profile" 
                :user-name="result.userName" 
                :user-photo="result.userPhoto"
                :is-favorited="result.isFavorited"
                @favorite-toggled="updateFavorites"
              />
            </div>
          </div>
        </div>
        
        <div v-else>
          <h3>Recently Added Profiles</h3>
          
          <div v-if="recentProfiles.length === 0" class="alert alert-info">
            No profiles available at the moment.
          </div>
          
          <div v-else class="row">
            <div 
              v-for="profile in recentProfiles" 
              :key="profile.profile.id" 
              class="col-md-4 mb-4"
            >
              <profile-card 
                :profile="profile.profile" 
                :user-name="profile.userName" 
                :user-photo="profile.userPhoto"
                :is-favorited="profile.isFavorited"
                @favorite-toggled="updateFavorites"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchForm from '@/components/SearchForm.vue'
import ProfileCard from '@/components/ProfileCard.vue'
import apiService from '@/services/api'

export default {
  name: 'Home',
  components: {
    SearchForm,
    ProfileCard
  },
  data() {
    return {
      isLoggedIn: false,
      userId: null,
      loading: false,
      recentProfiles: [],
      searchResults: [],
      isSearching: false,
      userFavorites: [],
      currentFilter: 'name'
    }
  },
  created() {
    this.checkAuth()
    
    if (this.isLoggedIn) {
      this.loadRecentProfiles()
      this.loadUserFavorites()
    }
    

    window.addEventListener('refresh-profiles', this.loadRecentProfiles)
  },
  mounted() {
    if (this.isLoggedIn) {
      this.loadRecentProfiles()
    }
  },
  activated() {
    if (this.isLoggedIn) {
      this.loadRecentProfiles()
    }
  },
  beforeUnmount() {
    window.removeEventListener('refresh-profiles', this.loadRecentProfiles)
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('jwt')
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      this.isLoggedIn = !!token
      this.userId = user.id || null
    },
    
    async loadRecentProfiles() {
      this.loading = true
      console.log("Loading recent profiles...")
      
      try {
        const profilesResponse = await apiService.getProfiles(true)
        console.log("Profiles response:", profilesResponse.data)
        
        const profiles = profilesResponse.data.profiles
        
     
        if (!profiles || profiles.length === 0) {
          console.log("No profiles found")
          this.recentProfiles = []
          this.loading = false
          return
        }
        
       
        profiles.sort((a, b) => b.id - a.id)
        
       
        const recentProfiles = profiles.slice(0, 3)
        console.log("Recent profiles:", recentProfiles)
        
   
        this.recentProfiles = await Promise.all(
          recentProfiles.map(async profile => {
            try {
              const userResponse = await apiService.getUser(profile.user_id_fk)
              const user = userResponse.data.user
              
              return {
                profile,
                userName: user.name,
                userPhoto: user.photo || 'https://via.placeholder.com/150',
                isFavorited: this.userFavorites.includes(profile.user_id_fk)
              }
            } catch (error) {
              console.error(`Error getting user for profile ${profile.id}:`, error)
              return {
                profile,
                userName: "Unknown User",
                userPhoto: 'https://via.placeholder.com/150',
                isFavorited: false
              }
            }
          })
        )
        
        console.log("Processed recent profiles:", this.recentProfiles)
      } catch (error) {
        console.error('Error loading recent profiles:', error)
        this.recentProfiles = []
      } finally {
        this.loading = false
      }
    },
    
    async loadUserFavorites() {
      try {
        const response = await apiService.getUserFavourites(this.userId)
        this.userFavorites = response.data.favourites.map(fav => fav.id)
      } catch (error) {
        console.error('Error loading user favorites:', error)
        this.userFavorites = []
      }
    },
    
    filterBy(type) {
      this.currentFilter = type
    },
    
    async handleSearch(params) {
      this.loading = true
      this.isSearching = true
      
      try {
        console.log("Searching with params:", params)
        const response = await apiService.searchProfiles(params)
        const results = response.data.results
        
       
        this.searchResults = await Promise.all(
          results.map(async profile => {
            try {
              const userResponse = await apiService.getUser(profile.user_id_fk)
              const user = userResponse.data.user
              
              return {
                profile,
                userName: user.name,
                userPhoto: user.photo || 'https://via.placeholder.com/150',
                isFavorited: this.userFavorites.includes(profile.user_id_fk)
              }
            } catch (error) {
              console.error(`Error getting user for profile ${profile.id}:`, error)
              return {
                profile,
                userName: "Unknown User",
                userPhoto: 'https://via.placeholder.com/150',
                isFavorited: false
              }
            }
          })
        )
      } catch (error) {
        console.error('Error searching profiles:', error)
        this.searchResults = []
      } finally {
        this.loading = false
      }
    },
    
    updateFavorites(userId) {
      if (!this.userFavorites.includes(userId)) {
        this.userFavorites.push(userId)
      }
      
      this.recentProfiles.forEach(profile => {
        if (profile.profile.user_id_fk === userId) {
          profile.isFavorited = true
        }
      })
      
      this.searchResults.forEach(result => {
        if (result.profile.user_id_fk === userId) {
          result.isFavorited = true
        }
      })
    },
    
    async logout() {
      try {
        await apiService.logout()
        localStorage.removeItem('jwt')
        localStorage.removeItem('user')
        this.$router.push('/login')
      } catch (error) {
        console.error('Error logging out:', error)
      }
    }
  }
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
}

.btn-warning {
  background-color: #FCD116;
  border-color: #FCD116;
}
</style>