import time
import uuid
import os
from typing import List, Dict, Any
from openai import OpenAI
from loguru import logger
from app.core.config import settings
from app.services.pdf_service import PDFService
from app.services.prompt_service import PromptService
from app.schemas.report_schema import ReportMetadata

class ReportService:
    """报告生成服务"""
    
    def __init__(self):
        self.pdf_service = PDFService()
        self.prompt_service = PromptService()
        self.client = OpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.api_base
        )
    
    async def generate_report(self, pdf_path: str, question: str) -> Dict[str, Any]:
        """生成研究报告"""
        start_time = time.time()
        report_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Starting report generation for question: {question}")
            
            # 1. 处理PDF文件
            chunks = self.pdf_service.process_pdf(pdf_path)
            total_chunks = len(chunks)
            
            if total_chunks == 0:
                raise ValueError("PDF文件内容为空或无法解析")
            
            logger.info(f"PDF processed into {total_chunks} chunks")
            
            # 2. 分段调用大模型
            report_parts = []
            processed_chunks = 0
            
            for i, chunk in enumerate(chunks):
                try:
                    # 构建Prompt
                    messages = self.prompt_service.build_chat_messages(
                        question=question,
                        chunk_content=chunk,
                        chunk_index=i,
                        total_chunks=total_chunks
                    )
                    
                    # 调用OpenAI API
                    response = await self._call_openai_api(messages)
                    
                    if response and response.strip():
                        report_parts.append(response.strip())
                        processed_chunks += 1
                        logger.info(f"Processed chunk {i + 1}/{total_chunks}")
                    else:
                        logger.warning(f"Empty response for chunk {i + 1}")
                        
                except Exception as e:
                    logger.error(f"Error processing chunk {i + 1}: {e}")
                    # 继续处理其他片段
                    continue
            
            # 3. 拼接报告
            if not report_parts:
                raise ValueError("所有片段处理失败，无法生成报告")
            
            markdown_report = self._combine_report_parts(report_parts)
            
            # 4. 保存报告
            self._save_report(report_id, markdown_report, question)
            
            # 5. 计算处理时间
            processing_time = time.time() - start_time
            
            # 6. 构建元数据
            metadata = ReportMetadata(
                total_chunks=total_chunks,
                processed_chunks=processed_chunks,
                token_per_chunk=settings.max_tokens_per_chunk,
                chunk_size=self.pdf_service.max_chunk_size,
                overlap_size=self.pdf_service.overlap_size,
                model_context_length=settings.model_context_length,
                processing_time=processing_time,
                model_used=settings.model_name
            )
            
            logger.info(f"Report generation completed: {report_id}")
            
            return {
                "report_id": report_id,
                "markdown_report": markdown_report,
                "report_metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    async def _call_openai_api(self, messages: List[Dict[str, str]]) -> str:
        """调用OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=settings.model_name,
                messages=messages,
                max_tokens=settings.max_tokens_per_chunk,
                temperature=settings.temperature,
                timeout=60
            )
            
            content = response.choices[0].message.content
            return content if content else ""
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise
    
    def _combine_report_parts(self, parts: List[str]) -> str:
        """拼接报告片段"""
        try:
            # 简单的拼接策略
            combined_report = "\n\n".join(parts)
            
            # 清理重复的标题
            combined_report = self._clean_duplicate_headers(combined_report)
            
            # 确保报告有合适的结构
            if not combined_report.startswith("#"):
                combined_report = "# 研究报告\n\n" + combined_report
            
            return combined_report
            
        except Exception as e:
            logger.error(f"Error combining report parts: {e}")
            raise
    
    def _clean_duplicate_headers(self, report: str) -> str:
        """清理重复的标题"""
        lines = report.split('\n')
        cleaned_lines = []
        seen_headers = set()
        
        for line in lines:
            if line.strip().startswith('#'):
                # 提取标题文本（去除#符号）
                header_text = line.strip().lstrip('#').strip()
                if header_text not in seen_headers:
                    cleaned_lines.append(line)
                    seen_headers.add(header_text)
            else:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _save_report(self, report_id: str, markdown_report: str, question: str):
        """保存报告到文件"""
        try:
            # 确保reports目录存在
            os.makedirs(settings.reports_dir, exist_ok=True)
            
            # 保存Markdown文件
            report_file_path = os.path.join(settings.reports_dir, f"{report_id}.md")
            
            with open(report_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# 研究报告\n\n")
                f.write(f"**研究问题**: {question}\n\n")
                f.write(f"**报告ID**: {report_id}\n\n")
                f.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                f.write(markdown_report)
            
            logger.info(f"Report saved to: {report_file_path}")
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            raise
    
    def get_report(self, report_id: str) -> str:
        """获取报告内容"""
        try:
            report_file_path = os.path.join(settings.reports_dir, f"{report_id}.md")
            
            if not os.path.exists(report_file_path):
                raise FileNotFoundError(f"Report not found: {report_id}")
            
            with open(report_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content
            
        except Exception as e:
            logger.error(f"Error getting report {report_id}: {e}")
            raise
    
    def list_reports(self) -> List[Dict[str, Any]]:
        """列出所有报告"""
        try:
            reports = []
            
            if not os.path.exists(settings.reports_dir):
                return reports
            
            for filename in os.listdir(settings.reports_dir):
                if filename.endswith('.md'):
                    report_id = filename[:-3]  # 移除.md后缀
                    report_path = os.path.join(settings.reports_dir, filename)
                    
                    try:
                        with open(report_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 提取基本信息
                        lines = content.split('\n')
                        question = ""
                        created_at = ""
                        
                        for line in lines:
                            if line.startswith('**研究问题**:'):
                                question = line.replace('**研究问题**:', '').strip()
                            elif line.startswith('**生成时间**:'):
                                created_at = line.replace('**生成时间**:', '').strip()
                        
                        reports.append({
                            "report_id": report_id,
                            "question": question,
                            "created_at": created_at,
                            "file_size": os.path.getsize(report_path)
                        })
                        
                    except Exception as e:
                        logger.warning(f"Error reading report {filename}: {e}")
                        continue
            
            # 按创建时间排序
            reports.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            return reports
            
        except Exception as e:
            logger.error(f"Error listing reports: {e}")
            raise 