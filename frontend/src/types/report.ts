// 报告状态枚举
export enum ReportStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

// 报告元数据类型
export interface ReportMetadata {
  total_chunks: number
  processed_chunks: number
  token_per_chunk: number
  chunk_size?: number
  overlap_size?: number
  model_context_length?: number
  processing_time: number
  model_used: string
  created_at?: string
}

// 报告处理进度
export interface ReportProgress {
  status: ReportStatus
  progress: number // 0-100
  message: string
  current_chunk?: number
  total_chunks?: number
}

// 报告内容
export interface ReportContent {
  id: string
  title: string
  content: string
  metadata?: any
  created_at?: string
  updated_at?: string
}

// 报告搜索参数
export interface ReportSearchParams {
  keyword?: string
  start_date?: string
  end_date?: string
  status?: ReportStatus
  page?: number
  page_size?: number
}

// 报告排序选项
export interface ReportSortOptions {
  field: 'created_at' | 'title' | 'status'
  order: 'asc' | 'desc'
} 