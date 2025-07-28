<template>
  <div class="home-page">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="text-center mb-12">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          智能文档
          <span class="text-primary-600">研究助手</span>
        </h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
          基于AI技术，快速分析PDF文档并生成专业的结构化研究报告
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <el-button 
            type="primary" 
            size="large"
            @click="scrollToUpload"
            class="px-8 py-3"
          >
            开始使用
          </el-button>
          <el-button 
            size="large"
            @click="showDemo"
            class="px-8 py-3"
          >
            查看演示
          </el-button>
        </div>
      </div>
    </section>

    <!-- 上传区域 -->
    <section ref="uploadSection" class="upload-section mb-16">
      <div class="max-w-4xl mx-auto">
        <UploadForm />
      </div>
    </section>

    <!-- 功能特性 -->
    <section id="features" class="features-section mb-16">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">强大功能</h2>
        <p class="text-lg text-gray-600">为您提供专业的文档分析体验</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="feature-card">
          <div class="feature-icon">
            <Document class="w-8 h-8" />
          </div>
          <h3 class="feature-title">智能PDF解析</h3>
          <p class="feature-description">
            支持各种格式的PDF文档，自动提取文本内容并进行语义分片处理
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <MagicStick class="w-8 h-8" />
          </div>
          <h3 class="feature-title">AI智能分析</h3>
          <p class="feature-description">
            基于先进的大语言模型，深度理解文档内容并生成专业分析报告
          </p>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">
            <Download class="w-8 h-8" />
          </div>
          <h3 class="feature-title">结构化输出</h3>
          <p class="feature-description">
            生成标准Markdown格式报告，支持下载、打印和分享功能
          </p>
        </div>
      </div>
    </section>

    <!-- 使用流程 -->
    <section class="workflow-section mb-16">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">使用流程</h2>
        <p class="text-lg text-gray-600">简单三步，快速生成专业报告</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div class="workflow-step">
          <div class="step-number">1</div>
          <h3 class="step-title">上传文档</h3>
          <p class="step-description">
            拖拽或选择PDF文件上传，支持最大50MB文件
          </p>
        </div>
        
        <div class="workflow-step">
          <div class="step-number">2</div>
          <h3 class="step-title">输入问题</h3>
          <p class="step-description">
            描述您的研究问题，AI将基于文档内容进行分析
          </p>
        </div>
        
        <div class="workflow-step">
          <div class="step-number">3</div>
          <h3 class="step-title">获取报告</h3>
          <p class="step-description">
            等待AI处理完成，下载或查看生成的专业报告
          </p>
        </div>
      </div>
    </section>

    <!-- 关于我们 -->
    <section id="about" class="about-section">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">关于DeepResearch</h2>
          <p class="text-lg text-gray-600 mb-8">
            DeepResearch是一款基于人工智能的智能文档研究助手，致力于为用户提供高效、准确的文档分析服务。
          </p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 text-left">
            <div>
              <h3 class="text-xl font-semibold text-gray-900 mb-4">技术优势</h3>
              <ul class="space-y-2 text-gray-600">
                <li>• 先进的PDF解析技术</li>
                <li>• 基于GPT-4的智能分析</li>
                <li>• 语义分片处理算法</li>
                <li>• 实时进度跟踪</li>
              </ul>
            </div>
            
            <div>
              <h3 class="text-xl font-semibold text-gray-900 mb-4">应用场景</h3>
              <ul class="space-y-2 text-gray-600">
                <li>• 学术研究文档分析</li>
                <li>• 商业报告解读</li>
                <li>• 技术文档总结</li>
                <li>• 法律文件分析</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, MagicStick, Download } from '@element-plus/icons-vue'
import UploadForm from '@/components/UploadForm.vue'

const uploadSection = ref<HTMLElement>()

// 滚动到上传区域
const scrollToUpload = () => {
  uploadSection.value?.scrollIntoView({ 
    behavior: 'smooth',
    block: 'start'
  })
}

// 显示演示
const showDemo = () => {
  ElMessage.info('演示功能开发中...')
}
</script>

<style scoped>
.hero-section {
  @apply py-16;
}

.feature-card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 text-center p-8 hover:shadow-lg transition-shadow duration-300;
}

.feature-icon {
  @apply w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 text-primary-600;
}

.feature-title {
  @apply text-xl font-semibold text-gray-900 mb-3;
}

.feature-description {
  @apply text-gray-600 leading-relaxed;
}

.workflow-step {
  @apply text-center p-6;
}

.step-number {
  @apply w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center mx-auto mb-4 text-lg font-bold;
}

.step-title {
  @apply text-xl font-semibold text-gray-900 mb-3;
}

.step-description {
  @apply text-gray-600;
}

.about-section {
  @apply py-16;
}
</style> 