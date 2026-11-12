import api from './client'

export const lookupService = {
  programs: () => api.get('/programs/'),
  subjects: () => api.get('/subjects/'),
}