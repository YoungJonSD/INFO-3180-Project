import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8080/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})


apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  const skipAuthRoutes = ['/login', '/register']
  if (token && !skipAuthRoutes.some(path => config.url.includes(path))) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default apiClient
