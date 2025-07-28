#!/usr/bin/env python3
"""
配置验证测试
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

def test_config_validation():
    """验证配置是否正确"""
    print("🔧 配置验证结果:")
    print(f"LLM API Key: {'已设置' if settings.llm_api_key else '未设置'}")
    print(f"Model Name: {settings.model_name}")
    print(f"API Base: {settings.api_base}")
    print(f"Model Context Length: {settings.model_context_length:,} tokens")
    print(f"Max Tokens Per Chunk: {settings.max_tokens_per_chunk}")
    print(f"Temperature: {settings.temperature}")
    print(f"Reports Dir: {settings.reports_dir}")
    print(f"Upload Dir: {settings.upload_dir}")
    
    # 检查必要的配置
    if not settings.llm_api_key or settings.llm_api_key == "sk-test-key-for-development":
        print("⚠️  警告: 请设置真实的LLM API密钥")
    else:
        print("✅ LLM API密钥已配置")
    
    if settings.model_name == "qwen-turbo":
        print("✅ 模型配置正确")
    else:
        print("⚠️  警告: 当前模型不是qwen-turbo")
    
    if "dashscope" in settings.api_base:
        print("✅ API基础URL配置正确")
    else:
        print("⚠️  警告: API基础URL可能不正确")
    
    if settings.model_context_length >= 1000000:
        print("✅ 模型上下文长度配置正确")
    else:
        print("⚠️  警告: 模型上下文长度可能过小")

def test_required_settings():
    """测试必要的配置项"""
    assert settings.llm_api_key is not None, "LLM API密钥不能为空"
    assert settings.model_name is not None, "模型名称不能为空"
    assert settings.api_base is not None, "API基础URL不能为空"
    assert settings.model_context_length > 0, "模型上下文长度必须大于0"
    assert settings.max_tokens_per_chunk > 0, "最大token数必须大于0"

def test_model_configuration():
    """测试模型配置"""
    assert settings.model_name == "qwen-turbo", "当前配置的模型应该是qwen-turbo"
    assert "dashscope" in settings.api_base, "API基础URL应该包含dashscope"
    assert settings.model_context_length >= 1000000, "qwen-turbo的上下文长度应该至少为1M"

if __name__ == "__main__":
    test_config_validation() 