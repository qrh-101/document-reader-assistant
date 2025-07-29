#!/usr/bin/env python3
"""
提示词管理器测试脚本
用于测试多套提示词的管理和切换功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.prompts.prompt_manager import prompt_manager
from app.core.config import settings
from loguru import logger

def test_prompt_manager():
    """测试提示词管理器功能"""
    print("=" * 60)
    print("提示词管理器测试")
    print("=" * 60)
    
    # 1. 测试可用版本发现
    print("\n1. 测试可用版本发现:")
    available_versions = prompt_manager.get_available_versions()
    print(f"可用版本: {available_versions}")
    
    # 2. 测试当前配置版本
    print(f"\n2. 当前配置版本: {settings.prompt_version}")
    
    # 3. 测试加载各个版本
    print("\n3. 测试加载各个版本:")
    for version in available_versions:
        try:
            content = prompt_manager.load_prompt(version)
            print(f"✓ 版本 {version}: 加载成功 (长度: {len(content)} 字符)")
        except Exception as e:
            print(f"✗ 版本 {version}: 加载失败 - {e}")
    
    # 4. 测试格式化功能
    print("\n4. 测试格式化功能:")
    test_params = {
        "question": "如何提高工作效率？",
        "chunk_content": "这是一个测试的PDF内容片段。",
        "max_tokens": 500
    }
    
    for version in available_versions[:2]:  # 只测试前两个版本
        try:
            formatted = prompt_manager.format_prompt(version, **test_params)
            print(f"✓ 版本 {version}: 格式化成功")
            print(f"  格式化后长度: {len(formatted)} 字符")
        except Exception as e:
            print(f"✗ 版本 {version}: 格式化失败 - {e}")
    
    # 5. 测试提示词信息获取
    print("\n5. 测试提示词信息获取:")
    for version in available_versions:
        try:
            info = prompt_manager.get_prompt_info(version)
            print(f"✓ 版本 {version}:")
            print(f"  文件路径: {info.get('file_path', 'N/A')}")
            print(f"  文件大小: {info.get('file_size', 'N/A')} 字节")
            print(f"  是否缓存: {info.get('is_cached', 'N/A')}")
        except Exception as e:
            print(f"✗ 版本 {version}: 获取信息失败 - {e}")
    
    # 6. 测试缓存功能
    print("\n6. 测试缓存功能:")
    print("清除缓存前，缓存状态:")
    for version in available_versions:
        info = prompt_manager.get_prompt_info(version)
        print(f"  版本 {version}: {'已缓存' if info.get('is_cached') else '未缓存'}")
    
    prompt_manager.reload_prompts()
    print("清除缓存后，缓存状态:")
    for version in available_versions:
        info = prompt_manager.get_prompt_info(version)
        print(f"  版本 {version}: {'已缓存' if info.get('is_cached') else '未缓存'}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

def test_prompt_service():
    """测试提示词服务功能"""
    print("\n" + "=" * 60)
    print("提示词服务测试")
    print("=" * 60)
    
    from app.services.prompt_service import PromptService
    
    prompt_service = PromptService()
    
    # 1. 测试渲染功能
    print("\n1. 测试提示词渲染:")
    try:
        rendered = prompt_service.render_prompt(
            question="如何提高工作效率？",
            chunk_content="这是一个测试的PDF内容片段。",
            chunk_index=0,
            total_chunks=1
        )
        print(f"✓ 渲染成功，长度: {len(rendered)} 字符")
        print(f"  使用版本: {prompt_service.prompt_version}")
    except Exception as e:
        print(f"✗ 渲染失败: {e}")
    
    # 2. 测试聊天消息构建
    print("\n2. 测试聊天消息构建:")
    try:
        messages = prompt_service.build_chat_messages(
            question="如何提高工作效率？",
            chunk_content="这是一个测试的PDF内容片段。",
            chunk_index=0,
            total_chunks=1
        )
        print(f"✓ 消息构建成功，消息数量: {len(messages)}")
        for i, msg in enumerate(messages):
            print(f"  消息 {i+1}: {msg['role']} (长度: {len(msg['content'])} 字符)")
    except Exception as e:
        print(f"✗ 消息构建失败: {e}")
    
    # 3. 测试统计信息
    print("\n3. 测试统计信息:")
    try:
        stats = prompt_service.get_prompt_stats(
            question="如何提高工作效率？",
            chunk_content="这是一个测试的PDF内容片段。"
        )
        print("✓ 统计信息获取成功:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ 统计信息获取失败: {e}")
    
    # 4. 测试版本管理
    print("\n4. 测试版本管理:")
    try:
        versions = prompt_service.get_available_prompt_versions()
        print(f"✓ 可用版本: {versions}")
        
        current_info = prompt_service.get_prompt_info()
        print(f"✓ 当前版本信息: {current_info}")
    except Exception as e:
        print(f"✗ 版本管理失败: {e}")
    
    print("\n" + "=" * 60)
    print("提示词服务测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_prompt_manager()
        test_prompt_service()
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        sys.exit(1) 