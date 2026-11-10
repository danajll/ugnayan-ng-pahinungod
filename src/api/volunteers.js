import api from './client'

export const volunteerService = {
  list:   ()          => api.get('/volunteers/'),
  get:    (id)        => api.get(`/volunteers/${id}/`),
}