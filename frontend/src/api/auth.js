import request from './request'
import store from '@/stores/auth'

export function login(username, password) {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  
  return request.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function register(username, email, password) {
  return request.post('/auth/register', {
    username,
    email,
    password
  })
}

export function getCurrentUser() {
  return request.get('/auth/me')
}

export function logout() {
  store.logout()
}
