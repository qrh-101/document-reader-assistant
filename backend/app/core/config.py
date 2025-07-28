from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API配置
    api_v1_str: str = "/api/v1"
    project_name: str = "DeepResearch"
    
    # 大模型API配置
    llm_api_key: str = "sk-test-key-for-development"  # 百炼API Key
    model_name: str = "qwen-turbo"
    api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_context_length: int = 1000000  # qwen-turbo上下文长度为1M tokens
    max_tokens_per_chunk: int = 500
    temperature: float = 0.7
    
    # PDF处理配置
    chunk_strategy: str = "semantic"
    max_chunk_size: int = 2000
    overlap_size: int = 200
    
    # 文件存储配置
    reports_dir: str = "reports"
    upload_dir: str = "uploads"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "protected_namespaces": ("settings_",)
    }

# 创建全局设置实例
settings = Settings()

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        settings.reports_dir,
        settings.upload_dir,
        os.path.dirname(settings.log_file)
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# 初始化时创建目录
ensure_directories() 