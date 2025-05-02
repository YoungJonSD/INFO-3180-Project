import axios from 'axios'

// Create an Axios instance
const apiClient = axios.create({
  baseURL: 'http://localhost:8080/api'
})

// Intercept requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')

  // Don't attach token to login or register
  const isAuthRoute = config.url.includes('/auth/login') || config.url.includes('/register')

  if (token && !isAuthRoute) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
}, (error) => {
  return Promise.reject(error)
})

export default apiClient
