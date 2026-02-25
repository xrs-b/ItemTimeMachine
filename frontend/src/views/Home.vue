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
        
        <div v-else class="items-list">
          <!-- 朋友圈风格卡片 -->
          <div v-for="item in items" :key="item.id" class="item-card" @click="$router.push(`/item/${item.id}`)">
            <!-- 用户信息区域 -->
            <div class="card-header">
              <div class="user-info">
                <van-image
                  round
                  width="40"
                  height="40"
                  src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
                />
                <div class="user-detail">
                  <span class="item-name">{{ item.name }}</span>
                  <span class="publish-time">{{ item.days_since_purchase }}天前</span>
                </div>
              </div>
            </div>
            
            <!-- 文字内容区域 -->
            <div class="card-content">
              <div class="info-row" v-if="item.category_name">
                <span class="label">分类：</span>
                <span class="value">{{ item.category_name }}</span>
              </div>
              <div class="info-row" v-if="item.brand">
                <span class="label">品牌：</span>
                <span class="value">{{ item.brand }}</span>
              </div>
              <div class="info-row">
                <span class="label">购买日期：</span>
                <span class="value">{{ formatDate(item.purchase_date) }}</span>
              </div>
              <div class="info-row">
                <span class="label">价格：</span>
                <span class="value price">¥{{ item.purchase_price }}</span>
              </div>
              <div class="info-row" v-if="item.platform">
                <span class="label">平台：</span>
                <span class="value">{{ item.platform }}</span>
              </div>
              <div class="info-row" v-if="item.days_since_purchase">
                <span class="label">已购：</span>
                <span class="value">{{ item.days_since_purchase }}天</span>
              </div>
              <div class="info-row" v-if="item.estimated_value">
                <span class="label">二手估价：</span>
                <span class="value estimate">¥{{ item.estimated_value }}</span>
              </div>
              <div class="info-row" v-if="item.description">
                <span class="label">备注：</span>
                <span class="value">{{ item.description }}</span>
              </div>
            </div>
            
            <!-- 九宫格图片区域 -->
            <div class="images-grid" v-if="item.images && item.images.length > 0">
              <div 
                v-for="(img, idx) in item.images" 
                :key="img.id"
                class="image-item"
                :class="{ 
                  'single': item.images.length === 1,
                  'four': item.images.length === 4,
                  'two': item.images.length === 2
                }"
              >
                <img :src="img.thumbnail_url || img.image_url" :alt="item.name" />
              </div>
            </div>
            
            <!-- 底部操作区域 -->
            <div class="card-footer">
              <span class="location" v-if="item.platform">{{ item.platform }}</span>
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

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

const fetchItems = async (reset = false) => {
  if (reset) {
    page.value = 1
    items.value = []
  }
  
  loading.value = true
  try {
    const res = await getItems({ page: page.value, page_size: 20 })
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
    const res = await getItems({ page: page.value, page_size: 20 })
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

.items-list {
  padding: 12px;
}

/* 朋友圈风格卡片 */
.item-card {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
}

.card-header {
  padding: 12px;
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
}

.publish-time {
  font-size: 12px;
  color: #969799;
}

.card-content {
  padding: 0 12px 12px;
}

.info-row {
  display: flex;
  font-size: 14px;
  line-height: 1.8;
  color: #646566;
}

.info-row .label {
  width: 70px;
  flex-shrink: 0;
}

.info-row .value {
  flex: 1;
}

.info-row .value.price {
  color: #ee0a24;
  font-weight: 600;
}

.info-row .value.estimate {
  color: #07c160;
}

/* 九宫格图片 */
.images-grid {
  display: grid;
  gap: 2px;
  padding: 0 12px;
}

.images-grid .image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 单张图片 */
.images-grid .single {
  grid-template-columns: 1fr;
  max-height: 300px;
}

/* 2张图片 */
.images-grid .two {
  grid-template-columns: repeat(2, 1fr);
  max-height: 200px;
}

/* 4张图片 */
.images-grid .four {
  grid-template-columns: repeat(2, 1fr);
  max-height: 200px;
}

/* 3、5、6、7、8、9张图片 */
.images-grid:not(.single):not(.two):not(.four) {
  grid-template-columns: repeat(3, 1fr);
  max-height: 240px;
}

.card-footer {
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.location {
  font-size: 12px;
  color: #969799;
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
  z-index: 100;
}
</style>
