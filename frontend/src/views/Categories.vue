<template>
  <div class="categories-container">
    <van-nav-bar title="分类管理" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <van-cell-group inset>
        <van-cell v-for="cat in categories" :key="cat.id" is-link @click="showCategory(cat)">
          <template #title>
            <span class="cat-name">{{ cat.name }}</span>
          </template>
          <template #value>
            <span class="cat-count">{{ cat.children ? cat.children.length : 0 }}个子分类</span>
          </template>
        </van-cell>
      </van-cell-group>
      
      <div class="add-btn">
        <van-button icon="plus" type="primary" block round @click="showAddDialog = true">
          添加分类
        </van-button>
      </div>
    </div>
    
    <!-- 添加分类对话框 -->
    <van-dialog
      v-model:show="showAddDialog"
      title="添加分类"
      show-cancel-button
      @confirm="handleAdd"
    >
      <van-field v-model="newCategoryName" placeholder="请输入分类名称" />
    </van-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, createCategory } from '@/api/categories'
import { showToast } from 'vant'

const categories = ref([])
const showAddDialog = ref(false)
const newCategoryName = ref('')

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res || []
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  }
}

const showCategory = (cat) => {
  // TODO: 显示子分类
  console.log('showCategory', cat)
}

const handleAdd = async () => {
  if (!newCategoryName.value) return
  
  try {
    await createCategory({ name: newCategoryName.value })
    showToast({ message: '添加成功', position: 'top' })
    newCategoryName.value = ''
    fetchCategories()
  } catch (error) {
    showToast({ message: error.message || '添加失败', position: 'top' })
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.categories-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 80px;
}

.cat-name {
  font-size: 16px;
}

.cat-count {
  font-size: 13px;
  color: #969799;
}

.add-btn {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 16px;
}
</style>
