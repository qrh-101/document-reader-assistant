import os
import shutil
import tempfile
from typing import Optional, Tuple
from fastapi import UploadFile
from loguru import logger
from app.core.config import settings

class FileIOUtils:
    """文件IO工具类"""
    
    @staticmethod
    async def save_uploaded_file(upload_file: UploadFile, directory: str = None) -> str:
        """保存上传的文件"""
        try:
            # 确定保存目录
            save_dir = directory or settings.upload_dir
            os.makedirs(save_dir, exist_ok=True)
            
            # 生成唯一文件名
            file_extension = os.path.splitext(upload_file.filename)[1]
            unique_filename = f"{os.urandom(8).hex()}{file_extension}"
            file_path = os.path.join(save_dir, unique_filename)
            
            # 保存文件
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            
            logger.info(f"File saved: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
            raise
    
    @staticmethod
    def create_temp_file(suffix: str = "", prefix: str = "temp_") -> Tuple[str, str]:
        """创建临时文件"""
        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                prefix=prefix
            )
            temp_file.close()
            
            logger.info(f"Temp file created: {temp_file.name}")
            return temp_file.name, temp_file.name
            
        except Exception as e:
            logger.error(f"Error creating temp file: {e}")
            raise
    
    @staticmethod
    def cleanup_temp_file(file_path: str):
        """清理临时文件"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Temp file cleaned up: {file_path}")
        except Exception as e:
            logger.warning(f"Error cleaning up temp file {file_path}: {e}")
    
    @staticmethod
    def validate_file_type(filename: str, allowed_extensions: list) -> bool:
        """验证文件类型"""
        if not filename:
            return False
        
        file_extension = os.path.splitext(filename.lower())[1]
        return file_extension in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """验证文件大小"""
        return file_size <= max_size
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """获取文件信息"""
        try:
            if not os.path.exists(file_path):
                return {}
            
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created_time": stat.st_ctime,
                "modified_time": stat.st_mtime,
                "filename": os.path.basename(file_path),
                "extension": os.path.splitext(file_path)[1]
            }
        except Exception as e:
            logger.error(f"Error getting file info {file_path}: {e}")
            return {}
    
    @staticmethod
    def ensure_directory(directory_path: str):
        """确保目录存在"""
        try:
            os.makedirs(directory_path, exist_ok=True)
            logger.info(f"Directory ensured: {directory_path}")
        except Exception as e:
            logger.error(f"Error ensuring directory {directory_path}: {e}")
            raise
    
    @staticmethod
    def list_files_in_directory(directory_path: str, extension: str = None) -> list:
        """列出目录中的文件"""
        try:
            if not os.path.exists(directory_path):
                return []
            
            files = []
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    if extension is None or filename.endswith(extension):
                        files.append({
                            "filename": filename,
                            "path": file_path,
                            "size": os.path.getsize(file_path),
                            "modified_time": os.path.getmtime(file_path)
                        })
            
            return files
            
        except Exception as e:
            logger.error(f"Error listing files in directory {directory_path}: {e}")
            return []
    
    @staticmethod
    def safe_filename(filename: str) -> str:
        """生成安全的文件名"""
        # 移除或替换不安全的字符
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # 限制长度
        if len(filename) > 255:
            name, ext = os.path.splitext(filename)
            filename = name[:255-len(ext)] + ext
        
        return filename 