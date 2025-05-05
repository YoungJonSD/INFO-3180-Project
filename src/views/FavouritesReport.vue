<template>
  <div class="favourites-report">
    <h2 class="mb-4">Favorites Report</h2>
    
    <div class="mb-4">
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'top' }"
            href="#" 
            @click.prevent="activeTab = 'top'"
          >
            Top 20 Most Favorited
          </a>
        </li>
        <li class="nav-item">
          <a 
            class="nav-link" 
            :class="{ active: activeTab === 'personal' }"
            href="#" 
            @click.prevent="activeTab = 'personal'"
          >
            Your Favorites
          </a>
        </li>
      </ul>
    </div>
    
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else>
      <div v-if="activeTab === 'top'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3>Top 20 Most Favorited Users</h3>
          
          <div class="btn-group">
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: sortBy === 'count' }"
              @click="sortTopFavorites('count')"
            >
              Popularity
            </button>
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: sortBy === 'name' }"
              @click="sortTopFavorites('name')"
            >
              Name
            </button>
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: sortBy === 'parish' }"
              @click="sortTopFavorites('parish')"
            >
              Parish
            </button>
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: sortBy === 'age' }"
              @click="sortTopFavorites('age')"
            >
              Age
            </button>
          </div>
        </div>
        
        <div v-if="topFavorites.length === 0" class="alert alert-info">
          No favorited users found.
        </div>
        
        <div v-else class="row">
          <div 
            v-for="favorite in topFavorites" 
            :key="favorite.id" 
            class="col-md-3 mb-4"
          >
            <div class="card h-100">
              <img 
                :src="favorite.photo || 'https://via.placeholder.com/150'" 
                alt="Profile Photo" 
                class="card-img-top"
                style="height: 150px; object-fit: cover;"
              />
              <div class="card-body">
                <h5 class="card-title">{{ favorite.name }}</h5>
                <p class="badge bg-success">{{ favorite.fav_count }} Favorites</p>
                
                <div v-if="favorite.parish" class="mt-2">
                  <small class="text-muted">Parish: {{ favorite.parish }}</small>
                </div>
                
                <div v-if="favorite.age" class="mt-2">
                  <small class="text-muted">Age: {{ favorite.age }}</small>
                </div>
              </div>
              <div class="card-footer">
                <router-link 
                  :to="`/users/${favorite.id}`" 
                  class="btn btn-outline-primary btn-sm"
                >
                  View Profile
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else>
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3>Your Favorites</h3>
          
          <div class="btn-group">
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: personalSortBy === 'name' }"
              @click="sortPersonalFavorites('name')"
            >
              Name
            </button>
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: personalSortBy === 'parish' }"
              @click="sortPersonalFavorites('parish')"
            >
              Parish
            </button>
            <button 
              class="btn btn-outline-primary" 
              :class="{ active: personalSortBy === 'age' }"
              @click="sortPersonalFavorites('age')"
            >
              Age
            </button>
          </div>
        </div>
        
        <div v-if="personalFavorites.length === 0" class="alert alert-info">
          You haven't favorited any users yet.
        </div>
        
        <div v-else class="row">
          <div 
            v-for="favorite in personalFavorites" 
            :key="favorite.id" 
            class="col-md-3 mb-4"
          >
            <div class="card h-100">
              <img 
                :src="favorite.photo || 'https://via.placeholder.com/150'" 
                alt="Profile Photo" 
                class="card-img-top"
                style="height: 150px; object-fit: cover;"
              />
              <div class="card-body">
                <h5 class="card-title">{{ favorite.name }}</h5>
                
                <div v-if="favorite.parish" class="mt-2">
                  <small class="text-muted">Parish: {{ favorite.parish }}</small>
                </div>
                
                <div v-if="favorite.age" class="mt-2">
                  <small class="text-muted">Age: {{ favorite.age }}</small>
                </div>
              </div>
              <div class="card-footer">
                <router-link 
                  :to="`/users/${favorite.id}`" 
                  class="btn btn-outline-primary btn-sm"
                >
                  View Profile
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  name: 'FavouritesReport',
  data() {
    return {
      activeTab: 'top',
      loading: true,
      topFavorites: [],
      personalFavorites: [],
      sortBy: 'count',
      personalSortBy: 'name',
      userId: null
    }
  },
  created() {
    this.userId = JSON.parse(localStorage.getItem('user') || '{}').id
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      
      try {
      
        await this.loadTopFavorites()
        
       
        await this.loadPersonalFavorites()
      } catch (error) {
        console.error('Error loading favorites data:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadTopFavorites() {
      try {
        const response = await apiService.getTopFavourites(20, this.sortBy)
        this.topFavorites = response.data.top_favourites
        
        
        if (this.sortBy === 'parish' || this.sortBy === 'age') {
        }
      } catch (error) {
        console.error('Error loading top favorites:', error)
      }
    },
    
    async loadPersonalFavorites() {
      try {
        const response = await apiService.getUserFavourites(this.userId, this.personalSortBy)
        this.personalFavorites = response.data.favourites
        
       
        if (this.personalSortBy === 'parish' || this.personalSortBy === 'age') {
          if (!this.personalFavorites[0]?.parish && this.personalFavorites.length > 0) {
            this.personalFavorites = await Promise.all(
              this.personalFavorites.map(async user => {
                try {
                 
                  const profilesResponse = await apiService.getProfiles()
                  const userProfile = profilesResponse.data.profiles.find(
                    p => p.user_id === user.id
                  )
                  
                  if (userProfile) {
                    const currentYear = new Date().getFullYear()
                    return {
                      ...user,
                      parish: userProfile.parish,
                      age: currentYear - userProfile.birth_year
                    }
                  }
                  
                  return user
                } catch (error) {
                  console.error('Error loading profile data for user:', user.id, error)
                  return user
                }
              })
            )
          }
        }
      } catch (error) {
        console.error('Error loading personal favorites:', error)
      }
    },
    
    async sortTopFavorites(sortBy) {
      if (this.sortBy === sortBy) return
      
      this.sortBy = sortBy
      this.loading = true
      
      try {
        await this.loadTopFavorites()
      } catch (error) {
        console.error('Error sorting top favorites:', error)
      } finally {
        this.loading = false
      }
    },
    
    async sortPersonalFavorites(sortBy) {
      if (this.personalSortBy === sortBy) return
      
      this.personalSortBy = sortBy
      this.loading = true
      
      try {
        await this.loadPersonalFavorites()
      } catch (error) {
        console.error('Error sorting personal favorites:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>