import api from './client'

export const authService = {
  googleLogin: (idToken) => api.post('/auth/google/', { id_token: idToken }),
}