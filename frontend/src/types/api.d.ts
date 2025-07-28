// API响应基础类型
export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}

// 报告元数据类型
export interface ReportMetadata {
  total_chunks: number
  processed_chunks: number
  token_per_chunk: number
  processing_time: number
  model_used: string
  created_at: string
}

// 生成报告响应类型
export interface GenerateReportResponse {
  report_id: string
  markdown_report: string
  report_metadata: ReportMetadata
}

// 报告信息类型
export interface ReportInfo {
  report_id: string
  question: string
  created_at: string
  file_size?: number
  status: string
}

// 报告列表响应类型
export interface ReportListResponse {
  reports: ReportInfo[]
  total: number
  page: number
  page_size: number
}

// 文件上传类型
export interface FileUpload {
  file: File
  question: string
}

// 错误响应类型
export interface ErrorResponse {
  code: number
  msg: string
  data?: any
} 