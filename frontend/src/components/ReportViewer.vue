<template>
  <div class="report-viewer" data-testid="report-viewer">
    <!-- 报告头部信息 -->
    <div class="report-header">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">智能文档研究助手</h1>
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
      
      <!-- 研究问题 -->
      <div class="research-question mb-6">
        <div class="card bg-blue-50 border-blue-200">
          <h3 class="text-lg font-semibold text-blue-900 mb-2">研究问题</h3>
          <p class="text-blue-800">{{ extractResearchQuestion() }}</p>
        </div>
      </div>
      
      <!-- 报告元数据 -->
      <div class="report-meta">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="meta-item">
            <span class="meta-label">报告ID</span>
            <span class="meta-value font-mono text-sm">{{ report?.id || 'N/A' }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">生成时间</span>
            <span class="meta-value">{{ formatDate(report?.created_at) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">处理时间</span>
            <span class="meta-value">{{ formatDuration(report?.metadata?.processing_time ?? 0) }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">使用模型</span>
            <span class="meta-value">{{ report?.metadata?.model_used ?? 'N/A' }}</span>
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
            <div class="stat-value">{{ report?.metadata?.chunk_size ?? 0 }}</div>
            <div class="stat-label">分片大小</div>
          </div>
        </div>
        
        <!-- 技术参数 -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <h4 class="text-md font-medium text-gray-700 mb-3">技术参数</h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="tech-param">
              <span class="param-label">重叠大小</span>
              <span class="param-value">{{ report?.metadata?.overlap_size ?? 0 }} 字符</span>
            </div>
            <div class="tech-param">
              <span class="param-label">模型上下文长度</span>
              <span class="param-value">{{ formatNumber(report?.metadata?.model_context_length ?? 0) }}</span>
            </div>
            <div class="tech-param">
              <span class="param-label">处理效率</span>
              <span class="param-value">{{ calculateEfficiency() }}</span>
            </div>
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
  
  // 过滤掉重复的元数据信息和通用标题
  let content = report.value.content
  
  // 移除元数据部分（从第一个**开始到---结束）
  const metadataStart = content.indexOf('**研究问题**:')
  const separatorIndex = content.indexOf('---')
  
  if (metadataStart !== -1 && separatorIndex !== -1 && separatorIndex > metadataStart) {
    // 获取实际内容部分（从---之后开始）
    const actualContent = content.substring(separatorIndex + 3) // 跳过---和换行
    
    // 移除通用的"# 研究报告"标题，保留具体的报告标题
    const lines = actualContent.split('\n')
    const filteredLines = []
    let skipNextEmptyLine = false
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      
      // 跳过"# 研究报告"标题
      if (line.trim() === '# 研究报告') {
        skipNextEmptyLine = true
        continue
      }
      
      // 跳过"# 研究报告"后面的空行
      if (skipNextEmptyLine && line.trim() === '') {
        skipNextEmptyLine = false
        continue
      }
      
      filteredLines.push(line)
    }
    
    content = filteredLines.join('\n')
  }
  
  return marked(content)
})

// 提取研究问题
const extractResearchQuestion = () => {
  if (!report.value?.content) return 'N/A'
  
  // 匹配后端保存的格式：**研究问题**: 问题内容
  const questionMatch = report.value.content.match(/\*\*研究问题\*\*: (.+?)(?=\n\n)/);
  return questionMatch ? questionMatch[1].trim() : 'N/A';
}

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

// 格式化数字
const formatNumber = (num: number): string => {
  if (num === null || num === undefined) return 'N/A'
  return num.toLocaleString('zh-CN')
}

// 计算处理效率
const calculateEfficiency = (): string => {
  if (!report.value?.metadata?.processing_time || !report.value?.metadata?.total_chunks) {
    return 'N/A'
  }
  const totalSeconds = report.value.metadata.processing_time
  const totalChunks = report.value.metadata.total_chunks
  const avgTimePerChunk = totalSeconds / totalChunks
  return `${avgTimePerChunk.toFixed(2)}秒/片段`
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
  @apply text-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors;
}

.stat-value {
  @apply text-2xl font-bold text-primary-600 mb-1;
}

.stat-label {
  @apply text-sm text-gray-600;
}

.tech-param {
  @apply text-center p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors;
}

.param-label {
  @apply text-sm text-gray-500 block mb-1;
}

.param-value {
  @apply text-sm font-medium text-gray-900;
}

.card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
}

.markdown-content {
  @apply prose prose-gray max-w-none;
}

.markdown-content h1 {
  @apply text-2xl font-bold text-gray-900 mb-4;
}

.markdown-content h2 {
  @apply text-xl font-semibold text-gray-800 mb-3;
}

.markdown-content h3 {
  @apply text-lg font-medium text-gray-700 mb-2;
}

.markdown-content p {
  @apply text-gray-700 leading-relaxed mb-4;
}

.markdown-content ul, .markdown-content ol {
  @apply mb-4;
}

.markdown-content li {
  @apply text-gray-700 mb-1;
}

/* 打印样式 */
@media print {
  .report-header .flex:last-child,
  .report-stats {
    display: none;
  }
}
</style> 