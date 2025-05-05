<template>
    <div class="my-profile">
      <div class="user-header">
        <img :src="user.photo" class="avatar" />
        <h1>My Profile</h1>
        <h2>{{ user.name }}</h2>
        <p>Joined: {{ formatDate(user.date_joined) }}</p>
      </div>
  
      <h2>My Created Profiles</h2>
      <div v-if="myProfiles.length" class="profile-row">
        <div class="card" v-for="p in myProfiles" :key="p.id">
          <img :src="p.photo" />
          <h3>{{ p.description }}</h3>
          <p>{{ p.biography }}</p>
          <router-link :to="`/profiles/${p.id}`">
            <button>Show More Details</button>
          </router-link>
          <router-link :to="`/profiles/${p.id}/matches`">
          <button style="margin-top: 0.5rem;">Match Me</button>
          </router-link>
        </div>
      </div>
      <p v-else>No profiles created yet.</p>
  
      <h2>My Favourites</h2>
      <div v-if="favourites.length" class="profile-row">
        <div class="card" v-for="f in favourites" :key="f.id">
          <img :src="f.photo" />
          <h3>{{ f.description }}</h3>
          <p>{{ f.biography }}</p>
          <router-link :to="`/profiles/${f.id}`">
            <button>Show More Details</button>
          </router-link>
        </div>
      </div>
      <p v-else>You have not favourited any profiles yet.</p>
    </div>
  </template>
  
  <script>
  import apiService from '@/services/api'
  
  export default {
    name: 'MyProfile',
    data() {
      return {
        user: {},
        myProfiles: [],
        favourites: []
      }
    },
    async mounted() {
      try {
        // Get logged-in user info
        const userRes = await apiClient.get('/me')
        this.user = userRes.data
  
        // Get up to 3 profiles created by user
        const profilesRes = await apiClient.get(`/users/${this.user.id}/profiles`)
        this.myProfiles = profilesRes.data.slice(0, 3)
  
        // Get favourites
        const favRes = await apiClient.get(`/users/${this.user.id}/favourites`)
        this.favourites = favRes.data
      } catch (err) {
        console.error(err)
      }
    },
    methods: {
      formatDate(date) {
        return new Date(date).toLocaleDateString()
      }
    }
  }
  </script>
  
  <style scoped>
  .my-profile {
    max-width: 900px;
    margin: auto;
    padding: 1rem;
  }
  .user-header {
    text-align: center;
    margin-bottom: 2rem;
  }
  .avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    object-fit: cover;
  }
  .profile-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .card {
    width: 280px;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    text-align: center;
  }
  .card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 6px;
  }
  button {
    margin-top: 0.5rem;
    padding: 0.4rem 1rem;
    background-color: #f26666;
    color: white;
    border: none;
    border-radius: 4px;
  }
  </style>
  