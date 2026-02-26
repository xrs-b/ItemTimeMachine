<template>
  <div class="categories-container">
    <van-nav-bar title="分类管理" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <!-- 提示 -->
      <div class="tip">点击分类可展开/收起，点击右侧按钮可添加或修改</div>
      
      <van-cell-group inset v-if="categories.length > 0">
        <van-swipe-cell v-for="cat in categories" :key="cat.id" :right-width="65">
          <div class="cat-item" @click="toggleCategory(cat.id)">
            <div class="cat-info">
              <van-icon 
                v-if="cat.children && cat.children.length > 0" 
                :name="expandedIds.includes(cat.id) ? 'arrow-down' : 'arrow'" 
                size="14" 
                class="expand-arrow"
              />
              <span class="cat-name">{{ cat.name }}</span>
            </div>
            <div class="cat-actions" @click.stop>
              <van-button size="small" hairline type="primary" @click="showAddSubCategory(cat.id)">+二级</van-button>
              <van-button size="small" hairline @click="editCategory(cat)">改</van-button>
            </div>
          </div>
          
          <!-- 二级分类 -->
          <div v-if="expandedIds.includes(cat.id) && cat.children && cat.children.length > 0" class="sub-list">
            <div v-for="child in cat.children" :key="child.id" class="sub-item">
              <span>{{ child.name }}</span>
              <van-button size="small" hairline @click="editCategory(child)">改</van-button>
            </div>
          </div>
          
          <template #right>
            <van-button 
              square 
              type="danger" 
              @click="handleDeleteCategory(cat.id)"
            >
              删除
            </van-button>
          </template>
        </van-swipe-cell>
      </van-cell-group>
      
      <van-empty v-else description="暂无分类" />
      
      <!-- 添加一级分类按钮 -->
      <div class="add-btn">
        <van-button icon="plus" type="primary" block round @click="showAddDialog = true">
          添加一级分类
        </van-button>
      </div>
    </div>
    
    <!-- 添加/编辑对话框 -->
    <van-dialog v-model:show="showDialog" :title="isEdit ? '修改分类' : '添加分类'" show-cancel-button @confirm="handleConfirm">
      <van-field v-model="dialogName" placeholder="请输入分类名称" />
    </van-dialog>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import { showToast, showConfirmDialog } from 'vant'

const categories = ref([])
const expandedIds = ref([])
const showDialog = ref(false)
const dialogName = ref('')
const isEdit = ref(false)
const currentParentId = ref(null)
const currentEditId = ref(null)

const fetchCategories = async () => {
  try {
    const res = await getCategories()
    categories.value = res || []
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  }
}

const toggleCategory = (id) => {
  const idx = expandedIds.value.indexOf(id)
  if (idx > -1) {
    expandedIds.value.splice(idx, 1)
  } else {
    expandedIds.value.push(id)
  }
}

const showAddDialog = () => {
  isEdit.value = false
  currentParentId.value = null
  dialogName.value = ''
  showDialog.value = true
}

const showAddSubCategory = (parentId) => {
  isEdit.value = false
  currentParentId.value = parentId
  currentEditId.value = null
  dialogName.value = ''
  showDialog.value = true
}

const editCategory = (cat) => {
  isEdit.value = true
  currentEditId.value = cat.id
  currentParentId.value = cat.parent_id
  dialogName.value = cat.name
  showDialog.value = true
}

const handleConfirm = async () => {
  if (!dialogName.value) return
  
  try {
    if (isEdit.value) {
      await updateCategory(currentEditId.value, { name: dialogName.value })
      showToast({ message: '修改成功', position: 'top' })
    } else {
      await createCategory({ 
        name: dialogName.value, 
        parent_id: currentParentId.value 
      })
      showToast({ message: '添加成功', position: 'top' })
    }
    dialogName.value = ''
    fetchCategories()
  } catch (error) {
    showToast({ message: error.message || '操作失败', position: 'top' })
  }
}

const handleDeleteCategory = async (id) => {
  try {
    await showConfirmDialog({ title: '确认删除', message: '确定要删除这个分类吗？' })
    await deleteCategory(id)
    showToast({ message: '删除成功', position: 'top' })
    fetchCategories()
  } catch (error) {
    if (error !== 'cancel') {
      showToast({ message: error.message || '删除失败', position: 'top' })
    }
  }
}

fetchCategories()
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

.tip {
  padding: 12px 16px;
  font-size: 12px;
  color: #969799;
}

.cat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fff;
}

.cat-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.expand-arrow {
  color: #969799;
}

.cat-name {
  font-size: 15px;
}

.cat-actions {
  display: flex;
  gap: 8px;
}

.sub-list {
  background: #f7f8fa;
  padding: 8px 0;
}

.sub-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px 10px 32px;
  font-size: 14px;
  color: #646566;
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
