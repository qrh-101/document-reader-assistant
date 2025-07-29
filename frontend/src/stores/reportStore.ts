import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ReportStatus } from '@/types/report'
import type { ReportProgress, ReportContent } from '@/types/report'
import type { ReportInfo, GenerateReportResponse } from '@/types/api'
import { 
  generateReport, 
  getReportList, 
  getReportDetail, 
  downloadReport, 
  deleteReport 
} from '@/api/research'

export const useReportStore = defineStore('report', () => {
  // 状态
  const reports = ref<ReportInfo[]>([])
  const currentReport = ref<ReportContent | null>(null)
  const loading = ref(false)
  const progress = ref<ReportProgress>({
    status: ReportStatus.PENDING,
    progress: 0,
    message: ''
  })

  // 计算属性
  const completedReports = computed(() => 
    reports.value.filter(report => report.status === 'completed')
  )

  const pendingReports = computed(() => 
    reports.value.filter(report => report.status === 'pending')
  )

  const processingReports = computed(() => 
    reports.value.filter(report => report.status === 'processing')
  )

  // 生成报告
  const createReport = async (file: File, question: string) => {
    let progressInterval: NodeJS.Timeout | null = null
    
    try {
      loading.value = true
      progress.value = {
        status: ReportStatus.PROCESSING,
        progress: 0,
        message: '正在上传文件...'
      }

      // 模拟进度更新
      progressInterval = setInterval(() => {
        if (progress.value.progress < 90) {
          progress.value.progress += Math.random() * 10
          progress.value.message = `正在处理中... ${Math.round(progress.value.progress)}%`
        }
      }, 1000)

      const response = await generateReport(file, question)
      
      if (progressInterval) {
        clearInterval(progressInterval)
      }
      progress.value = {
        status: ReportStatus.COMPLETED,
        progress: 100,
        message: '报告生成完成！'
      }

      // 添加到报告列表
      const newReport: ReportInfo = {
        report_id: response.data.report_id,
        question: question,
        created_at: new Date().toISOString(),
        status: 'completed'
      }
      
      reports.value.unshift(newReport)
      
      ElMessage.success('报告生成成功！')
      return response.data
      
    } catch (error: any) {
      if (progressInterval) {
        clearInterval(progressInterval)
      }
      progress.value = {
        status: ReportStatus.FAILED,
        progress: 0,
        message: '报告生成失败'
      }
      
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
        ElMessage.error('报告生成失败，请检查网络连接后重试')
      }
      
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取报告列表
  const fetchReports = async () => {
    try {
      loading.value = true
      const response = await getReportList()
      reports.value = response.data.reports || []
    } catch (error) {
      ElMessage.error('获取报告列表失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取报告详情
  const fetchReportDetail = async (reportId: string) => {
    console.log(`[DEBUG] fetchReportDetail called with reportId: ${reportId}`)
    try {
      loading.value = true
      const response = await getReportDetail(reportId)
      console.log('[DEBUG] getReportDetail response:', response.data)
      currentReport.value = {
        id: response.data.report_id,
        title: '研究报告',
        content: response.data.content,
        metadata: response.data.report_metadata || {},
        created_at: response.data.created_at || new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      console.log(`[DEBUG] fetchReportDetail completed for reportId: ${reportId}`)
      return currentReport.value
    } catch (error) {
      console.error(`[DEBUG] fetchReportDetail failed for reportId: ${reportId}`, error)
      ElMessage.error('获取报告详情失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 下载报告
  const downloadReportFile = async (reportId: string) => {
    try {
      await downloadReport(reportId)
      ElMessage.success('报告下载成功')
    } catch (error) {
      ElMessage.error('报告下载失败')
      throw error
    }
  }

  // 删除报告
  const removeReport = async (reportId: string) => {
    try {
      await deleteReport(reportId)
      reports.value = reports.value.filter(report => report.report_id !== reportId)
      ElMessage.success('报告删除成功')
    } catch (error) {
      ElMessage.error('报告删除失败')
      throw error
    }
  }

  // 重置进度
  const resetProgress = () => {
    progress.value = {
      status: ReportStatus.PENDING,
      progress: 0,
      message: ''
    }
  }

  // 清除当前报告
  const clearCurrentReport = () => {
    currentReport.value = null
  }

  return {
    // 状态
    reports,
    currentReport,
    loading,
    progress,
    
    // 计算属性
    completedReports,
    pendingReports,
    processingReports,
    
    // 方法
    createReport,
    fetchReports,
    fetchReportDetail,
    downloadReportFile,
    removeReport,
    resetProgress,
    clearCurrentReport
  }
}) 