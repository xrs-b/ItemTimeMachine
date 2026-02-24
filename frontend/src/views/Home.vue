<template>
  <div class="home-container">
    <!-- 顶部导航 -->
    <van-nav-bar title="物品时光机" fixed>
      <template #right>
        <van-icon name="search" size="18" @click="$router.push('/search')" />
      </template>
    </van-nav-bar>
    
    <!-- 内容区域 -->
    <div class="content">
      <div v-if="loading" class="loading-state">
        <van-loading size="24px">加载中...</van-loading>
      </div>
      
      <div v-else-if="items.length === 0" class="empty-state">
        <van-empty description="还没有记录任何物品">
          <van-button type="primary" round @click="$router.push('/add')">
            添加第一个物品
          </van-button>
        </van-empty>
      </div>
      
      <div v-else class="items-list">
        <div v-for="item in items" :key="item.id" class="item-card" @click="$router.push(`/item/${item.id}`)">
          <!-- 图片九宫格 -->
          <div class="images-grid" v-if="item.images && item.images.length > 0">
            <div 
              v-for="(img, idx) in item.images.slice(0, 9)" 
              :key="img.id"
              class="image-item"
              :class="{ 'single': item.images.length === 1, 'multiple': item.images.length > 1 }"
            >
              <img :src="img.thumbnail_url || img.image_url" :alt="item.name" />
            </div>
          </div>
          
          <!-- 物品信息 -->
          <div class="item-info">
            <div class="item-header">
              <span class="item-name">{{ item.name }}</span>
              <van-tag :type="getTagType(item.category_id)" size="small">
                {{ item.category_name || '未分类' }}
              </van-tag>
            </div>
            
            <div class="item-details">
              <span class="brand" v-if="item.brand">{{ item.brand }}</span>
              <span class="platform" v-if="item.platform">{{ item.platform }}</span>
            </div>
            
            <div class="item-footer">
              <div class="price-info">
                <span class="purchase-price">¥{{ item.purchase_price }}</span>
                <span class="days-info" v-if="item.days_since_purchase">
                  · {{ item.days_since_purchase }}天前
                </span>
              </div>
              <div class="estimate-info" v-if="item.estimated_value">
                <span class="estimate-label">二手约</span>
                <span class="estimate-price">¥{{ item.estimated_value }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 加载更多 -->
        <div class="load-more" v-if="hasMore" @click="loadMore">
          <span v-if="loadingMore">加载中...</span>
          <span v-else>点击加载更多</span>
        </div>
      </div>
    </div>
    
    <!-- 返回顶部按钮 -->
    <van-back-top />
    
    <!-- 发布按钮 -->
    <div class="publish-btn" @click="$router.push('/add')">
      <van-icon name="plus" size="28" />
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
import { getItems } from '@/api/items'
import { showToast } from 'vant'

const activeTab = ref(0)
const items = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const page = ref(1)
const hasMore = ref(true)

const getTagType = (categoryId) => {
  // 根据分类返回不同颜色标签
  const types = ['primary', 'success', 'warning', 'danger']
  return types[categoryId % 4] || 'primary'
}

const fetchItems = async () => {
  loading.value = true
  try {
    const res = await getItems({ page: 1, page_size: 20 })
    items.value = res.items || []
    hasMore.value = res.has_more
    page.value = 1
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loading.value = false
  }
}

const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  
  loadingMore.value = true
  try {
    const res = await getItems({ page: page.value + 1, page_size: 20 })
    items.value = [...items.value, ...(res.items || [])]
    hasMore.value = res.has_more
    page.value++
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loadingMore.value = false
  }
}

onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 50px;
}

.content {
  padding-top: 46px;
}

.loading-state,
.empty-state {
  padding: 100px 0;
  text-align: center;
}

.items-list {
  padding: 12px;
}

.item-card {
  background: #fff;
  border-radius: 12px;
  margin-bottom: 12px;
  overflow: hidden;
  cursor: pointer;
}

.images-grid {
  display: grid;
  gap: 2px;
}

.images-grid .single {
  grid-template-columns: 1fr;
}

.images-grid .single img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.images-grid .multiple {
  grid-template-columns: repeat(3, 1fr);
}

.images-grid .multiple img {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.item-info {
  padding: 12px;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-name {
  font-size: 16px;
  font-weight: 600;
  color: #323233;
}

.item-details {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.brand,
.platform {
  font-size: 13px;
  color: #969799;
  background: #f7f8fa;
  padding: 2px 8px;
  border-radius: 4px;
}

.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-info {
  display: flex;
  align-items: center;
}

.purchase-price {
  font-size: 16px;
  font-weight: 600;
  color: #ee0a24;
}

.days-info {
  font-size: 12px;
  color: #969799;
  margin-left: 4px;
}

.estimate-info {
  display: flex;
  align-items: center;
  gap: 4px;
}

.estimate-label {
  font-size: 12px;
  color: #969799;
}

.estimate-price {
  font-size: 14px;
  color: #07c160;
}

.load-more {
  text-align: center;
  padding: 16px;
  color: #969799;
  font-size: 14px;
  cursor: pointer;
}

.publish-btn {
  position: fixed;
  right: 16px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  cursor: pointer;
}
</style>
