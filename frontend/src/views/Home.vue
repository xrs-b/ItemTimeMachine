<template>
  <div class="home-container">
    <!-- 顶部导航 -->
    <van-nav-bar title="物品时光机" fixed>
      <template #right>
        <van-icon name="search" size="18" @click="$router.push('/search')" />
      </template>
    </van-nav-bar>
    
    <!-- 图片预览组件 -->
    <van-image-preview
      v-model:show="showPreview"
      :images="previewImages"
      :start-position="previewIndex"
      @close="showPreview = false"
    />
    
    <!-- 内容区域 -->
    <div class="content">
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
        <div v-if="loading && items.length === 0" class="loading-state">
          <van-loading size="24px">加载中...</van-loading>
        </div>
        
        <div v-else-if="items.length === 0" class="empty-state">
          <van-empty description="还没有记录任何物品">
            <van-button type="primary" round @click="$router.push('/add')">
              添加第一个物品
            </van-button>
          </van-empty>
        </div>
        
        <div v-else class="timeline-list">
          <!-- 朋友圈风格卡片 -->
          <div v-for="item in items" :key="item.id" class="timeline-card">
            <!-- 头像区域 -->
            <div class="card-avatar">
              <van-image
                round
                width="40"
                height="40"
                src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
              />
            </div>
            
            <!-- 内容区域 -->
            <div class="card-body">
              <!-- 用户名和时间 -->
              <div class="card-header">
                <span class="username">{{ item.name }}</span>
                <span class="time">{{ item.days_since_purchase }}天前</span>
              </div>
              
              <!-- 文字内容 -->
              <div class="card-content">
                <div class="info-item" v-if="item.category_name">
                  <span class="label">分类：</span>
                  <span class="value">{{ item.category_name }}</span>
                </div>
                <div class="info-item" v-if="item.brand">
                  <span class="label">品牌：</span>
                  <span class="value">{{ item.brand }}</span>
                </div>
                <div class="info-item">
                  <span class="label">购买日期：</span>
                  <span class="value">{{ item.purchase_date }}</span>
                </div>
                <div class="info-item">
                  <span class="label">价格：</span>
                  <span class="value price">¥{{ item.purchase_price }}</span>
                </div>
                <div class="info-item" v-if="item.platform">
                  <span class="label">平台：</span>
                  <span class="value">{{ item.platform }}</span>
                </div>
                <div class="info-item" v-if="item.estimated_value">
                  <span class="label">二手估价：</span>
                  <span class="value estimate">¥{{ item.estimated_value }}</span>
                </div>
                <div class="info-item" v-if="item.description">
                  <span class="label">备注：</span>
                  <span class="value">{{ item.description }}</span>
                </div>
              </div>
              
              <!-- 九宫格图片 -->
              <div class="card-images" v-if="item.images && item.images.length > 0">
                <div class="images-grid" :class="'grid-' + Math.min(item.images.length, 9)">
                  <div 
                    v-for="(img, idx) in item.images.slice(0, 9)" 
                    :key="img.id || idx"
                    class="image-wrapper"
                    @click="openPreview(item, idx)"
                  >
                    <img 
                      :src="img.image_url" 
                      :alt="item.name"
                    />
                  </div>
                </div>
              </div>
              
              <!-- 底部来源和修改按钮 -->
              <div class="card-footer">
                <span class="source" v-if="item.platform">{{ item.platform }}</span>
                <span class="edit-btn" @click.stop="$router.push(`/item/${item.id}/edit`)">修改</span>
              </div>
            </div>
          </div>
          
          <!-- 加载更多 -->
          <div class="load-more" v-if="hasMore" @click="loadMore">
            <span v-if="loadingMore">加载中...</span>
            <span v-else>点击加载更多</span>
          </div>
        </div>
      </van-pull-refresh>
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
const refreshing = ref(false)
const page = ref(1)
const hasMore = ref(true)

// 图片预览
const showPreview = ref(false)
const previewImages = ref([])
const previewIndex = ref(0)

const openPreview = (item, idx) => {
  if (!item.images || item.images.length === 0) return
  
  const images = item.images
    .filter(img => img && img.image_url)
    .map(img => img.image_url)
  
  if (images.length === 0) return
  
  previewImages.value = images
  previewIndex.value = idx
  showPreview.value = true
}

const fetchItems = async (reset = false) => {
  if (reset) {
    page.value = 1
    items.value = []
  }
  
  loading.value = true
  try {
    const res = await getItems({ page: page.value, page_size: 10 })
    if (reset) {
      items.value = res.items || []
    } else {
      items.value = [...items.value, ...(res.items || [])]
    }
    hasMore.value = res.has_more
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  
  loadingMore.value = true
  try {
    page.value++
    const res = await getItems({ page: page.value, page_size: 10 })
    items.value = [...items.value, ...(res.items || [])]
    hasMore.value = res.has_more
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  } finally {
    loadingMore.value = false
  }
}

const onRefresh = () => {
  refreshing.value = true
  fetchItems(true)
}

onMounted(() => {
  fetchItems(true)
})
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 60px;
}

.loading-state,
.empty-state {
  padding: 100px 0;
  text-align: center;
}

.timeline-list {
  padding: 0;
}

/* 朋友圈风格卡片 */
.timeline-card {
  background: #fff;
  margin-bottom: 8px;
  display: flex;
  padding: 12px;
}

.card-avatar {
  flex-shrink: 0;
  margin-right: 12px;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.username {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
}

.time {
  font-size: 12px;
  color: #999;
}

.card-content {
  margin-bottom: 8px;
}

.info-item {
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.info-item .label {
  color: #666;
}

.info-item .value.price {
  color: #e64340;
  font-weight: 500;
}

.info-item .value.estimate {
  color: #07c160;
  font-weight: 500;
}

/* 九宫格图片 */
.card-images {
  margin-top: 8px;
}

.images-grid {
  display: grid;
  gap: 4px;
}

/* 1张图片 */
.images-grid.grid-1 {
  grid-template-columns: 1fr;
  max-width: 200px;
}

/* 2张图片 */
.images-grid.grid-2 {
  grid-template-columns: repeat(2, 1fr);
  max-width: 220px;
}

/* 3张图片 */
.images-grid.grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

/* 4张图片 */
.images-grid.grid-4 {
  grid-template-columns: repeat(2, 1fr);
}

/* 5-9张图片 */
.images-grid.grid-5,
.images-grid.grid-6,
.images-grid.grid-7,
.images-grid.grid-8,
.images-grid.grid-9 {
  grid-template-columns: repeat(3, 1fr);
}

.image-wrapper {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 4px;
  cursor: pointer;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-footer {
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.source {
  font-size: 12px;
  color: #999;
}

.edit-btn {
  font-size: 12px;
  color: #07c160;
  cursor: pointer;
}

.load-more {
  text-align: center;
  padding: 16px;
  color: #999;
  font-size: 14px;
  cursor: pointer;
  background: #f5f5f5;
}

.publish-btn {
  position: fixed;
  right: 16px;
  bottom: 80px;
  width: 56px;
  height: 56px;
  background: #07c160;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(7, 193, 96, 0.4);
  cursor: pointer;
  z-index: 100;
}
</style>
