<template>
  <div id="app">
   
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    
    <router-link class="navbar-brand" to="/">
      <strong>Jam-Date</strong>
    </router-link>
    
    
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    
    
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <template v-if="isLoggedIn">
          <li class="nav-item">
            <router-link class="nav-link" :to="'/users/' + userId">My Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profiles/new">Add Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profiles/favourites">Favourites</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/logout">Logout</router-link>
          </li>
        </template>
        <template v-else>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
        </template>
      </ul>
    </div>
  </div>
</nav>
    
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>





<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userId: null
    }
  },
  created() {
  this.checkAuth()
  
  window.addEventListener('auth-changed', this.checkAuth)
},
beforeUnmount() {
  
  window.removeEventListener('auth-changed', this.checkAuth)
},
  methods: {
    checkAuth() {
      const token = localStorage.getItem('jwt')
      const user = JSON.parse(localStorage.getItem('user') || '{}')
      this.isLoggedIn = !!token
      this.userId = user.id || null
    }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  flex: 1;
}

.footer {
  margin-top: auto;
}
</style>

