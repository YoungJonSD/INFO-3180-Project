<template>
    <div class="match-report">
      <h1>Match Report</h1>
      <div class="match-grid">
        <div class="card" v-for="match in matches" :key="match.id">
          <img :src="match.photo" />
          <h3>{{ match.description }}</h3>
          <p>{{ match.biography }}</p>
          <router-link :to="`/profiles/${match.id}`">
            <button>View Profile</button>
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import apiService from '@/services/api'
  
  export default {
    name: 'MatchReport',
    data() {
      return {
        matches: []
      }
    },
    async mounted() {
      const profileId = this.$route.params.profile_id
      const res = await apiClient.get(`/profiles/${profileId}/matches`)
      this.matches = res.data
    }
  }
  </script>
  
  <style scoped>
  .match-report {
    max-width: 900px;
    margin: auto;
    padding: 1rem;
  }
  .match-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }
  .card {
    width: 240px;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    text-align: center;
  }
  .card img {
    width: 100%;
    height: 160px;
    object-fit: cover;
  }
  </style>
  