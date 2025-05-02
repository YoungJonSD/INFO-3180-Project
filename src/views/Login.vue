<template>
    <div class="login-form">
      <h1>Login</h1>
      <form @submit.prevent="handleLogin">
        <label>Username:</label>
        <input type="text" v-model="credentials.username" required />
  
        <label>Password:</label>
        <input type="password" v-model="credentials.password" required />
  
        <button type="submit">Login</button>
      </form>
  
      <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import apiClient from '../axios'

  
  export default {
    name: 'Login',
    data() {
      return {
        credentials: {
          username: '',
          password: ''
        },
        errorMessage: ''
      }
    },
    methods: {
      async handleLogin() {
        try {
          const response = await apiClient.post('/auth/login', this.credentials)

  
          // Save token (you can also use Vuex or Pinia)
          localStorage.setItem('token', response.data.access_token)
  
          // Redirect after login
          this.$router.push('/')
        } catch (error) {
          this.errorMessage = error.response?.data?.message || 'Login failed'
          console.error(error)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .login-form {
    max-width: 400px;
    margin: auto;
    padding: 1rem;
  }
  input {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }
  button {
    padding: 0.5rem 1rem;
  }
  </style>
  