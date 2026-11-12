import api from './client'

export const taskService = {
  list:   ()         => api.get('/tasks/'),
  create: (data)     => api.post('/tasks/', data),
  update: (id, data) => api.put(`/tasks/${id}/`, data),
  remove: (id)       => api.delete(`/tasks/${id}/`),
}