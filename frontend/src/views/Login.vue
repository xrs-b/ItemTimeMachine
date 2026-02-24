<template>
  <div class="login-container">
    <div class="logo-section">
      <h1 class="app-title">物品时光机</h1>
      <p class="app-subtitle">记录生活，珍藏回忆</p>
    </div>
    
    <van-form @submit="onSubmit">
      <van-cell-group inset>
        <van-field
          v-model="form.username"
          name="username"
          label="用户名"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        <van-field
          v-model="form.password"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
        />
      </van-cell-group>
      
      <div class="submit-btn">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          登录
        </van-button>
      </div>
    </van-form>
    
    <div class="bottom-links">
      <span @click="$router.push('/register')">还没有账号？立即注册</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})
const loading = ref(false)

const onSubmit = async () => {
  loading.value = true
  try {
    const result = await authStore.loginAction(form.value.username, form.value.password)
    if (result.success) {
      showToast({ message: '登录成功', position: 'top' })
      router.replace('/')
    } else {
      showToast({ message: result.message, position: 'top' })
    }
  } catch (error) {
    showToast({ message: error.message || '登录失败', position: 'top' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 24px;
}

.logo-section {
  text-align: center;
  margin-bottom: 48px;
}

.app-title {
  font-size: 32px;
  font-weight: bold;
  color: #fff;
  margin-bottom: 8px;
}

.app-subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
}

.submit-btn {
  padding: 24px 16px;
}

.bottom-links {
  text-align: center;
  margin-top: 24px;
}

.bottom-links span {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  cursor: pointer;
}
</style>
