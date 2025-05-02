<template>
    <div class="profile-form">
      <h1>Create New Profile</h1>
      <form @submit.prevent="submitForm">
        <input v-model="form.description" placeholder="Description" required />
        <input v-model="form.parish" placeholder="Parish" required />
        <textarea v-model="form.biography" placeholder="Biography"></textarea>
  
        <select v-model="form.sex">
          <option value="">Sex</option>
          <option>Male</option>
          <option>Female</option>
        </select>
        <input v-model="form.race" placeholder="Race" />
        <input type="number" v-model.number="form.birth_year" placeholder="Birth Year" />
        <input type="number" v-model.number="form.height" placeholder="Height in inches" />
  
        <input v-model="form.fav_cuisine" placeholder="Favourite Cuisine" />
        <input v-model="form.fav_colour" placeholder="Favourite Colour" />
        <input v-model="form.fav_school_sibject" placeholder="Favourite Subject" />
  
        <label><input type="checkbox" v-model="form.political" /> Political</label>
        <label><input type="checkbox" v-model="form.religious" /> Religious</label>
        <label><input type="checkbox" v-model="form.family_oriented" /> Family-Oriented</label>
  
        <input v-model="form.photo" placeholder="Photo URL" />
  
        <button type="submit">Create Profile</button>
      </form>
  
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import apiClient from '../axios'
  
  export default {
    name: 'NewProfile',
    data() {
      return {
        form: {
          description: '',
          parish: '',
          biography: '',
          sex: '',
          race: '',
          birth_year: '',
          height: '',
          fav_cuisine: '',
          fav_colour: '',
          fav_school_sibject: '',
          political: false,
          religious: false,
          family_oriented: false,
          photo: ''
        },
        message: ''
      }
    },
    methods: {
      async submitForm() {
        try {
          const res = await apiClient.post('/profiles', this.form)
          this.message = 'Profile created successfully!'
          this.$router.push(`/profiles/${res.data.id}`)
        } catch (err) {
          this.message = err.response?.data?.message || 'Error creating profile.'
          console.error(err)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .profile-form {
    max-width: 600px;
    margin: auto;
    padding: 1rem;
  }
  input, select, textarea {
    display: block;
    width: 100%;
    margin-bottom: 10px;
  }
  button {
    padding: 0.5rem 1rem;
  }
  </style>
  