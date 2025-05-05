<template>
    <div class="user-profile">
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <div v-else>
        <div class="profile-header mb-5">
          <div class="row align-items-center">
            <div class="col-md-3 text-center">
              <img 
                :src="user.photo || 'https://via.placeholder.com/150'" 
                alt="Profile Photo" 
                class="rounded-circle img-thumbnail" 
                style="width: 150px; height: 150px; object-fit: cover;"
              />
            </div>
            <div class="col-md-9">
              <h2>My Profile: {{ user.name }}</h2>
              <p class="text-muted">
                <small>Year Joined: {{ new Date(user.date_joined).getFullYear() }}</small>
              </p>
            </div>
          </div>
        </div>
        
        <div v-if="profiles.length === 0" class="alert alert-warning">
          <p>You haven't created any profiles yet. Get started by creating your first profile!</p>
          <router-link to="/profiles/new" class="btn btn-primary">Create Profile</router-link>
        </div>
        
        <div v-else>
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h3>Your Profiles</h3>
            <div v-if="profiles.length < 3">
              <router-link to="/profiles/new" class="btn btn-primary">Add New Profile</router-link>
            </div>
          </div>
          
          <div class="row">
            <div 
              v-for="profile in profiles" 
              :key="profile.id" 
              class="col-md-6 mb-4"
            >
              <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">{{ profile.description }}</h5>
                  <span class="badge bg-primary">{{ profile.parish }}</span>
                </div>
                <div class="card-body">
                  <p>{{ truncateText(profile.biography, 150) }}</p>
                  <div class="row mb-3">
                    <div class="col-6">
                      <small class="text-muted">Sex: {{ profile.sex }}</small>
                    </div>
                    <div class="col-6">
                      <small class="text-muted">Age: {{ calculateAge(profile.birth_year) }}</small>
                    </div>
                  </div>
                  <div class="row mb-3">
                    <div class="col-6">
                      <small class="text-muted">Race: {{ profile.race }}</small>
                    </div>
                    <div class="col-6">
                      <small class="text-muted">Height: {{ profile.height }} inches</small>
                    </div>
                  </div>
                  <div class="mb-3">
                    <p class="mb-1"><small class="text-muted">Preferences:</small></p>
                    <div class="d-flex flex-wrap">
                      <span 
                        v-if="profile.political" 
                        class="badge bg-secondary me-1 mb-1"
                      >Political</span>
                      <span 
                        v-if="profile.religious" 
                        class="badge bg-secondary me-1 mb-1"
                      >Religious</span>
                      <span 
                        v-if="profile.family_oriented" 
                        class="badge bg-secondary me-1 mb-1"
                      >Family Oriented</span>
                    </div>
                  </div>
                </div>
                <div class="card-footer">
                  <div class="d-flex justify-content-between">
                    <router-link 
                      :to="`/profiles/${profile.id}`" 
                      class="btn btn-outline-primary btn-sm"
                    >
                      View More Details
                    </router-link>
                    <button 
                      @click="findMatches(profile.id)" 
                      class="btn btn-outline-success btn-sm"
                    >
                      Match Me
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="showingMatches" class="mt-5">
          <h3>Your Matches</h3>
          
          <div v-if="matches.length === 0" class="alert alert-info">
            No matches found for your profile criteria.
          </div>
          
          <div v-else class="row">
            <div 
              v-for="match in matches" 
              :key="match.id" 
              class="col-md-4 mb-4"
            >
              <div class="card h-100">
                <div class="card-header">
                  <h5 class="mb-0">{{ match.description }}</h5>
                </div>
                <div class="card-body">
                  <p>{{ truncateText(match.biography, 100) }}</p>
                  <div class="mb-2">
                    <small class="text-muted">Parish: {{ match.parish }}</small>
                  </div>
                  <div class="mb-2">
                    <small class="text-muted">Age: {{ calculateAge(match.birth_year) }}</small>
                  </div>
                </div>
                <div class="card-footer">
                  <router-link 
                    :to="`/profiles/${match.id}`" 
                    class="btn btn-outline-primary btn-sm"
                  >
                    View More Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="userFavourites.length > 0" class="mt-5">
          <h3>Your Favourites</h3>
          
          <div class="row">
            <div 
              v-for="fav in userFavourites" 
              :key="fav.id" 
              class="col-md-3 mb-4"
            >
              <div class="card h-100">
                <img 
                  :src="fav.photo || 'https://via.placeholder.com/150'" 
                  alt="Profile Photo" 
                  class="card-img-top"
                  style="height: 150px; object-fit: cover;"
                />
                <div class="card-body">
                  <h5 class="card-title">{{ fav.name }}</h5>
                </div>
                <div class="card-footer">
                  <router-link 
                    :to="`/users/${fav.id}`" 
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
    name: 'UserProfile',
    data() {
      return {
        user: {},
        profiles: [],
        matches: [],
        userFavourites: [],
        loading: true,
        showingMatches: false
      }
    },
    async created() {
      try {
        await this.loadUserProfile()
      } catch (error) {
        console.error('Error loading profile:', error)
      } finally {
        this.loading = false
      }
    },
    methods: {
      async loadUserProfile() {
  const userId = this.$route.params.user_id
  
  
  console.log("Fetching user with ID:", userId)
  const userResponse = await apiService.getUser(userId)
  this.user = userResponse.data.user
  console.log("User loaded:", this.user)
  
 
  console.log("Fetching all profiles with includeOwn=true")
  try {
  const profilesResponse = await apiService.getProfiles(true)
  this.profiles = profilesResponse.data.profiles  
  console.log("User profiles:", this.profiles)
} catch (error) {
  console.error("Error fetching user profiles:", error)
  this.profiles = []
}
  
  
  try {
    const favouritesResponse = await apiService.getUserFavourites(userId)
    this.userFavourites = favouritesResponse.data.favourites
  } catch (error) {
    console.error('Error loading favourites:', error)
    this.userFavourites = []
  }
},
      
      async findMatches(profileId) {
        try {
          const response = await apiService.getMatches(profileId)
          this.matches = response.data.matches
          this.showingMatches = true
        } catch (error) {
          console.error('Error finding matches:', error)
          alert('Failed to find matches. Please try again.')
        }
      },
      
      calculateAge(birthYear) {
        const currentYear = new Date().getFullYear()
        return currentYear - birthYear
      },
      
      truncateText(text, maxLength) {
        if (text.length <= maxLength) return text
        return text.substring(0, maxLength) + '...'
      }
    }
  }
  </script>