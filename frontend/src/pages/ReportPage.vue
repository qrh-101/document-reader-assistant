<template>
  <div class="report-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="text-center">
        <el-icon class="loading-icon"><Loading /></el-icon>
        <p class="loading-text">正在加载报告...</p>
      </div>
    </div>

    <!-- 报告内容 -->
    <div v-else-if="report" class="report-container">
      <ReportViewer />
    </div>

    <!-- 错误状态 -->
    <div v-else class="error-container">
      <div class="text-center">
        <el-icon class="error-icon"><Warning /></el-icon>
        <h2 class="error-title">报告加载失败</h2>
        <p class="error-message">无法找到指定的报告，可能已被删除或不存在</p>
        <el-button type="primary" @click="goHome">
          返回首页
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Loading, Warning } from '@element-plus/icons-vue'
import { useReportStore } from '@/stores/reportStore'
import ReportViewer from '@/components/ReportViewer.vue'

const route = useRoute()
const router = useRouter()
const reportStore = useReportStore()

// 计算属性
const loading = computed(() => reportStore.loading)
const report = computed(() => reportStore.currentReport)

// 返回首页
const goHome = () => {
  router.push('/')
}

// 组件挂载时获取报告
onMounted(async () => {
  const reportId = route.params.id as string
  console.log(`[DEBUG] ReportPage onMounted called with reportId: ${reportId}`)
  if (reportId) {
    try {
      await reportStore.fetchReportDetail(reportId)
    } catch (error) {
      console.error('获取报告失败:', error)
    }
  }
})
</script>

<style scoped>
.report-page {
  @apply min-h-screen;
}

.loading-container {
  @apply flex items-center justify-center min-h-96;
}

.loading-icon {
  @apply w-12 h-12 text-primary-600 animate-spin mb-4;
}

.loading-text {
  @apply text-lg text-gray-600;
}

.report-container {
  @apply w-full;
}

.error-container {
  @apply flex items-center justify-center min-h-96;
}

.error-icon {
  @apply w-16 h-16 text-red-500 mb-4;
}

.error-title {
  @apply text-2xl font-bold text-gray-900 mb-2;
}

.error-message {
  @apply text-gray-600 mb-6;
}
</style> 