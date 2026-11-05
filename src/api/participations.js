import api from './client'

export const participationService = {
  myParticipations: ()             => api.get('/me/participations/'),
  cancel:           (id)           => api.patch(`/participations/${id}/`, { status: 'cancelled' }),
  remove:           (id)           => api.delete(`/participations/${id}/`),
}