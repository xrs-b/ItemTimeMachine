<template>
  <div class="add-item-container">
    <van-nav-bar title="添加物品" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <van-form @submit="onSubmit">
        <!-- 物品名称 -->
        <van-cell-group inset>
          <van-field
            v-model="form.name"
            name="name"
            label="物品名称"
            placeholder="请输入物品名称"
          />
        </van-cell-group>
        
        <!-- 分类选择 -->
        <van-cell-group inset>
          <van-field
            is-link
            readonly
            clickable
            label="分类"
            placeholder="请选择分类"
            :model-value="selectedCategoryName"
            @click="showCategoryPicker = true"
          />
        </van-cell-group>
        
        <!-- 品牌 -->
        <van-cell-group inset>
          <van-field
            v-model="form.brand"
            name="brand"
            label="品牌"
            placeholder="请输入品牌（选填）"
          />
        </van-cell-group>
        
        <!-- 购买日期 -->
        <van-cell-group inset>
          <van-field
            is-link
            readonly
            clickable
            label="购买日期"
            placeholder="请选择购买日期"
            :model-value="form.purchase_date"
            @click="showDatePicker = true"
          />
        </van-cell-group>
        
        <!-- 购买价格 -->
        <van-cell-group inset>
          <van-field
            v-model="form.purchase_price"
            type="digit"
            name="purchase_price"
            label="购买价格"
            placeholder="请输入购买价格"
          >
            <template #right-icon>¥</template>
          </van-field>
        </van-cell-group>
        
        <!-- 购买平台 -->
        <van-cell-group inset>
          <van-field
            is-link
            readonly
            clickable
            label="购买平台"
            placeholder="请选择购买平台"
            :model-value="form.platform"
            @click="showPlatformPicker = true"
          />
        </van-cell-group>
        
        <!-- 二手转卖价格 -->
        <van-cell-group inset>
          <van-field
            v-model="form.second_hand_price"
            type="digit"
            name="second_hand_price"
            label="二手转卖价"
            placeholder="请输入二手转卖价格（选填）"
          >
            <template #right-icon>¥</template>
          </van-field>
        </van-cell-group>
        
        <!-- 描述 -->
        <van-cell-group inset>
          <van-field
            v-model="form.description"
            type="textarea"
            name="description"
            label="备注"
            placeholder="请输入物品描述（选填）"
            rows="3"
            autosize
          />
        </van-cell-group>
        
        <!-- 图片上传 -->
        <van-cell-group inset>
          <div class="image-upload">
            <div class="upload-title">图片（最多9张）</div>
            <van-uploader
              v-model="fileList"
              multiple
              :max-count="9"
              :after-read="afterRead"
              @delete="onDelete"
            />
          </div>
        </van-cell-group>
        
        <!-- 提交按钮 -->
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" :loading="loading">
            保存
          </van-button>
        </div>
      </van-form>
      
      <!-- 分类选择器 -->
      <van-popup v-model:show="showCategoryPicker" position="bottom">
        <van-cascader
          v-model="categoryCascader"
          title="选择分类"
          :options="categoryOptions"
          @close="showCategoryPicker = false"
          @finish="onCategoryFinish"
        />
      </van-popup>
      
      <!-- 日期选择器 -->
      <van-popup v-model:show="showDatePicker" position="bottom">
        <van-date-picker
          v-model="currentDate"
          type="date"
          title="选择日期"
          :min-date="minDate"
          :max-date="maxDate"
          @confirm="onDateConfirm"
          @cancel="showDatePicker = false"
        />
      </van-popup>
      
      <!-- 平台选择器 -->
      <van-popup v-model:show="showPlatformPicker" position="bottom">
        <van-picker
          title="选择平台"
          :columns="platformColumns"
          value-key="text"
          @confirm="onPlatformConfirm"
          @cancel="showPlatformPicker = false"
        />
      </van-popup>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createItem, uploadImage } from '@/api/items'
import { getCategories } from '@/api/categories'
import { showToast } from 'vant'

const router = useRouter()

const form = ref({
  name: '',
  category_id: null,
  brand: '',
  purchase_date: '',
  purchase_price: '',
  platform: '',
  second_hand_price: '',
  description: ''
})

const fileList = ref([])
const loading = ref(false)
const showCategoryPicker = ref(false)
const showDatePicker = ref(false)
const showPlatformPicker = ref(false)
const categoryCascader = ref('')
const selectedCategoryName = ref('')

// 初始化日期为今天
const today = new Date()
const currentDate = ref([
  String(today.getFullYear()),
  String(today.getMonth() + 1).padStart(2, '0'),
  String(today.getDate()).padStart(2, '0')
])
form.value.purchase_date = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

const minDate = new Date(2000, 0, 1)
const maxDate = new Date()

// 分类数据 - 扁平化结构用于Cascader
// 分类数据 - 从API动态加载
const categoryOptions = ref([])

const loadCategories = async () => {
  try {
    const res = await getCategories()
    categoryOptions.value = (res || []).map(cat => ({
      text: cat.name,
      value: String(cat.id),
      children: cat.children ? cat.children.map(child => ({
        text: child.name,
        value: String(child.id)
      })) : []
    }))
  } catch (error) {
    console.error('加载分类失败', error)
  }
}

const platformColumns = [
  { text: '淘宝', value: '淘宝' },
  { text: '京东', value: '京东' },
  { text: '天猫', value: '天猫' },
  { text: '拼多多', value: '拼多多' },
  { text: '小红书', value: '小红书' },
  { text: '抖音', value: '抖音' },
  { text: '闲鱼', value: '闲鱼' },
  { text: '线下门店', value: '线下门店' },
  { text: '官网', value: '官网' },
  { text: '其他', value: '其他' }
]

const onCategoryFinish = ({ selectedOptions }) => {
  const lastOption = selectedOptions[selectedOptions.length - 1]
  form.value.category_id = parseInt(lastOption.value)
  selectedCategoryName.value = lastOption.text
  showCategoryPicker.value = false
}

const onDateConfirm = ({ selectedValues }) => {
  form.value.purchase_date = selectedValues.join('-')
  showDatePicker.value = false
}

const onPlatformConfirm = ({ selectedOptions }) => {
  if (selectedOptions && selectedOptions.length > 0) {
    form.value.platform = selectedOptions[0].text || ''
  }
  showPlatformPicker.value = false
}

const afterRead = (file) => {
  // 文件上传处理
}

const onDelete = (file) => {
  // 文件删除处理
}

const onSubmit = async () => {
  if (!form.value.name) {
    showToast({ message: '请输入物品名称', position: 'top' })
    return
  }
  if (!form.value.purchase_price) {
    showToast({ message: '请输入购买价格', position: 'top' })
    return
  }
  
  loading.value = true
  try {
    // 创建物品
    const itemData = {
      name: form.value.name,
      category_id: form.value.category_id,
      brand: form.value.brand || null,
      purchase_date: form.value.purchase_date,
      purchase_price: parseFloat(form.value.purchase_price),
      platform: form.value.platform || null,
      second_hand_price: form.value.second_hand_price ? parseFloat(form.value.second_hand_price) : null,
      description: form.value.description || null
    }
    
    const item = await createItem(itemData)
    
    // 上传图片
    for (const file of fileList.value) {
      if (file.file) {
        await uploadImage(item.id, file.file)
      }
    }
    
    showToast({ message: '添加成功', position: 'top' })
    router.replace('/')
  } catch (error) {
    showToast({ message: error.message || '添加失败', position: 'top' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.add-item-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 24px;
}

.image-upload {
  padding: 12px 0;
}

.upload-title {
  font-size: 14px;
  color: #646566;
  padding: 0 16px;
  margin-bottom: 8px;
}

.submit-btn {
  padding: 24px 16px;
}
</style>
