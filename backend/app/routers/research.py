from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import os
import tempfile
from typing import Optional
from loguru import logger

from app.services.report_service import ReportService
from app.schemas.report_schema import (
    GenerateReportResponse,
    StandardResponse,
    ReportListResponse
)
from app.core.config import settings

router = APIRouter()
report_service = ReportService()

@router.post("/generate_report", response_model=StandardResponse)
async def generate_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF文件"),
    question: str = Form(..., description="研究问题", min_length=1, max_length=1000)
):
    """生成研究报告"""
    try:
        # 验证文件类型
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="只支持PDF文件")
        
        # 验证文件大小
        if file.size > settings.max_file_size:
            raise HTTPException(status_code=400, detail="文件大小超过限制")
        
        # 保存上传的文件
        temp_file_path = None
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            logger.info(f"File uploaded: {file.filename}, size: {file.size} bytes")
            
            # 生成报告
            result = await report_service.generate_report(temp_file_path, question)
            
            return StandardResponse(
                code=200,
                msg="success",
                data=result
            )
            
        finally:
            # 清理临时文件
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail="生成报告失败")

@router.get("/download_report/{report_id}")
async def download_report(report_id: str):
    """下载报告文件"""
    try:
        # 获取报告内容
        report_content = report_service.get_report(report_id)
        
        # 创建临时文件用于下载
        temp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.md', mode='w', encoding='utf-8') as temp_file:
                temp_file.write(report_content)
                temp_file_path = temp_file.name
            
            # 返回文件响应
            return FileResponse(
                path=temp_file_path,
                filename=f"research_report_{report_id}.md",
                media_type="text/markdown",
                background=lambda: os.unlink(temp_file_path) if os.path.exists(temp_file_path) else None
            )
            
        except Exception as e:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            raise e
            
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="报告不存在")
    except Exception as e:
        logger.error(f"Error downloading report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="下载报告失败")

@router.get("/reports", response_model=StandardResponse)
async def list_reports():
    """获取报告列表"""
    try:
        reports = report_service.list_reports()
        
        return StandardResponse(
            code=200,
            msg="success",
            data={
                "reports": reports,
                "total": len(reports)
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing reports: {e}")
        raise HTTPException(status_code=500, detail="获取报告列表失败")

@router.get("/reports/{report_id}", response_model=StandardResponse)
async def get_report(report_id: str):
    """获取报告详情"""
    try:
        report_content = report_service.get_report(report_id)
        
        return StandardResponse(
            code=200,
            msg="success",
            data={
                "report_id": report_id,
                "content": report_content
            }
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="报告不存在")
    except Exception as e:
        logger.error(f"Error getting report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="获取报告失败")

@router.delete("/reports/{report_id}", response_model=StandardResponse)
async def delete_report(report_id: str):
    """删除报告"""
    try:
        report_file_path = os.path.join(settings.reports_dir, f"{report_id}.md")
        
        if not os.path.exists(report_file_path):
            raise HTTPException(status_code=404, detail="报告不存在")
        
        os.remove(report_file_path)
        logger.info(f"Report deleted: {report_id}")
        
        return StandardResponse(
            code=200,
            msg="success",
            data={"deleted": True}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting report {report_id}: {e}")
        raise HTTPException(status_code=500, detail="删除报告失败")

@router.get("/health", response_model=StandardResponse)
async def health_check():
    """健康检查"""
    return StandardResponse(
        code=200,
        msg="success",
        data={
            "status": "healthy",
            "service": "research"
        }
    ) 