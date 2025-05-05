<template>
  <div class="profile-details">
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else class="card">
      <div class="card-header bg-success text-white">
        <h2 class="mb-0">{{ profile.description }}</h2>
      </div>
      
      <div class="card-body">
        <div class="row">
          <div class="col-md-4 mb-4">
            <img 
              :src="userPhoto || 'https://via.placeholder.com/300'" 
              alt="Profile Photo" 
              class="img-fluid rounded"
            />
            
            <div class="mt-3">
              <h4>{{ userName }}</h4>
              <p class="text-muted">{{ profile.parish }}</p>
            </div>
          </div>
          
          <div class="col-md-8">
            <div class="mb-4">
              <h5>Biography</h5>
              <p>{{ profile.biography }}</p>
            </div>
            
            <div class="row mb-4">
              <div class="col-md-6">
                <h5>Basic Information</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Sex:</span>
                    <span>{{ profile.sex }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Race:</span>
                    <span>{{ profile.race }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Age:</span>
                    <span>{{ calculateAge(profile.birth_year) }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Height:</span>
                    <span>{{ profile.height }} inches</span>
                  </li>
                </ul>
              </div>
              
              <div class="col-md-6">
                <h5>Favorites</h5>
                <ul class="list-group list-group-flush">
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Cuisine:</span>
                    <span>{{ profile.fav_cuisine }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>Color:</span>
                    <span>{{ profile.fav_colour }}</span>
                  </li>
                  <li class="list-group-item d-flex justify-content-between">
                    <span>School Subject:</span>
                    <span>{{ profile.fav_school_sibject }}</span>
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="mb-4">
              <h5>Preferences</h5>
              <div class="row">
                <div class="col-md-4 mb-2">
                  <div class="card">
                    <div class="card-body text-center">
                      <p>Political</p>
                      <div>
                        <i 
                          :class="[
                            'fas', 
                            profile.political ? 'fa-check text-success' : 'fa-times text-danger'
                          ]"
                        ></i>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-md-4 mb-2">
                  <div class="card">
                    <div class="card-body text-center">
                      <p>Religious</p>
                      <div>
                        <i 
                          :class="[
                            'fas', 
                            profile.religious ? 'fa-check text-success' : 'fa-times text-danger'
                          ]"
                        ></i>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="col-md-4 mb-2">
                  <div class="card">
                    <div class="card-body text-center">
                      <p>Family Oriented</p>
                      <div>
                        <i 
                          :class="[
                            'fas', 
                            profile.family_oriented ? 'fa-check text-success' : 'fa-times text-danger'
                          ]"
                        ></i>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="card-footer d-flex justify-content-between">
        <button class="btn btn-outline-primary">Email Profile</button>
        <button 
          @click="addToFavourites" 
          class="btn btn-outline-danger"
          :disabled="isFavorited"
        >
          <i class="fas" :class="isFavorited ? 'fa-heart' : 'fa-heart-o'"></i>
          {{ isFavorited ? 'Added to Favorites' : 'Add to Favorites' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  name: 'ProfileDetails',
  data() {
    return {
      profile: {},
      user: {},
      isFavorited: false,
      loading: true,
      userPhoto: '',
      userName: ''
    }
  },
  async created() {
    try {
      await this.loadProfileDetails()
    } catch (error) {
      console.error('Error loading profile details:', error)
    } finally {
      this.loading = false
    }
  },
  methods: {
    async loadProfileDetails() {
      const profileId = this.$route.params.profile_id
      
    
      const response = await apiService.getProfile(profileId)
      this.profile = response.data.profile
      
    
      const userResponse = await apiService.getUser(this.profile.user_id)
      this.user = userResponse.data.user
      this.userPhoto = this.user.photo
      this.userName = this.user.name
      
  
      try {
        const currentUserId = JSON.parse(localStorage.getItem('user')).id
        const favoritesResponse = await apiService.getUserFavourites(currentUserId)
        
       
        this.isFavorited = favoritesResponse.data.favourites.some(
          fav => fav.id === this.profile.user_id
        )
      } catch (error) {
        console.error('Error checking favorites:', error)
      }
    },
    
    async addToFavourites() {
      if (this.isFavorited) return
      
      try {
        await apiService.addToFavourites(this.profile.user_id)
        this.isFavorited = true
        alert('User added to favorites!')
      } catch (error) {
        console.error('Error adding to favorites:', error)
        alert('Failed to add user to favorites. Please try again.')
      }
    },
    
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear()
      return currentYear - birthYear
    }
  }

}
</script>