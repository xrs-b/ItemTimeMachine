<template>
  <div class="profile-container">
    <van-nav-bar title="我的" fixed />
    
    <div class="content">
      <!-- 用户信息 -->
      <div class="user-section">
        <van-image
          round
          width="60"
          height="60"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
        <div class="user-info">
          <span class="username">{{ user?.username || '用户' }}</span>
          <span class="email">{{ user?.email || '' }}</span>
        </div>
      </div>
      
      <!-- 功能列表 -->
      <van-cell-group inset>
        <van-cell title="分类管理" is-link to="/categories" />
        <van-cell title="数据统计" is-link to="/stats" />
      </van-cell-group>
      
      <van-cell-group inset>
        <van-cell title="关于我们" is-link @click="showAbout = true" />
      </van-cell-group>
      
      <div class="logout-btn">
        <van-button type="danger" block round @click="handleLogout">
          退出登录
        </van-button>
      </div>
    </div>
    
    <!-- 底部导航 -->
    <van-tabbar v-model="activeTab" fixed>
      <van-tabbar-item icon="wap-home" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="chart-trending-o" to="/stats">统计</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/profile">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { showToast } from 'vant'

const router = useRouter()
const authStore = useAuthStore()

const activeTab = ref(2)
const user = ref(null)
const showAbout = ref(false)

const handleLogout = () => {
  authStore.logout()
  router.replace('/login')
  showToast({ message: '已退出登录', position: 'top' })
}

onMounted(() => {
  user.value = authStore.user
})
</script>

<style scoped>
.profile-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 50px;
}

.content {
  padding-top: 46px;
  padding: 12px;
}

.user-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 32px 16px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.email {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

.logout-btn {
  margin-top: 24px;
  padding: 0 16px;
}
</style>
