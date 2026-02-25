import request from './request'

export function getSummary() {
  return request.get('/statistics/summary')
}

export function getCategoryStats() {
  return request.get('/statistics/by-category')
}

export function getPlatformStats() {
  return request.get('/statistics/by-platform')
}

export function getTrend(year) {
  return request.get('/statistics/trend', { params: { year } })
}
