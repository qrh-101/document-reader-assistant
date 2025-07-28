import { upload, get, del, download } from '@/utils/request'
import type { 
  GenerateReportResponse, 
  ReportListResponse, 
  ApiResponse 
} from '@/types/api'

// 生成研究报告
export const generateReport = (file: File, question: string): Promise<ApiResponse<GenerateReportResponse>> => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('question', question)
  
  return upload<GenerateReportResponse>('/generate_report', formData)
}

// 获取报告列表
export const getReportList = (): Promise<ApiResponse<ReportListResponse>> => {
  return get<ReportListResponse>('/reports')
}

// 获取报告详情
export const getReportDetail = (reportId: string): Promise<ApiResponse<{ report_id: string; content: string }>> => {
  return get<{ report_id: string; content: string }>(`/reports/${reportId}`)
}

// 下载报告
export const downloadReport = (reportId: string): Promise<void> => {
  return download(`/download_report/${reportId}`, `research_report_${reportId}.md`)
}

// 删除报告
export const deleteReport = (reportId: string): Promise<ApiResponse<{ deleted: boolean }>> => {
  return del<{ deleted: boolean }>(`/reports/${reportId}`)
}

// 健康检查
export const healthCheck = (): Promise<ApiResponse<{ status: string; service: string }>> => {
  return get<{ status: string; service: string }>('/health')
} 