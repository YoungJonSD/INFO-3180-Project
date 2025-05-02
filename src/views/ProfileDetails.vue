<template>
    <div class="profile-details">
      <div class="profile-header">
        <img :src="profile.photo" alt="Profile Photo" class="profile-img" />
        <h1>{{ profile.name }}</h1>
        <p>{{ profile.description }}</p>
      </div>
  
      <ul class="profile-info">
        <li>Parish: {{ profile.parish }}</li>
        <li>Biography: {{ profile.biography }}</li>
        <li>Birth Year: {{ profile.birth_year }}</li>
        <li>Race: {{ profile.race }}</li>
        <li>Sex: {{ profile.sex }}</li>
        <li>Height: {{ profile.height }} inches</li>
        <li>Favorite Color: {{ profile.fav_colour }}</li>
        <li>Favorite Subject: {{ profile.fav_school_sibject }}</li>
        <li>Political: {{ profile.political ? 'Yes' : 'No' }}</li>
        <li>Religious: {{ profile.religious ? 'Yes' : 'No' }}</li>
        <li>Family-Oriented: {{ profile.family_oriented ? 'Yes' : 'No' }}</li>
      </ul>
  
      <div class="action-buttons">
        <button class="email-btn">Email User</button>
        <button class="fav-btn" @click="addToFavourites">❤️ Add to Favourites</button>
        <p v-if="message">{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import apiClient from '../axios'
  
  export default {
    name: 'ProfileDetails',
    data() {
      return {
        profile: {},
        message: ''
      }
    },
    async created() {
      const profileId = this.$route.params.profile_id
      const response = await apiClient.get(`/profiles/${profileId}`)
      this.profile = response.data
    },
    methods: {
      async addToFavourites() {
        try {
          await apiClient.post(`/profiles/${this.profile.id}/favourite`)
          this.message = 'Added to favourites!'
        } catch (err) {
          this.message = 'Failed to add to favourites.'
          console.error(err)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .profile-details {
    max-width: 800px;
    margin: auto;
    padding: 1rem;
  }
  .profile-header {
    text-align: center;
  }
  .profile-img {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    object-fit: cover;
  }
  .profile-info {
    list-style: none;
    padding: 0;
  }
  .profile-info li {
    margin: 0.3rem 0;
  }
  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
  }
  .email-btn,
  .fav-btn {
    padding: 0.6rem 1.2rem;
    border: none;
    background-color: #d14f4f;
    color: white;
    border-radius: 6px;
    cursor: pointer;
  }
  </style>
  