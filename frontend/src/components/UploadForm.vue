<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
    <div class="text-center mb-8">
      <h2 class="text-2xl font-bold text-gray-900 mb-2">开始您的研究</h2>
      <p class="text-gray-600">上传PDF文档并输入研究问题，AI将为您生成专业的分析报告</p>
    </div>

    <el-form 
      ref="formRef" 
      :model="formData" 
      :rules="rules" 
      label-width="0"
      @submit.prevent="handleSubmit"
    >
      <!-- 文件上传区域 -->
      <div class="mb-6">
        <el-upload
          ref="uploadRef"
          class="upload-area"
          drag
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleFileChange"
          :before-upload="beforeUpload"
          accept=".pdf"
        >
          <div class="upload-content">
            <el-icon class="upload-icon"><Document /></el-icon>
            <div class="upload-text">
              <span class="text-lg font-medium">点击或拖拽PDF文件到此处</span>
              <p class="text-sm text-gray-500 mt-2">支持单个文件，最大50MB</p>
            </div>
          </div>
        </el-upload>
        
        <!-- 文件信息显示 -->
        <div v-if="selectedFile" class="mt-4 p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <Document class="w-5 h-5 text-primary-600" />
              <div>
                <p class="font-medium text-gray-900">{{ selectedFile.name }}</p>
                <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
            </div>
            <el-button 
              type="danger" 
              size="small" 
              @click="removeFile"
              :icon="Delete"
            >
              移除
            </el-button>
          </div>
        </div>
      </div>

      <!-- 研究问题输入 -->
      <div class="mb-6">
        <el-form-item prop="question">
          <el-input
            v-model="formData.question"
            type="textarea"
            :rows="4"
            placeholder="请输入您的研究问题，例如：请分析数字医疗在老龄化社会中的影响和作用..."
            class="input-field"
          />
        </el-form-item>
      </div>

      <!-- 提交按钮 -->
      <div class="text-center">
        <el-button
          type="primary"
          size="large"
          :loading="loading"
          :disabled="!selectedFile || !formData.question.trim()"
          @click="handleSubmit"
          class="w-full md:w-auto px-8"
        >
          <template #icon>
            <MagicStick v-if="!loading" />
          </template>
          {{ loading ? '正在生成报告...' : '开始生成报告' }}
        </el-button>
      </div>
    </el-form>

    <!-- 使用提示 -->
    <div class="mt-8 p-4 bg-blue-50 rounded-lg">
      <h3 class="font-medium text-blue-900 mb-2">💡 使用提示</h3>
      <ul class="text-sm text-blue-800 space-y-1">
        <li>• 确保PDF文档内容清晰可读</li>
        <li>• 问题描述越具体，生成的报告越精准</li>
        <li>• 支持中文和英文文档分析</li>
        <li>• 生成时间取决于文档长度，请耐心等待</li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, UploadInstance, UploadFile } from 'element-plus'
import { Document, Delete, MagicStick } from '@element-plus/icons-vue'
import { useReportStore } from '@/stores/reportStore'

const router = useRouter()
const reportStore = useReportStore()

// 表单引用
const formRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()

// 表单数据
const formData = reactive({
  question: ''
})

// 选中的文件
const selectedFile = ref<File | null>(null)

// 加载状态
const loading = ref(false)

// 表单验证规则
const rules = {
  question: [
    { required: true, message: '请输入研究问题', trigger: 'blur' },
    { min: 5, message: '问题描述至少5个字符', trigger: 'blur' },
    { max: 1000, message: '问题描述不能超过1000个字符', trigger: 'blur' }
  ]
}

// 文件大小格式化
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 文件选择处理
const handleFileChange = (file: UploadFile) => {
  if (file.raw) {
    selectedFile.value = file.raw
  }
}

// 文件上传前验证
const beforeUpload = (file: File): boolean => {
  // 检查文件类型
  if (!file.type.includes('pdf')) {
    ElMessage.error('只能上传PDF文件')
    return false
  }
  
  // 检查文件大小 (50MB)
  const maxSize = 50 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过50MB')
    return false
  }
  
  return true
}

// 移除文件
const removeFile = () => {
  selectedFile.value = null
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请选择PDF文件')
    return
  }

  if (!formData.question.trim()) {
    ElMessage.warning('请输入研究问题')
    return
  }

  try {
    loading.value = true
    
    // 调用store生成报告
    const result = await reportStore.createReport(selectedFile.value, formData.question)
    
    // 跳转到报告页面
    router.push(`/report/${result.report_id}`)
    
  } catch (error: any) {
    console.error('生成报告失败:', error)
    
    // 根据错误类型提供不同的提示
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      ElMessage.error('请求超时，请稍后重试。大文件处理可能需要更长时间。')
    } else if (error.response?.status === 413) {
      ElMessage.error('文件太大，请选择小于50MB的文件')
    } else if (error.response?.status === 400) {
      ElMessage.error(error.response.data?.msg || '请求参数错误')
    } else if (error.response?.status === 500) {
      ElMessage.error('服务器内部错误，请稍后重试')
    } else {
      ElMessage.error('生成报告失败，请检查网络连接后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-area {
  @apply w-full;
}

.upload-content {
  @apply flex flex-col items-center justify-center py-8;
}

.upload-icon {
  @apply w-12 h-12 text-gray-400 mb-4;
}

.upload-text {
  @apply text-center;
}

:deep(.el-upload-dragger) {
  @apply w-full border-2 border-dashed border-gray-300 hover:border-primary-500 transition-colors duration-200;
}

:deep(.el-upload-dragger:hover) {
  @apply bg-primary-50;
}
</style> 