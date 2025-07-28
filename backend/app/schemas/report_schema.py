from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class GenerateReportRequest(BaseModel):
    """生成报告请求模型"""
    question: str = Field(..., description="研究问题", min_length=1, max_length=1000)
    
class ReportMetadata(BaseModel):
    """报告元数据"""
    total_chunks: int = Field(..., description="总片段数")
    processed_chunks: int = Field(..., description="已处理片段数")
    token_per_chunk: int = Field(..., description="每个片段的token数")
    chunk_size: int = Field(..., description="分片大小（字符数）")
    overlap_size: int = Field(..., description="重叠大小（字符数）")
    model_context_length: int = Field(..., description="模型上下文长度（tokens）")
    processing_time: float = Field(..., description="处理时间（秒）")
    model_used: str = Field(..., description="使用的模型")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    
    model_config = {
        "protected_namespaces": ()
    }

class GenerateReportResponse(BaseModel):
    """生成报告响应模型"""
    report_id: str = Field(..., description="报告唯一ID")
    markdown_report: str = Field(..., description="Markdown格式的报告内容")
    report_metadata: ReportMetadata = Field(..., description="报告元数据")

class StandardResponse(BaseModel):
    """标准响应模型"""
    code: int = Field(..., description="响应状态码")
    msg: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")

class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误状态码")
    msg: str = Field(..., description="错误消息")
    data: Optional[Any] = Field(None, description="错误详情")

class ReportInfo(BaseModel):
    """报告信息模型"""
    report_id: str = Field(..., description="报告ID")
    question: str = Field(..., description="研究问题")
    created_at: datetime = Field(..., description="创建时间")
    file_size: Optional[int] = Field(None, description="文件大小")
    status: str = Field(..., description="处理状态")

class ReportListResponse(BaseModel):
    """报告列表响应模型"""
    reports: list[ReportInfo] = Field(..., description="报告列表")
    total: int = Field(..., description="总数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小") 