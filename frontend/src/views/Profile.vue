<template>
  <div class="profile-container">
    <van-nav-bar title="我的" fixed />
    
    <div class="content">
      <!-- 用户信息卡片 -->
      <div class="user-card">
        <div class="user-info">
          <van-image
            round
            width="60"
            height="60"
            src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          />
          <div class="user-detail">
            <div class="username">
              {{ user?.username || '用户' }}
              <van-tag type="success" size="small" v-if="user?.is_admin === 1">管理员</van-tag>
            </div>
            <div class="email">{{ user?.email || '' }}</div>
          </div>
        </div>
      </div>
      
      <!-- 统计入口 -->
      <van-cell-group inset>
        <van-cell title="数据统计" is-link to="/stats" icon="chart-trending-o" />
      </van-cell-group>
      
      <!-- 管理员功能 -->
      <van-cell-group inset v-if="user?.is_admin === 1">
        <template #title>
          <span class="section-title">管理功能</span>
        </template>
        <van-cell title="用户管理" is-link to="/admin/users" icon="manager-o" />
      </van-cell-group>
      
      <!-- 分类管理 -->
      <van-cell-group inset>
        <van-cell title="分类管理" is-link to="/categories" icon="label-o" />
      </van-cell-group>
      
      <!-- 退出登录 -->
      <div class="logout-btn">
        <van-button color="#ff6b6b" text-color="#fff" block round @click="handleLogout">
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
  padding-bottom: 60px;
}

.content {
  padding: 60px 12px 12px;
}

.user-card {
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-detail {
  flex: 1;
}

.username {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.email {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 4px;
}

.section-title {
  font-size: 14px;
  color: #969799;
  font-weight: normal;
}

.logout-btn {
  margin-top: 24px;
  padding: 0 16px;
}
</style>
