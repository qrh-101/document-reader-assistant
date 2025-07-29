from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import os
import tempfile
from typing import Optional
from loguru import logger

from app.services.report_service import ReportService
from app.services.prompt_service import PromptService
from app.schemas.report_schema import (
    GenerateReportResponse,
    StandardResponse,
    ReportListResponse
)
from app.core.config import settings

router = APIRouter()
report_service = ReportService()
prompt_service = PromptService()

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
        
        # 获取报告标题用于文件名
        report_title = report_service.get_report_title(report_id)
        
        # 清理文件名中的特殊字符，确保文件名合法
        import re
        import urllib.parse
        
        # 使用英文文件名避免编码问题
        english_filename = f"research_report_{report_id}"
        
        # 准备中文文件名用于Content-Disposition头
        safe_filename = re.sub(r'[<>:"/\\|?*]', '_', report_title)
        safe_filename = safe_filename.replace(' ', '_')
        
        # URL编码中文文件名用于filename*参数
        encoded_filename = urllib.parse.quote(safe_filename)
        
        # 创建临时文件用于下载
        temp_file_path = None
        try:
            # 创建临时文件并写入内容
            temp_file_path = tempfile.mktemp(suffix='.md')
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                temp_file.write(report_content)
            
            async def cleanup_temp_file():
                """异步清理临时文件的函数"""
                try:
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                        logger.info(f"Cleaned up temp file: {temp_file_path}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file {temp_file_path}: {e}")
            
            def file_generator():
                try:
                    with open(temp_file_path, 'rb') as f:
                        yield from f
                except Exception as e:
                    logger.error(f"Error reading file {temp_file_path}: {e}")
                    raise
                finally:
                    # Ensure cleanup happens even if client disconnects or error occurs
                    try:
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)
                            logger.info(f"Cleaned up temp file: {temp_file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to cleanup temp file {temp_file_path}: {e}")
            
            return StreamingResponse(
                file_generator(),
                media_type="text/markdown",
                headers={
                    "Content-Disposition": f'attachment; filename="{english_filename}.md"; filename*=UTF-8\'\'{encoded_filename}.md',
                    "Access-Control-Expose-Headers": "Content-Disposition"
                }
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
        metadata = report_service.get_report_metadata(report_id)
        created_at = report_service.get_report_created_at(report_id)
        return StandardResponse(
            code=200,
            msg="success",
            data={
                "report_id": report_id,
                "content": report_content,
                "report_metadata": metadata,
                "created_at": created_at
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

@router.get("/prompts/versions", response_model=StandardResponse)
async def get_prompt_versions():
    """获取可用的提示词版本列表"""
    try:
        versions = prompt_service.get_available_prompt_versions()
        return StandardResponse(
            code=200,
            msg="success",
            data={
                "available_versions": versions,
                "current_version": prompt_service.prompt_version
            }
        )
    except Exception as e:
        logger.error(f"获取提示词版本列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取提示词版本列表失败")

@router.get("/prompts/info/{version}", response_model=StandardResponse)
async def get_prompt_info(version: str):
    """获取指定提示词版本的详细信息"""
    try:
        info = prompt_service.get_prompt_info(version)
        if "error" in info:
            raise HTTPException(status_code=404, detail=info["error"])
        
        return StandardResponse(
            code=200,
            msg="success",
            data=info
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取提示词信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取提示词信息失败")

@router.get("/prompts/current", response_model=StandardResponse)
async def get_current_prompt_info():
    """获取当前使用的提示词信息"""
    try:
        info = prompt_service.get_prompt_info()
        return StandardResponse(
            code=200,
            msg="success",
            data=info
        )
    except Exception as e:
        logger.error(f"获取当前提示词信息失败: {e}")
        raise HTTPException(status_code=500, detail="获取当前提示词信息失败") 