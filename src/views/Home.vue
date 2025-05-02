<template>
  <div class="home-page">
    <h1>Welcome to JamDate</h1>

    <!-- Search Filters -->
    <div class="search-box">
      <input v-model="filters.name" placeholder="Search by name..." />
      <input v-model="filters.birth_year" placeholder="Birth Year" type="number" />
      <select v-model="filters.sex">
        <option value="">Any Sex</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
      </select>
      <input v-model="filters.race" placeholder="Race" />
      <button @click="searchProfiles">Search</button>
    </div>

    <!-- Display Profiles -->
    <div class="profile-grid">
      <div class="card" v-for="profile in profiles" :key="profile.id">
        <img :src="profile.photo" alt="Profile Photo" />
        <h3>{{ profile.description }}</h3>
        <p>{{ profile.sex }} — {{ profile.race }}</p>
        <router-link :to="`/profiles/${profile.id}`">
          <button>View More Details</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from '../axios'

export default {
  name: 'Home',
  data() {
    return {
      profiles: [],
      filters: {
        name: '',
        birth_year: '',
        sex: '',
        race: ''
      }
    }
  },
  async mounted() {
    await this.fetchRecentProfiles()
  },
  methods: {
    async fetchRecentProfiles() {
      try {
        const response = await apiClient.get('/profiles')
        this.profiles = response.data.slice(-4).reverse()
      } catch (err) {
        console.error('Failed to load recent profiles', err)
      }
    },
    async searchProfiles() {
      try {
        const params = {}
        if (this.filters.name) params.name = this.filters.name
        if (this.filters.birth_year) params.birth_year = this.filters.birth_year
        if (this.filters.sex) params.sex = this.filters.sex
        if (this.filters.race) params.race = this.filters.race

        const response = await apiClient.get('/search', { params })
        this.profiles = response.data
      } catch (err) {
        console.error('Search failed', err)
      }
    }
  }
}
</script>

<style scoped>
.home-page {
  max-width: 900px;
  margin: auto;
  padding: 1rem;
}
.search-box {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}
input, select {
  padding: 0.5rem;
}
button {
  padding: 0.5rem 1rem;
}
.profile-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.card {
  border: 1px solid #ccc;
  padding: 1rem;
  width: 200px;
  text-align: center;
}
.card img {
  width: 100%;
  height: 160px;
  object-fit: cover;
}
</style>
