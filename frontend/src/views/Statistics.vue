<template>
  <div class="stats-container">
    <van-nav-bar title="数据统计" fixed />
    
    <div class="content">
      <!-- 总体统计 -->
      <div class="summary-cards">
        <div class="card">
          <span class="label">总花费</span>
          <span class="value">¥{{ summary.total_expense || 0 }}</span>
        </div>
        <div class="card">
          <span class="label">物品数量</span>
          <span class="value">{{ summary.total_items || 0 }}</span>
        </div>
        <div class="card">
          <span class="label">二手估价</span>
          <span class="value">¥{{ summary.total_estimated_value || 0 }}</span>
        </div>
        <div class="card">
          <span class="label">折旧</span>
          <span class="value depreciation">¥{{ summary.depreciation || 0 }}</span>
        </div>
      </div>
      
      <!-- 按分类统计 -->
      <div class="chart-section">
        <h3 class="section-title">分类统计</h3>
        <div class="chart-placeholder" v-if="categoryData.length > 0">
          <div v-for="item in categoryData" :key="item.category" class="chart-item">
            <span class="cat-name">{{ item.category }}</span>
            <span class="cat-count">{{ item.count }}件</span>
            <span class="cat-total">¥{{ item.total }}</span>
          </div>
        </div>
        <van-empty v-else description="暂无数据" />
      </div>
      
      <!-- 按平台统计 -->
      <div class="chart-section">
        <h3 class="section-title">平台分布</h3>
        <div class="chart-placeholder" v-if="platformData.length > 0">
          <div v-for="item in platformData" :key="item.platform" class="chart-item">
            <span class="cat-name">{{ item.platform }}</span>
            <span class="cat-count">{{ item.count }}件</span>
            <span class="cat-total">¥{{ item.total }}</span>
          </div>
        </div>
        <van-empty v-else description="暂无数据" />
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
import { getSummary, getCategoryStats, getPlatformStats } from '@/api/statistics'

const activeTab = ref(1)
const summary = ref({})
const categoryData = ref([])
const platformData = ref([])

const fetchData = async () => {
  try {
    const [sum, cat, plat] = await Promise.all([
      getSummary(),
      getCategoryStats(),
      getPlatformStats()
    ])
    summary.value = sum
    categoryData.value = cat || []
    platformData.value = plat || []
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.stats-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding-bottom: 50px;
}

.content {
  padding-top: 46px;
  padding: 12px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
}

.card .label {
  display: block;
  font-size: 13px;
  color: #969799;
  margin-bottom: 8px;
}

.card .value {
  font-size: 20px;
  font-weight: 600;
  color: #323233;
}

.card .value.depreciation {
  color: #ee0a24;
}

.chart-section {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  margin-top: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.chart-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}

.cat-name {
  flex: 1;
}

.cat-count {
  width: 60px;
  text-align: center;
  color: #969799;
}

.cat-total {
  width: 80px;
  text-align: right;
  color: #ee0a24;
}
</style>
