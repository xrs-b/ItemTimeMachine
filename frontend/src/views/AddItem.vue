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
            :rules="[{ required: true, message: '请输入物品名称' }]"
          />
        </van-cell-group>
        
        <!-- 分类选择 -->
        <van-cell-group inset>
          <van-field
            is-link
            readonly
            clickable
            name="category_id"
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
            name="purchase_date"
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
            :rules="[{ required: true, message: '请输入购买价格' }]"
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
            name="platform"
            label="购买平台"
            placeholder="请选择购买平台"
            :model-value="form.platform"
            @click="showPlatformPicker = true"
          />
        </van-cell-group>
        
        <!-- 描述 -->
        <van-cell-group inset>
          <van-field
            v-model="form.description"
            type="textarea"
            name="description"
            label="描述"
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
        <van-picker
          :columns="categoryColumns"
          @confirm="onCategoryConfirm"
          @cancel="showCategoryPicker = false"
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
          :columns="platformColumns"
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
import { createItem } from '@/api/items'
import { showToast } from 'vant'

const router = useRouter()

const form = ref({
  name: '',
  category_id: null,
  brand: '',
  purchase_date: '',
  purchase_price: '',
  platform: '',
  description: ''
})

const fileList = ref([])
const loading = ref(false)
const showCategoryPicker = ref(false)
const showDatePicker = ref(false)
const showPlatformPicker = ref(false)

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

// 分类数据
const categories = ref([
  { id: 1, name: '数码产品', children: [
    { id: 11, name: '手机' },
    { id: 12, name: '电脑' },
    { id: 13, name: '相机' },
    { id: 14, name: '镜头' },
    { id: 15, name: '耳机' },
    { id: 16, name: '智能手表' },
    { id: 17, name: '游戏机' },
    { id: 18, name: '其他数码' }
  ]},
  { id: 2, name: '衣服', children: [
    { id: 21, name: 'JK制服' },
    { id: 22, name: '洛丽塔' },
    { id: 23, name: '汉服' },
    { id: 24, name: '上装' },
    { id: 25, name: '下装' },
    { id: 26, name: '外套' },
    { id: 27, name: '鞋' },
    { id: 28, name: '配饰' }
  ]},
  { id: 3, name: '化妆品', children: [
    { id: 31, name: '底妆' },
    { id: 32, name: '彩妆' },
    { id: 33, name: '护肤' },
    { id: 34, name: '香水' },
    { id: 35, name: '美容工具' }
  ]},
  { id: 4, name: '其他', children: [
    { id: 41, name: '书籍' },
    { id: 42, name: '乐器' },
    { id: 43, name: '运动器材' },
    { id: 44, name: '家具' },
    { id: 45, name: '其他' }
  ]}
])

const categoryColumns = computed(() => {
  return categories.value.map(cat => ({
    text: cat.name,
    children: cat.children.map(child => ({ text: child.name, value: child.id }))
  }))
})

const platformColumns = [
  { text: '淘宝' },
  { text: '京东' },
  { text: '天猫' },
  { text: '拼多多' },
  { text: '小红书' },
  { text: '抖音' },
  { text: '闲鱼' },
  { text: '线下门店' },
  { text: '官网' },
  { text: '其他' }
]

const selectedCategoryName = ref('')

const onCategoryConfirm = ({ selectedOptions }) => {
  // 处理级联选择器的返回值
  if (selectedOptions && selectedOptions.length >= 2) {
    const parent = selectedOptions[0]
    const child = selectedOptions[1]
    if (child && child.value) {
      form.value.category_id = child.value
      selectedCategoryName.value = child.text
    } else if (parent && parent.value) {
      form.value.category_id = parent.value
      selectedCategoryName.value = parent.text
    }
  }
  showCategoryPicker.value = false
}

const onDateConfirm = ({ selectedValues }) => {
  const dateStr = selectedValues.join('-')
  form.value.purchase_date = dateStr
  currentDate.value = selectedValues
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
  loading.value = true
  try {
    // 验证必填字段
    if (!form.value.name) {
      showToast({ message: '请输入物品名称', position: 'top' })
      loading.value = false
      return
    }
    if (!form.value.purchase_price) {
      showToast({ message: '请输入购买价格', position: 'top' })
      loading.value = false
      return
    }
    
    await createItem({
      name: form.value.name,
      category_id: form.value.category_id,
      brand: form.value.brand || null,
      purchase_date: form.value.purchase_date,
      purchase_price: parseFloat(form.value.purchase_price),
      platform: form.value.platform || null,
      description: form.value.description || null
    })
    showToast({ message: '添加成功', position: 'top' })
    router.replace('/')
  } catch (error) {
    showToast({ message: error.message || '添加失败', position: 'top' })
  } finally {
    loading.value = false
  }
}
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
