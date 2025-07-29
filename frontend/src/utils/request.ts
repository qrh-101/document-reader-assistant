import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types/api'

// 创建axios实例
const request: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response
    
    // 如果是blob响应，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 如果响应成功但业务状态码不是200
    if (data.code !== 200) {
      ElMessage.error(data.msg || '请求失败')
      return Promise.reject(new Error(data.msg || '请求失败'))
    }
    
    return data
  },
  (error) => {
    let message = '网络错误'
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          message = data?.msg || '请求参数错误'
          break
        case 401:
          message = '未授权，请重新登录'
          break
        case 403:
          message = '拒绝访问'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = data?.msg || '服务器内部错误'
          break
        default:
          message = data?.msg || `请求失败 (${status})`
      }
    } else if (error.request) {
      message = '网络连接失败'
    } else {
      message = error.message || '请求配置错误'
    }
    
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// 封装GET请求
export const get = <T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> => {
  return request.get(url, config)
}

// 封装POST请求
export const post = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> => {
  return request.post(url, data, config)
}

// 封装PUT请求
export const put = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> => {
  return request.put(url, data, config)
}

// 封装DELETE请求
export const del = <T = any>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> => {
  return request.delete(url, config)
}

// 封装文件上传
export const upload = <T = any>(url: string, formData: FormData, config?: AxiosRequestConfig): Promise<ApiResponse<T>> => {
  return request.post(url, formData, {
    ...config,
    headers: {
      'Content-Type': 'multipart/form-data',
      ...config?.headers,
    },
  })
}

// 封装文件下载
export const download = (url: string, filename?: string): Promise<void> => {
  return request.get(url, {
    responseType: 'blob',
  }).then((response) => {
    const blob = new Blob([response.data])
    const downloadUrl = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = downloadUrl
    
    // 优先使用传入的文件名，其次从响应头获取，最后使用默认文件名
    let finalFilename = filename
    if (!finalFilename) {
      const contentDisposition = response.headers['content-disposition']
      console.log('Content-Disposition header:', contentDisposition)
      
      if (contentDisposition) {
        // 解析Content-Disposition头，优先使用filename*
        let filenameMatch = contentDisposition.match(/filename\*=UTF-8''([^;]+)/)
        console.log('filename* match:', filenameMatch)
        
        if (!filenameMatch) {
          filenameMatch = contentDisposition.match(/filename="([^"]+)"/)
          console.log('filename="..." match:', filenameMatch)
        }
        if (!filenameMatch) {
          filenameMatch = contentDisposition.match(/filename=([^;]+)/)
          console.log('filename=... match:', filenameMatch)
        }
        
        if (filenameMatch && filenameMatch[1]) {
          try {
            // 解码URL编码的文件名
            finalFilename = decodeURIComponent(filenameMatch[1])
            console.log('Decoded filename:', finalFilename)
            // 确保有.md扩展名
            if (!finalFilename.endsWith('.md')) {
              finalFilename += '.md'
            }
          } catch (e) {
            console.warn('Failed to decode filename:', e)
            finalFilename = '研究报告.md'
          }
        } else {
          console.log('No filename match found, using default')
          finalFilename = '研究报告.md'
        }
      } else {
        console.log('No Content-Disposition header found, using default')
        finalFilename = '研究报告.md'
      }
    }
    
    console.log('Download filename:', finalFilename)
    link.download = finalFilename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(downloadUrl)
  }).catch((error) => {
    console.error('Download failed:', error)
    ElMessage.error('下载失败')
    throw error
  })
}

export default request 