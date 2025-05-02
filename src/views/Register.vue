<template>
    <div class="register-form">
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <label>Username:</label>
        <input type="text" v-model="form.username" required />
  
        <label>Password:</label>
        <input type="password" v-model="form.password" required />
  
        <label>Full Name:</label>
        <input type="text" v-model="form.name" required />
  
        <label>Email:</label>
        <input type="email" v-model="form.email" required />
  
        <label>Photo URL:</label>
        <input type="text" v-model="form.photo" />
  
        <button type="submit">Register</button>
      </form>
  
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
 import apiClient from '../axios'

  
  export default {
    name: 'Register',
    data() {
      return {
        form: {
          username: '',
          password: '',
          name: '',
          email: '',
          photo: ''
        },
        message: ''
      }
    },
    methods: {
      async handleRegister() {
        try {
          const response = await apiClient.post('/register', this.form)

          this.message = response.data.message || 'Registration successful!'
          this.$router.push('/login')
        } catch (err) {
          this.message = err.response?.data?.message || 'Registration failed.'
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .register-form {
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
  