<template>
  <div class="register">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header bg-info text-white text-center">
            <h3>Register for Jam-Date</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="register">
              <div class="mb-3">
                <label for="username" class="form-label">Username:</label>
                <input 
                  type="text" 
                  id="username" 
                  v-model="user.username" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="user.password" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="fullName" class="form-label">Full Name:</label>
                <input 
                  type="text" 
                  id="fullName" 
                  v-model="user.name" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="email" class="form-label">Email Address:</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="user.email" 
                  class="form-control" 
                  required
                />
              </div>
              
              <div class="mb-3">
                <label for="photo" class="form-label">Photo URL:</label>
                <input 
                  type="text" 
                  id="photo" 
                  v-model="user.photo" 
                  class="form-control"
                />
                <small class="form-text text-muted">Enter a URL for your profile photo</small>
              </div>
              
              <div class="alert alert-danger" v-if="error">
                {{ error }}
              </div>
              
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-info text-white">
                  Register
                </button>
              </div>
              
              <div class="text-center mt-3">
                <p>Already have an account? <router-link to="/login">Login</router-link></p>
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
  name: 'Register',
  data() {
    return {
      user: {
        username: '',
        password: '',
        name: '',
        email: '',
        photo: ''
      },
      error: null
    }
  },
  methods: {
    async register() {
      try {
        this.error = null
        const response = await apiService.register(this.user)
        
        alert('Registration successful! Please login.')
        this.$router.push('/login')
      } catch (error) {
        this.error = error.response?.data?.error || 'Registration failed. Please try again.'
      }
    }
  }
}
</script>
