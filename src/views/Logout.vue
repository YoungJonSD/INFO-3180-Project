<template>
    <div class="logout-page text-center">
      <div class="spinner-border mb-3" role="status" v-if="loggingOut">
        <span class="visually-hidden">Loading...</span>
      </div>
      <h2>Logging out...</h2>
    </div>
  </template>
  
  <script>
  import apiService from '@/services/api'
  
  export default {
    name: 'Logout',
    data() {
      return {
        loggingOut: true
      }
    },
    async created() {
      try {
  
        await apiService.logout()
      } catch (error) {
        console.error('Logout API error:', error)
      } finally {
        
        localStorage.removeItem('jwt')
        localStorage.removeItem('user')
        
       
        this.$root.$emit('auth-changed')
        
      
        this.$router.push('/login')
      }
    }
  }
  </script>