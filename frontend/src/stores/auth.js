import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)
  
  const isLoggedIn = computed(() => !!token.value)
  
  async function loginAction(username, password) {
    try {
      const res = await login(username, password)
      token.value = res.access_token
      localStorage.setItem('token', res.access_token)
      await fetchUser()
      return { success: true }
    } catch (error) {
      return { success: false, message: error.message || '登录失败' }
    }
  }
  
  async function registerAction(username, email, password) {
    try {
      await register(username, email, password)
      // 注册成功后自动登录
      return await loginAction(username, password)
    } catch (error) {
      return { success: false, message: error.message || '注册失败' }
    }
  }
  
  async function fetchUser() {
    if (!token.value) return
    try {
      const res = await getCurrentUser()
      user.value = res
    } catch (error) {
      console.error('获取用户信息失败:', error)
      logout()
    }
  }
  
  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }
  
  // 初始化时获取用户信息
  if (token.value) {
    fetchUser()
  }
  
  return {
    token,
    user,
    isLoggedIn,
    loginAction,
    registerAction,
    logout,
    fetchUser
  }
})
