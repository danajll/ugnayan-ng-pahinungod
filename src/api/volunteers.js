import api from './client'

export const volunteerService = {
  list:   ()          => api.get('/volunteers/'),
  get:    (id)        => api.get(`/volunteers/${id}/`),
  patch:  (id, data)  => api.patch(`/volunteers/${id}/`, data),
  myProfile:     ()   => api.get('/volunteers/me/profile/'),
  updateProfile: (data) => api.patch('/volunteers/me/profile/', data),
  onboard:       (data) => api.patch('/volunteers/me/onboarding/', data),
}