import request from './request'

export function getItems(params = {}) {
  return request.get('/items', { params })
}

export function getItem(id) {
  return request.get(`/items/${id}`)
}

export function createItem(data) {
  return request.post('/items', data)
}

export function updateItem(id, data) {
  return request.put(`/items/${id}`, data)
}

export function deleteItem(id) {
  return request.delete(`/items/${id}`)
}

export function uploadImage(itemId, file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request.post(`/items/${itemId}/images`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function deleteImage(imageId) {
  return request.delete(`/items/images/${imageId}`)
}
