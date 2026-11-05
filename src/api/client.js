// src/api/client.js
import axios from 'axios'

const api = axios.create({
  baseURL: '/api', // Vite proxy forwards this to Django
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    // DRF TokenAuthentication requires the "Token" prefix, NOT "Bearer"
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('auth_token')
      // optionally redirect to login
    }
    return Promise.reject(err)
  }
)

export default api