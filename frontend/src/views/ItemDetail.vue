<template>
  <div class="item-detail-container">
    <van-nav-bar title="物品详情" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content" v-if="item">
      <!-- 图片展示 -->
      <div class="images-section" v-if="item.images && item.images.length > 0">
        <van-swipe class="images-swatch" :autoplay="3000" indicator-color="white">
          <van-swipe-item v-for="img in item.images" :key="img.id">
            <img :src="img.image_url" alt="" />
          </van-swipe-item>
        </van-swipe>
      </div>
      
      <!-- 物品信息 -->
      <div class="info-section">
        <div class="item-header">
          <h1 class="item-name">{{ item.name }}</h1>
          <van-tag :type="item.category_id ? 'primary' : 'default'">
            {{ item.category_name || '未分类' }}
          </van-tag>
        </div>
        
        <div class="price-info">
          <span class="purchase-price">¥{{ item.purchase_price }}</span>
          <span class="days-info" v-if="item.days_since_purchase">
            {{ item.days_since_purchase }}天前购买
          </span>
        </div>
        
        <div class="detail-list">
          <div class="detail-item" v-if="item.brand">
            <span class="label">品牌</span>
            <span class="value">{{ item.brand }}</span>
          </div>
          <div class="detail-item" v-if="item.platform">
            <span class="label">购买平台</span>
            <span class="value">{{ item.platform }}</span>
          </div>
          <div class="detail-item">
            <span class="label">购买日期</span>
            <span class="value">{{ item.purchase_date }}</span>
          </div>
          <div class="detail-item" v-if="item.estimated_value">
            <span class="label">二手估价</span>
            <span class="value estimate">¥{{ item.estimated_value }}</span>
          </div>
          <div class="detail-item" v-if="item.description">
            <span class="label">描述</span>
            <span class="value">{{ item.description }}</span>
          </div>
        </div>
      </div>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <van-button type="primary" block @click="$router.push(`/item/${item.id}/edit`)">
          编辑
        </van-button>
        <van-button type="danger" block plain @click="showDeleteDialog = true">
          删除
        </van-button>
      </div>
    </div>
    
    <van-loading v-else-if="loading" class="loading" />
    <van-empty v-else description="物品不存在" />
    
    <!-- 删除确认对话框 -->
    <van-dialog
      v-model:show="showDeleteDialog"
      title="删除物品"
      message="确定要删除这个物品吗？"
      show-cancel-button
      @confirm="handleDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getItem, deleteItem } from '@/api/items'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()

const item = ref(null)
const loading = ref(true)
const showDeleteDialog = ref(false)

const fetchItem = async () => {
  loading.value = true
  try {
    const res = await getItem(route.params.id)
    item.value = res
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  try {
    await deleteItem(route.params.id)
    showToast({ message: '删除成功', position: 'top' })
    router.replace('/')
  } catch (error) {
    showToast({ message: error.message || '删除失败', position: 'top' })
  }
}

onMounted(() => {
  fetchItem()
})
</script>

<style scoped>
.item-detail-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 80px;
}

.images-swatch img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.info-section {
  background: #fff;
  padding: 16px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-name {
  font-size: 20px;
  font-weight: 600;
}

.price-info {
  margin-bottom: 16px;
}

.purchase-price {
  font-size: 24px;
  font-weight: 600;
  color: #ee0a24;
}

.days-info {
  font-size: 14px;
  color: #969799;
  margin-left: 8px;
}

.detail-list {
  border-top: 1px solid #eee;
  padding-top: 16px;
}

.detail-item {
  display: flex;
  padding: 8px 0;
}

.detail-item .label {
  width: 80px;
  color: #969799;
}

.detail-item .value {
  flex: 1;
}

.detail-item .value.estimate {
  color: #07c160;
}

.action-buttons {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 12px 16px;
  display: flex;
  gap: 12px;
}

.loading {
  padding: 100px 0;
  text-align: center;
}
</style>
