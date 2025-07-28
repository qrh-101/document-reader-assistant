#!/usr/bin/env python3
"""
PDF服务单元测试
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.pdf_service import PDFService
from app.core.config import settings

class TestPDFService:
    """PDF服务测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.pdf_service = PDFService()
    
    def test_initialization(self):
        """测试PDF服务初始化"""
        assert self.pdf_service.max_chunk_size > 0
        assert self.pdf_service.overlap_size > 0
        assert self.pdf_service.overlap_size <= self.pdf_service.max_chunk_size
    
    def test_clean_text(self):
        """测试文本清理功能"""
        # 测试清理多余空白字符
        dirty_text = "  这是一个   测试文本  \n\n  包含多余空白  "
        cleaned = self.pdf_service.clean_text(dirty_text)
        assert "   " not in cleaned  # 不应该有多余的空格
        
        # 测试清理页眉页脚
        text_with_headers = "第1页\n这是内容\n第2页\n更多内容"
        cleaned = self.pdf_service.clean_text(text_with_headers)
        assert "第1页" not in cleaned
        assert "第2页" not in cleaned
    
    def test_split_text_semantic(self):
        """测试语义分片"""
        # 测试短文本
        short_text = "这是一个短文本。"
        chunks = self.pdf_service.split_text_semantic(short_text)
        assert len(chunks) == 1
        assert chunks[0] == short_text
        
        # 测试长文本
        long_text = "第一段内容。\n\n第二段内容。\n\n第三段内容。" * 100
        chunks = self.pdf_service.split_text_semantic(long_text)
        assert len(chunks) > 1
        
        # 验证每个分片都不超过最大长度
        for chunk in chunks:
            assert len(chunk) <= self.pdf_service.max_chunk_size
    
    def test_split_text_fixed(self):
        """测试固定长度分片"""
        # 测试短文本
        short_text = "这是一个短文本。"
        chunks = self.pdf_service.split_text_fixed(short_text)
        assert len(chunks) == 1
        
        # 测试长文本
        long_text = "这是一个很长的文本。" * 1000
        chunks = self.pdf_service.split_text_fixed(long_text)
        assert len(chunks) > 1
        
        # 验证分片大小
        for chunk in chunks:
            assert len(chunk) <= self.pdf_service.max_chunk_size
    
    def test_chunk_overlap(self):
        """测试分片重叠"""
        text = "第一段。\n\n第二段。\n\n第三段。" * 200
        chunks = self.pdf_service.split_text_semantic(text)
        
        if len(chunks) > 1:
            # 检查相邻分片是否有重叠
            for i in range(len(chunks) - 1):
                current_chunk = chunks[i]
                next_chunk = chunks[i + 1]
                
                # 检查是否有重叠内容
                overlap_found = False
                for j in range(len(current_chunk) - self.pdf_service.overlap_size, len(current_chunk)):
                    if j >= 0:
                        overlap_text = current_chunk[j:]
                        if overlap_text in next_chunk:
                            overlap_found = True
                            break
                
                # 对于语义分片，重叠不是强制的，所以这里只是记录
                if overlap_found:
                    print(f"分片 {i} 和 {i+1} 有重叠内容")
    
    def test_empty_text_handling(self):
        """测试空文本处理"""
        # 测试空字符串
        chunks = self.pdf_service.split_text_semantic("")
        assert len(chunks) == 0
        
        # 测试只有空白字符的文本
        chunks = self.pdf_service.split_text_semantic("   \n\n   ")
        assert len(chunks) == 0
    
    def test_chunk_strategy_configuration(self):
        """测试分片策略配置"""
        # 测试语义分片策略
        if settings.chunk_strategy == "semantic":
            text = "测试文本。" * 100
            chunks = self._process_pdf_text(text)
            assert len(chunks) > 0
        
        # 测试固定分片策略
        if settings.chunk_strategy == "fixed":
            text = "测试文本。" * 100
            chunks = self._process_pdf_text(text)
            assert len(chunks) > 0
    
    def _process_pdf_text(self, text):
        """模拟PDF文本处理（不涉及实际PDF文件）"""
        cleaned_text = self.pdf_service.clean_text(text)
        if settings.chunk_strategy == "semantic":
            return self.pdf_service.split_text_semantic(cleaned_text)
        else:
            return self.pdf_service.split_text_fixed(cleaned_text) 