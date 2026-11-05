import api from './client'

export const authService = {
  login:     (username, password) => api.post('/login/', { username, password }),
  register:  (data)               => api.post('/register/', data),
  googleLogin: (idToken)          => api.post('/auth/google/', { id_token: idToken }),
  health:    ()                   => api.get('/health/'),
}