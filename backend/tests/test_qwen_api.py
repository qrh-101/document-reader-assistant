#!/usr/bin/env python3
"""
测试百炼API配置的脚本
"""

import os
import asyncio
import pytest
import sys
from pathlib import Path
from openai import OpenAI

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

async def test_qwen_api():
    """测试百炼API连接"""
    try:
        print("🔧 正在测试百炼API配置...")
        print(f"API Base: {settings.api_base}")
        print(f"Model: {settings.model_name}")
        print(f"API Key: {settings.llm_api_key[:10]}..." if settings.llm_api_key else "未设置")
        
        # 创建客户端
        client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.api_base
        )
        
        # 测试简单对话
        print("\n🤖 正在测试模型对话...")
        completion = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {'role': 'system', 'content': '你是一个有用的AI助手。'},
                {'role': 'user', 'content': '请简单介绍一下你自己。'}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content
        print(f"✅ API测试成功！")
        print(f"模型回复: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

@pytest.mark.asyncio
@pytest.mark.api
async def test_api_connection():
    """测试API连接"""
    # 跳过API测试，因为需要真实的API密钥
    pytest.skip("需要真实的API密钥才能运行API测试")
    result = await test_qwen_api()
    assert result, "API连接测试失败"

@pytest.mark.asyncio
@pytest.mark.api
async def test_model_response():
    """测试模型响应"""
    # 跳过API测试，因为需要真实的API密钥
    pytest.skip("需要真实的API密钥才能运行API测试")
    
    try:
        client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.api_base
        )
        
        completion = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {'role': 'user', 'content': '你好'}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        response = completion.choices[0].message.content
        assert response is not None, "模型响应不能为空"
        assert len(response) > 0, "模型响应不能为空字符串"
        
    except Exception as e:
        pytest.fail(f"模型响应测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_qwen_api()) 