<template>
  <div class="not-found-page">
    <div class="text-center">
      <div class="error-code">404</div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-message">
        抱歉，您访问的页面不存在或已被移除
      </p>
      <div class="error-actions">
        <el-button type="primary" @click="goHome">
          返回首页
        </el-button>
        <el-button @click="goBack">
          返回上页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

// 返回首页
const goHome = () => {
  router.push('/')
}

// 返回上一页
const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.not-found-page {
  @apply flex items-center justify-center min-h-screen;
}

.error-code {
  @apply text-8xl font-bold text-gray-300 mb-4;
}

.error-title {
  @apply text-3xl font-bold text-gray-900 mb-4;
}

.error-message {
  @apply text-lg text-gray-600 mb-8;
}

.error-actions {
  @apply flex flex-col sm:flex-row gap-4 justify-center;
}
</style> 