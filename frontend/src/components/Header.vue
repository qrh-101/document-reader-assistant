<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <!-- Logo和标题 -->
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <Document class="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 class="text-xl font-bold text-gray-900">DeepResearch</h1>
            <p class="text-sm text-gray-500">智能文档研究助手</p>
          </div>
        </div>

        <!-- 导航菜单 -->
        <nav class="hidden md:flex items-center space-x-6">
          <router-link 
            to="/" 
            class="text-gray-600 hover:text-primary-600 transition-colors duration-200"
            :class="{ 'text-primary-600 font-medium': $route.name === 'home' }"
          >
            首页
          </router-link>
          <a 
            href="#features" 
            class="text-gray-600 hover:text-primary-600 transition-colors duration-200"
          >
            功能特性
          </a>
          <a 
            href="#about" 
            class="text-gray-600 hover:text-primary-600 transition-colors duration-200"
          >
            关于我们
          </a>
        </nav>

        <!-- 右侧操作区 -->
        <div class="flex items-center space-x-4">
          <!-- 主题切换 -->
          <el-button 
            :icon="Moon" 
            circle 
            size="small"
            @click="toggleTheme"
            class="text-gray-600 hover:text-primary-600"
          />
          
          <!-- 用户菜单 -->
          <el-dropdown>
            <el-button 
              :icon="User" 
              circle 
              size="small"
              class="text-gray-600 hover:text-primary-600"
            />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="showSettings">
                  <Setting class="w-4 h-4 mr-2" />
                  设置
                </el-dropdown-item>
                <el-dropdown-item @click="showHelp">
                  <QuestionFilled class="w-4 h-4 mr-2" />
                  帮助
                </el-dropdown-item>
                <el-dropdown-item divided @click="showAbout">
                  <InfoFilled class="w-4 h-4 mr-2" />
                  关于
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Document, 
  Moon, 
  User, 
  Setting, 
  QuestionFilled, 
  InfoFilled 
} from '@element-plus/icons-vue'

const router = useRouter()

// 切换主题
const toggleTheme = () => {
  ElMessage.info('主题切换功能开发中...')
}

// 显示设置
const showSettings = () => {
  ElMessage.info('设置功能开发中...')
}

// 显示帮助
const showHelp = () => {
  ElMessage.info('帮助功能开发中...')
}

// 显示关于
const showAbout = () => {
  ElMessage.info('关于功能开发中...')
}
</script>

<style scoped>
/* 组件特定样式 */
</style> 