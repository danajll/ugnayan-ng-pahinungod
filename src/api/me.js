import api from './client'

export const meService = { get: () => api.get('/me/') }