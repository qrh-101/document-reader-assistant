#!/usr/bin/env python3
"""
报告服务单元测试
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.report_service import ReportService
from app.core.config import settings

class TestReportService:
    """报告服务测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.report_service = ReportService()
    
    def test_initialization(self):
        """测试报告服务初始化"""
        assert self.report_service.pdf_service is not None
        assert self.report_service.prompt_service is not None
        assert self.report_service.client is not None
    
    @pytest.mark.asyncio
    async def test_call_openai_api(self):
        """测试OpenAI API调用"""
        # 模拟API响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "测试回复内容"
        
        with patch.object(self.report_service.client.chat.completions, 'create', return_value=mock_response):
            messages = [
                {'role': 'system', 'content': '你是一个助手。'},
                {'role': 'user', 'content': '你好'}
            ]
            
            response = await self.report_service._call_openai_api(messages)
            assert response == "测试回复内容"
    
    def test_combine_report_parts(self):
        """测试报告片段拼接"""
        parts = [
            "# 第一部分\n\n这是第一部分的内容。",
            "# 第二部分\n\n这是第二部分的内容。",
            "# 第三部分\n\n这是第三部分的内容。"
        ]
        
        combined = self.report_service._combine_report_parts(parts)
        
        # 由于输入已经以#开头，所以不会添加"# 研究报告"标题
        assert "第一部分" in combined
        assert "第二部分" in combined
        assert "第三部分" in combined
        
        # 测试不以#开头的情况
        parts_without_header = [
            "这是第一部分的内容。",
            "这是第二部分的内容。",
            "这是第三部分的内容。"
        ]
        
        combined_without_header = self.report_service._combine_report_parts(parts_without_header)
        assert "# 研究报告" in combined_without_header
    
    def test_clean_duplicate_headers(self):
        """测试清理重复标题"""
        report_with_duplicates = """
# 标题1
内容1

# 标题1
内容2

# 标题2
内容3

# 标题1
内容4
"""
        
        cleaned = self.report_service._clean_duplicate_headers(report_with_duplicates)
        
        # 统计标题1的出现次数
        title1_count = cleaned.count("# 标题1")
        assert title1_count == 1, f"标题1应该只出现1次，实际出现{title1_count}次"
        
        # 标题2应该保留
        assert "# 标题2" in cleaned
    
    def test_save_report(self):
        """测试报告保存"""
        report_id = "test-report-123"
        markdown_report = "# 测试报告\n\n这是测试内容。"
        question = "测试问题"
        
        # 使用临时目录进行测试
        with tempfile.TemporaryDirectory() as temp_dir:
            # 临时修改reports目录
            original_reports_dir = settings.reports_dir
            settings.reports_dir = temp_dir
            
            try:
                self.report_service._save_report(report_id, markdown_report, question)
                
                # 检查文件是否创建
                report_file = os.path.join(temp_dir, f"{report_id}.md")
                assert os.path.exists(report_file)
                
                # 检查文件内容
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    assert markdown_report in content
                    assert question in content
                    
            finally:
                # 恢复原始设置
                settings.reports_dir = original_reports_dir
    
    def test_get_report(self):
        """测试获取报告"""
        report_id = "test-report-456"
        expected_content = "# 测试报告\n\n这是测试内容。"
        
        # 使用临时目录进行测试
        with tempfile.TemporaryDirectory() as temp_dir:
            # 临时修改reports目录
            original_reports_dir = settings.reports_dir
            settings.reports_dir = temp_dir
            
            try:
                # 创建测试报告文件
                report_file = os.path.join(temp_dir, f"{report_id}.md")
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(expected_content)
                
                # 获取报告内容
                content = self.report_service.get_report(report_id)
                assert content == expected_content
                
            finally:
                # 恢复原始设置
                settings.reports_dir = original_reports_dir
    
    def test_get_report_not_found(self):
        """测试获取不存在的报告"""
        with pytest.raises(FileNotFoundError):
            self.report_service.get_report("non-existent-report")
    
    def test_list_reports(self):
        """测试报告列表"""
        # 使用临时目录进行测试
        with tempfile.TemporaryDirectory() as temp_dir:
            # 临时修改reports目录
            original_reports_dir = settings.reports_dir
            settings.reports_dir = temp_dir
            
            try:
                # 创建测试报告文件
                test_reports = [
                    ("report-1.md", "# 报告1\n\n内容1"),
                    ("report-2.md", "# 报告2\n\n内容2"),
                    ("report-3.md", "# 报告3\n\n内容3")
                ]
                
                for filename, content in test_reports:
                    filepath = os.path.join(temp_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                # 获取报告列表
                reports = self.report_service.list_reports()
                
                assert len(reports) == 3
                report_ids = [report['report_id'] for report in reports]
                assert 'report-1' in report_ids
                assert 'report-2' in report_ids
                assert 'report-3' in report_ids
                
            finally:
                # 恢复原始设置
                settings.reports_dir = original_reports_dir
    
    @pytest.mark.asyncio
    async def test_generate_report_integration(self):
        """测试报告生成集成"""
        # 模拟PDF服务
        mock_chunks = ["第一段内容", "第二段内容", "第三段内容"]
        self.report_service.pdf_service.process_pdf = Mock(return_value=mock_chunks)
        
        # 模拟提示词服务
        mock_messages = [
            {'role': 'system', 'content': '系统提示词'},
            {'role': 'user', 'content': '用户问题'}
        ]
        self.report_service.prompt_service.build_chat_messages = Mock(return_value=mock_messages)
        
        # 模拟API调用
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "生成的报告内容"
        
        with patch.object(self.report_service.client.chat.completions, 'create', return_value=mock_response):
            # 使用临时文件进行测试
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(b"fake pdf content")
                temp_file_path = temp_file.name
            
            try:
                result = await self.report_service.generate_report(temp_file_path, "测试问题")
                
                assert 'report_id' in result
                assert 'markdown_report' in result
                assert 'report_metadata' in result
                assert result['report_metadata'].total_chunks == 3
                assert result['report_metadata'].processed_chunks == 3
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path) 