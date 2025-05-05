<template>
  <div class="login">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-primary text-white text-center">
            <h3>Jam-Date</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="credentials.username" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="credentials.password" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="alert alert-danger" v-if="error">
                {{ error }}
              </div>
              
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Login</button>
              </div>
              
              <div class="text-center mt-3">
                <p>Forgot your password? Too bad.</p>
              </div>
              
              <div class="d-flex justify-content-center mt-3">
                <router-link to="/register" class="me-3">Register Date</router-link>
                <router-link to="/profiles/favourites">View Reports</router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import apiService from '@/services/api'

export default {
  name: 'Login',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      error: null
    }
  },
  methods: {
    async login() {
      try {
        this.error = null
        const response = await apiService.login(this.credentials)
        
      
        localStorage.setItem('jwt', response.data.access_token)
         localStorage.setItem('user', JSON.stringify(response.data.user))


        window.dispatchEvent(new Event('auth-changed'))


       this.$router.push('/')
      } catch (error) {
        this.error = error.response?.data?.error || 'Login failed. Please try again.'
      }
    }
  }
}
</script>