<template>
  <div class="categories-container">
    <van-nav-bar title="分类管理" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <!-- 提示 -->
      <div class="tip">点击一级分类可展开/收起二级分类</div>
      
      <van-cell-group inset v-if="categories.length > 0">
        <van-collapse v-model="activeNames">
          <van-collapse-item 
            v-for="cat in categories" 
            :key="cat.id" 
            :name="cat.id"
            :title="cat.name"
          >
            <template #value>
              <div class="cat-actions" @click.stop>
                <span class="add-sub" @click="showAddSubCategory(cat.id)">+添加</span>
                <span class="edit-cat" @click="editCategory(cat)">修改</span>
              </div>
            </template>
            
            <!-- 二级分类列表 -->
            <div class="sub-categories" v-if="cat.children && cat.children.length > 0">
              <div 
                v-for="child in cat.children" 
                :key="child.id" 
                class="sub-cat-item"
              >
                <span>{{ child.name }}</span>
                <van-icon name="edit" size="14" @click="editCategory(child)" />
              </div>
            </div>
            <div v-else class="no-sub">暂无二级分类</div>
          </van-collapse-item>
        </van-collapse>
      </van-cell-group>
      
      <van-empty v-else description="暂无分类" />
      
      <!-- 添加一级分类按钮 -->
      <div class="add-btn">
        <van-button icon="plus" type="primary" block round @click="showAddDialog = true">
          添加一级分类
        </van-button>
      </div>
    </div>
    
    <!-- 添加一级分类对话框 -->
    <van-dialog v-model:show="showAddDialog" title="添加一级分类" show-cancel-button @confirm="handleAddCategory">
      <van-field v-model="newCategoryName" placeholder="请输入分类名称" />
    </van-dialog>
    
    <!-- 添加二级分类对话框 -->
    <van-dialog v-model:show="showAddSubDialog" title="添加二级分类" show-cancel-button @confirm="handleAddSubCategory">
      <van-field v-model="newSubCategoryName" placeholder="请输入二级分类名称" />
    </van-dialog>
    
    <!-- 修改分类对话框 -->
    <van-dialog v-model:show="showEditDialog" title="修改分类" show-cancel-button @confirm="handleEditCategory">
      <van-field v-model="editCategoryName" placeholder="请输入分类名称" />
    </van-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import { showToast } from 'vant'

const categories = ref([])
const activeNames = ref([])
const showAddDialog = ref(false)
const showAddSubDialog = ref(false)
const showEditDialog = ref(false)
const newCategoryName = ref('')
const newSubCategoryName = ref('')
const editCategoryName = ref('')
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

// 添加一级分类
const handleAddCategory = async () => {
  if (!newCategoryName.value) return
  try {
    await createCategory({ name: newCategoryName.value, parent_id: null })
    showToast({ message: '添加成功', position: 'top' })
    newCategoryName.value = ''
    fetchCategories()
  } catch (error) {
    showToast({ message: error.message || '添加失败', position: 'top' })
  }
}

// 显示添加二级分类对话框
const showAddSubCategory = (parentId) => {
  currentParentId.value = parentId
  newSubCategoryName.value = ''
  showAddSubDialog.value = true
}

// 添加二级分类
const handleAddSubCategory = async () => {
  if (!newSubCategoryName.value || !currentParentId.value) return
  try {
    await createCategory({ 
      name: newSubCategoryName.value, 
      parent_id: currentParentId.value 
    })
    showToast({ message: '添加成功', position: 'top' })
    newSubCategoryName.value = ''
    fetchCategories()
  } catch (error) {
    showToast({ message: error.message || '添加失败', position: 'top' })
  }
}

// 修改分类
const editCategory = (cat) => {
  currentEditId.value = cat.id
  editCategoryName.value = cat.name
  showEditDialog.value = true
}

const handleEditCategory = async () => {
  if (!editCategoryName.value || !currentEditId.value) return
  try {
    await updateCategory(currentEditId.value, { name: editCategoryName.value })
    showToast({ message: '修改成功', position: 'top' })
    editCategoryName.value = ''
    fetchCategories()
  } catch (error) {
    showToast({ message: error.message || '修改失败', position: 'top' })
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

.tip {
  padding: 12px 16px;
  font-size: 12px;
  color: #969799;
}

.cat-actions {
  display: flex;
  gap: 12px;
}

.add-sub, .edit-cat {
  font-size: 12px;
  color: #07c160;
  cursor: pointer;
}

.sub-categories {
  padding: 8px 0;
}

.sub-cat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  font-size: 14px;
  color: #646566;
}

.sub-cat-item:active {
  background: #f7f8fa;
}

.no-sub {
  padding: 8px 12px;
  font-size: 12px;
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
