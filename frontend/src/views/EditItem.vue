<template>
  <div class="edit-item-container">
    <van-nav-bar title="编辑物品" left-arrow @click-left="$router.back()" fixed />
    
    <div class="content">
      <van-form @submit="onSubmit">
        <van-cell-group inset>
          <van-field
            v-model="form.name"
            name="name"
            label="物品名称"
            placeholder="请输入物品名称"
            :rules="[{ required: true, message: '请输入物品名称' }]"
          />
        </van-cell-group>
        
        <van-cell-group inset>
          <van-field
            v-model="form.brand"
            name="brand"
            label="品牌"
            placeholder="请输入品牌（选填）"
          />
        </van-cell-group>
        
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
        
        <van-cell-group inset>
          <van-field
            v-model="form.description"
            type="textarea"
            name="description"
            label="描述"
            placeholder="请输入物品描述"
            rows="3"
          />
        </van-cell-group>
        
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" :loading="loading">
            保存
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getItem, updateItem } from '@/api/items'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()

const form = ref({
  name: '',
  brand: '',
  purchase_price: '',
  description: ''
})
const loading = ref(false)

const fetchItem = async () => {
  try {
    const res = await getItem(route.params.id)
    form.value = {
      name: res.name || '',
      brand: res.brand || '',
      purchase_price: res.purchase_price ? String(res.purchase_price) : '',
      description: res.description || ''
    }
  } catch (error) {
    showToast({ message: error.message || '加载失败', position: 'top' })
  }
}

const onSubmit = async () => {
  loading.value = true
  try {
    await updateItem(route.params.id, {
      name: form.value.name,
      brand: form.value.brand,
      purchase_price: parseFloat(form.value.purchase_price),
      description: form.value.description
    })
    showToast({ message: '保存成功', position: 'top' })
    router.back()
  } catch (error) {
    showToast({ message: error.message || '保存失败', position: 'top' })
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchItem()
})
</script>

<style scoped>
.edit-item-container {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 46px;
  padding-bottom: 24px;
}

.submit-btn {
  padding: 24px 16px;
}
</style>
