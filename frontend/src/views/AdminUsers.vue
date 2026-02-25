<template>
  <div class="admin-users-container">
    <van-nav-bar title="用户管理" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <van-loading v-if="loading" />
      
      <van-empty v-else-if="users.length === 0" description="暂无用户" />
      
      <van-cell-group v-else inset>
        <van-cell 
          v-for="user in users" 
          :key="user.id"
          :title="user.username"
          :label="user.email"
        >
          <template #value>
            <div class="user-actions">
              <van-tag type="success" v-if="user.is_admin === 1">管理员</van-tag>
              <van-tag :type="user.is_active === 1 ? 'success' : 'danger'">
                {{ user.is_active === 1 ? '正常' : '已禁用' }}
              </van-tag>
              <van-button 
                v-if="user.is_admin !== 1"
                size="small" 
                :type="user.is_active === 1 ? 'default' : 'primary'"
                @click="toggleUserStatus(user)"
              >
                {{ user.is_active === 1 ? '禁用' : '启用' }}
              </van-button>
            </div>
          </template>
        </van-cell>
      </van-cell-group>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers, updateUserStatus } from '@/api/admin'
import { showToast } from 'vant'

const loading = ref(false)
const users = ref([])

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res || []
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loading.value = false
  }
}

const toggleUserStatus = async (user) => {
  const newStatus = user.is_active === 1 ? 0 : 1
  try {
    await updateUserStatus(user.id, { is_active: newStatus })
    user.is_active = newStatus
    showToast({ message: newStatus === 1 ? '已启用' : '已禁用', position: 'top' })
  } catch (error) {
    showToast({ message: error.message || '操作失败', position: 'top' })
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.admin-users-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 12px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
