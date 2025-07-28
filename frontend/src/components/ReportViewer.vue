<template>
  <div class="report-viewer" data-testid="report-viewer">
    <!-- 报告头部信息 -->
    <div class="report-header">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">研究报告</h1>
          <p class="text-gray-600">基于AI智能分析生成的专业研究报告</p>
        </div>
        
        <!-- 操作按钮 -->
        <div class="flex items-center space-x-3">
          <el-button 
            type="primary" 
            @click="downloadReport"
            :loading="downloading"
            :icon="Download"
          >
            下载报告
          </el-button>
          <el-button 
            @click="printReport"
            :icon="Printer"
          >
            打印
          </el-button>
          <el-dropdown @command="handleCommand">
            <el-button :icon="More" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="share">
                  <Share class="w-4 h-4 mr-2" />
                  分享
                </el-dropdown-item>
                <el-dropdown-item command="export">
                  <Document class="w-4 h-4 mr-2" />
                  导出
                </el-dropdown-item>
                <el-dropdown-item divided command="delete">
                  <Delete class="w-4 h-4 mr-2" />
                  删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <!-- 报告元数据 -->
      <div class="report-meta">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="meta-item">
            <span class="meta-label">报告ID</span>
            <span class="meta-value">{{ report?.id || 'N/A' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">生成时间</span>
            <span class="meta-value">{{ formatDate(report?.created_at) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">处理时间</span>
            <span class="meta-value">{{ formatDuration(report?.metadata?.processing_time ?? 0) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 报告内容 -->
    <div class="report-content">
      <div class="card">
        <div 
          ref="contentRef"
          class="markdown-content"
          v-html="renderedContent"
        ></div>
      </div>
    </div>

    <!-- 报告统计信息 -->
    <div class="report-stats mt-8">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">处理统计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="stat-item">
            <div class="stat-value">{{ report?.metadata?.total_chunks ?? 0 }}</div>
            <div class="stat-label">总片段数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ report?.metadata?.processed_chunks ?? 0 }}</div>
            <div class="stat-label">已处理片段</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ report?.metadata?.token_per_chunk ?? 0 }}</div>
            <div class="stat-label">每片段Token数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ report?.metadata?.model_used ?? 'N/A' }}</div>
            <div class="stat-label">使用模型</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'
import { 
  Download, 
  Printer, 
  More, 
  Share, 
  Document, 
  Delete 
} from '@element-plus/icons-vue'
import { useReportStore } from '@/stores/reportStore'
import type { ReportContent } from '@/types/report'

const route = useRoute()
const router = useRouter()
const reportStore = useReportStore()

const contentRef = ref<HTMLElement>()
const downloading = ref(false)

// 获取报告数据
const report = computed(() => reportStore.currentReport)

// 渲染Markdown内容
const renderedContent = computed(() => {
  if (!report.value?.content) return ''
  return marked(report.value.content)
})

// 格式化日期
const formatDate = (dateString?: string): string => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 格式化处理时间
const formatDuration = (seconds?: number): string => {
  if (!seconds) return 'N/A'
  if (seconds < 60) return `${seconds.toFixed(1)}秒`
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds.toFixed(0)}秒`
}

// 下载报告
const downloadReport = async () => {
  if (!report.value?.id) return
  
  try {
    downloading.value = true
    await reportStore.downloadReportFile(report.value.id)
  } catch (error) {
    console.error('下载失败:', error)
  } finally {
    downloading.value = false
  }
}

// 打印报告
const printReport = () => {
  if (!contentRef.value) return
  
  const printWindow = window.open('', '_blank')
  if (printWindow) {
    printWindow.document.write(`
      <html>
        <head>
          <title>研究报告</title>
          <style>
            body { font-family: 'Inter', sans-serif; line-height: 1.6; }
            .markdown-content { max-width: 800px; margin: 0 auto; padding: 20px; }
            h1, h2, h3 { color: #1f2937; }
            pre { background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; }
            code { background: #f3f4f6; padding: 0.2rem 0.4rem; border-radius: 0.25rem; }
          </style>
        </head>
        <body>
          <div class="markdown-content">
            ${contentRef.value.innerHTML}
          </div>
        </body>
      </html>
    `)
    printWindow.document.close()
    printWindow.print()
  }
}

// 处理下拉菜单命令
const handleCommand = async (command: string) => {
  switch (command) {
    case 'share':
      ElMessage.info('分享功能开发中...')
      break
    case 'export':
      ElMessage.info('导出功能开发中...')
      break
    case 'delete':
      await handleDelete()
      break
  }
}

// 处理删除
const handleDelete = async () => {
  if (!report.value?.id) return
  
  try {
    await ElMessageBox.confirm(
      '确定要删除这份报告吗？删除后无法恢复。',
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await reportStore.removeReport(report.value.id)
    router.push('/')
    ElMessage.success('报告已删除')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

// 组件挂载时获取报告详情
onMounted(async () => {
  const reportId = route.params.id as string
  if (reportId) {
    try {
      await reportStore.fetchReportDetail(reportId)
    } catch (error) {
      ElMessage.error('获取报告失败')
      router.push('/')
    }
  }
})
</script>

<style scoped>
.report-viewer {
  @apply max-w-6xl mx-auto;
}

.report-header {
  @apply mb-8;
}

.report-meta {
  @apply bg-gray-50 rounded-lg p-4;
}

.meta-item {
  @apply flex flex-col;
}

.meta-label {
  @apply text-sm text-gray-500 mb-1;
}

.meta-value {
  @apply text-sm font-medium text-gray-900;
}

.report-content {
  @apply mb-8;
}

.report-stats {
  @apply mb-8;
}

.stat-item {
  @apply text-center p-4 bg-gray-50 rounded-lg;
}

.stat-value {
  @apply text-2xl font-bold text-primary-600 mb-1;
}

.stat-label {
  @apply text-sm text-gray-600;
}

/* 打印样式 */
@media print {
  .report-header .flex:last-child,
  .report-stats {
    display: none;
  }
}
</style> 