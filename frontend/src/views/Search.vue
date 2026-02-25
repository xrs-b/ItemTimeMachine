<template>
  <div class="search-container">
    <van-nav-bar title="搜索" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <!-- 搜索框 -->
      <div class="search-bar">
        <van-search
          v-model="searchText"
          placeholder="请输入物品名称"
          show-action
          @search="onSearch"
        >
          <template #action>
            <div @click="onSearch">搜索</div>
          </template>
        </van-search>
      </div>
      
      <!-- 筛选 -->
      <div class="filter-section">
        <van-dropdown-menu>
          <van-dropdown-item v-model="selectedCategory" :options="categories" title="分类" />
          <van-dropdown-item v-model="selectedBrand" :options="brands" title="品牌" />
        </van-dropdown-menu>
      </div>
      
      <!-- 结果列表 -->
      <div class="results" v-if="results.length > 0">
        <div v-for="item in results" :key="item.id" class="result-item" @click="$router.push(`/item/${item.id}`)">
          <div class="item-info">
            <span class="item-name">{{ item.name }}</span>
            <span class="item-price">¥{{ item.purchase_price }}</span>
          </div>
          <div class="item-meta">
            <span v-if="item.brand">{{ item.brand }}</span>
            <span>{{ item.purchase_date }}</span>
          </div>
        </div>
      </div>
      
      <van-empty v-else-if="searched" description="未找到相关物品" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getItems } from '@/api/items'

const searchText = ref('')
const selectedCategory = ref(null)
const selectedBrand = ref(null)
const results = ref([])
const searched = ref(false)

const categories = [
  { text: '全部分类', value: null },
  { text: '数码产品', value: 1 },
  { text: '衣服', value: 2 },
  { text: '化妆品', value: 3 }
]

const brands = [
  { text: '全部品牌', value: null },
  { text: 'Apple', value: 'Apple' },
  { text: '华为', value: '华为' },
  { text: '小米', value: '小米' }
]

const onSearch = async () => {
  searched.value = true
  try {
    const params = { search: searchText.value }
    if (selectedCategory.value) params.category_id = selectedCategory.value
    if (selectedBrand.value) params.brand = selectedBrand.value
    
    const res = await getItems(params)
    results.value = res.items || []
  } catch (error) {
    console.error(error)
  }
}
</script>

<style scoped>
.search-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
}

.search-bar {
  background: #fff;
}

.filter-section {
  background: #fff;
  margin-top: 8px;
}

.results {
  padding: 12px;
}

.result-item {
  background: #fff;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  cursor: pointer;
}

.item-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.item-name {
  font-size: 16px;
  font-weight: 500;
}

.item-price {
  color: #ee0a24;
}

.item-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #969799;
}
</style>
