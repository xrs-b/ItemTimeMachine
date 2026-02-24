<template>
  <div class="register-container">
    <div class="header">
      <h1 class="app-title">注册账号</h1>
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
          v-model="form.email"
          name="email"
          label="邮箱"
          placeholder="请输入邮箱"
          :rules="[
            { required: true, message: '请输入邮箱' },
            { validator: validatorEmail, message: '请输入正确的邮箱格式' }
          ]"
        />
        <van-field
          v-model="form.password"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[
            { required: true, message: '请输入密码' },
            { validator: validatorPassword, message: '密码至少6位' }
          ]"
        />
        <van-field
          v-model="form.confirmPassword"
          type="password"
          name="confirmPassword"
          label="确认密码"
          placeholder="请再次输入密码"
          :rules="[
            { required: true, message: '请再次输入密码' },
            { validator: validatorConfirm, message: '两次密码输入不一致' }
          ]"
        />
      </van-cell-group>
      
      <div class="submit-btn">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          注册
        </van-button>
      </div>
    </van-form>
    
    <div class="bottom-links">
      <span @click="$router.push('/login')">已有账号？立即登录</span>
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
  email: '',
  password: '',
  confirmPassword: ''
})
const loading = ref(false)

const validatorEmail = (val) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)
}

const validatorPassword = (val) => {
  return val.length >= 6
}

const validatorConfirm = (val) => {
  return val === form.value.password
}

const onSubmit = async () => {
  loading.value = true
  try {
    const result = await authStore.registerAction(
      form.value.username,
      form.value.email,
      form.value.password
    )
    if (result.success) {
      showToast({ message: '注册成功', position: 'top' })
      router.replace('/')
    } else {
      showToast({ message: result.message, position: 'top' })
    }
  } catch (error) {
    showToast({ message: error.message || '注册失败', position: 'top' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 48px 24px;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.app-title {
  font-size: 28px;
  font-weight: bold;
  color: #fff;
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
