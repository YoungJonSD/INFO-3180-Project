// components/ProfileCard.vue
<template>
  <div class="card h-100">
    <div class="position-relative">
      <img 
        :src="userPhoto || 'https://via.placeholder.com/300x200'" 
        alt="Profile Photo" 
        class="card-img-top"
        style="height: 200px; object-fit: cover;"
      />
      <div class="card-img-overlay d-flex align-items-end justify-content-center">
        <span class="badge bg-warning text-dark mb-2">{{ profile.parish }}</span>
      </div>
    </div>
    
    <div class="card-body">
      <h5 class="card-title">{{ userName }}</h5>
      <p class="card-text">{{ truncateText(profile.description, 100) }}</p>
      
      <div class="d-flex justify-content-between mb-2">
        <span>
          <i class="fas fa-venus-mars me-1"></i>
          {{ profile.sex }}
        </span>
        <span>
          <i class="fas fa-birthday-cake me-1"></i>
          {{ calculateAge(profile.birth_year) }} years
        </span>
      </div>
      
      <div>
        <i class="fas fa-globe me-1"></i>
        {{ profile.race }}
      </div>
    </div>
    
    <div class="card-footer d-flex justify-content-between align-items-center">
      <router-link 
        :to="`/profiles/${profile.id}`" 
        class="btn btn-outline-primary btn-sm"
      >
        View More Details
      </router-link>
      <button 
        @click="toggleFavorite" 
        class="btn btn-sm" 
        :class="isFavorited ? 'btn-danger' : 'btn-outline-danger'"
      >
        <i class="fas" :class="isFavorited ? 'fa-heart' : 'fa-heart-o'"></i>
      </button>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  name: 'ProfileCard',
  props: {
    profile: {
      type: Object,
      required: true
    },
    userName: {
      type: String,
      required: true
    },
    userPhoto: {
      type: String,
      default: ''
    },
    isFavorited: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    calculateAge(birthYear) {
      const currentYear = new Date().getFullYear()
      return currentYear - birthYear
    },
    
    truncateText(text, maxLength) {
      if (!text || text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    },
    
    async toggleFavorite() {
      if (!this.isFavorited) {
        try {
          await apiService.addToFavourites(this.profile.user_id_fk)
          this.$emit('favorite-toggled', this.profile.user_id_fk)
        } catch (error) {
          console.error('Error adding to favorites:', error)
          alert('Failed to add user to favorites. Please try again.')
        }
      }
    }
  }
}
</script>

<style scoped>
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.badge {
  font-size: 0.8rem;
  font-weight: 500;
}
</style>