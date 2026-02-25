import request from './request'

export function getUsers() {
  return request.get('/admin/users')
}

export function updateUserStatus(userId, data) {
  return request.put(`/admin/users/${userId}`, data)
}
