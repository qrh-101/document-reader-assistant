<template>
  <div class="progress-container">
    <!-- 进度条 -->
    <div class="progress-bar">
      <div 
        class="progress-fill"
        :style="{ width: `${progress}%` }"
        :class="progressClass"
      ></div>
    </div>
    
    <!-- 进度信息 -->
    <div class="progress-info">
      <div class="flex items-center justify-between">
        <span class="progress-text">{{ message }}</span>
        <span class="progress-percentage">{{ Math.round(progress) }}%</span>
      </div>
      
      <!-- 详细进度信息 -->
      <div v-if="showDetails" class="progress-details">
        <div class="flex items-center space-x-4 text-sm text-gray-600">
          <span>状态: {{ statusText }}</span>
          <span v-if="currentChunk && totalChunks">
            处理进度: {{ currentChunk }}/{{ totalChunks }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ReportStatus } from '@/types/report'

interface Props {
  progress: number
  message: string
  status: ReportStatus
  currentChunk?: number
  totalChunks?: number
  showDetails?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  progress: 0,
  message: '',
  status: ReportStatus.PENDING,
  showDetails: true
})

// 进度条样式类
const progressClass = computed(() => {
  switch (props.status) {
    case ReportStatus.PROCESSING:
      return 'bg-primary-500'
    case ReportStatus.COMPLETED:
      return 'bg-green-500'
    case ReportStatus.FAILED:
      return 'bg-red-500'
    default:
      return 'bg-gray-400'
  }
})

// 状态文本
const statusText = computed(() => {
  switch (props.status) {
    case ReportStatus.PENDING:
      return '等待中'
    case ReportStatus.PROCESSING:
      return '处理中'
    case ReportStatus.COMPLETED:
      return '已完成'
    case ReportStatus.FAILED:
      return '失败'
    default:
      return '未知'
  }
})
</script>

<style scoped>
.progress-container {
  @apply w-full;
}

.progress-bar {
  @apply w-full h-2 bg-gray-200 rounded-full overflow-hidden;
}

.progress-fill {
  @apply h-full transition-all duration-300 ease-out;
}

.progress-info {
  @apply mt-3;
}

.progress-text {
  @apply text-sm font-medium text-gray-700;
}

.progress-percentage {
  @apply text-sm font-semibold text-primary-600;
}

.progress-details {
  @apply mt-2;
}
</style> 