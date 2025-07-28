import fitz  # PyMuPDF
import re
from typing import List, Tuple
from loguru import logger
from app.core.config import settings

class PDFService:
    """PDF文档解析与分片服务"""
    
    def __init__(self):
        # 根据模型上下文长度智能计算分片大小
        self.max_chunk_size = self._calculate_optimal_chunk_size()
        self.overlap_size = self._calculate_overlap_size()
        logger.info(f"PDF Service initialized with chunk_size={self.max_chunk_size}, overlap_size={self.overlap_size}")
    
    def _calculate_optimal_chunk_size(self) -> int:
        """根据模型上下文长度智能计算最优分片大小"""
        context_length = settings.model_context_length
        
        # 为系统提示词、用户问题、输出内容预留空间
        system_prompt_reserve = 2000  # 系统提示词大约2000 tokens
        user_question_reserve = 1000  # 用户问题大约1000 tokens
        output_reserve = settings.max_tokens_per_chunk  # 输出内容
        safety_margin = 1000  # 安全边距
        
        # 计算可用于输入文本的最大tokens
        available_tokens = context_length - system_prompt_reserve - user_question_reserve - output_reserve - safety_margin
        
        # 将tokens转换为字符数（粗略估计：1 token ≈ 4个字符）
        max_chars = available_tokens * 4
        
        # 确保不超过配置的最大值
        max_chars = min(max_chars, settings.max_chunk_size)
        
        # 确保至少有合理的最小值
        min_chars = 1000
        max_chars = max(max_chars, min_chars)
        
        logger.info(f"Model context length: {context_length}, calculated optimal chunk size: {max_chars}")
        return int(max_chars)
    
    def _calculate_overlap_size(self) -> int:
        """根据分片大小计算重叠大小"""
        # 重叠大小设为分片大小的10%，但不超过配置的最大值
        overlap = min(self.max_chunk_size // 10, settings.overlap_size)
        # 确保至少有200字符的重叠
        overlap = max(overlap, 200)
        return overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """从PDF文件中提取文本内容"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            logger.info(f"Successfully extracted text from PDF: {pdf_path}")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise
    
    def clean_text(self, text: str) -> str:
        """清理和预处理文本"""
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()\[\]{}"\'-]', '', text)
        # 移除页眉页脚等重复内容
        text = re.sub(r'第\s*\d+\s*页', '', text)
        text = re.sub(r'Page\s*\d+', '', text)
        
        return text.strip()
    
    def split_text_semantic(self, text: str) -> List[str]:
        """基于语义的文本分片"""
        # 按段落分割
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # 如果当前段落加上现有内容超过最大长度，保存当前块并开始新块
            if len(current_chunk) + len(paragraph) > self.max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    # 保留重叠部分
                    overlap_start = max(0, len(current_chunk) - self.overlap_size)
                    current_chunk = current_chunk[overlap_start:] + "\n\n" + paragraph
                else:
                    # 如果单个段落就超过最大长度，强制分割
                    current_chunk = paragraph[:self.max_chunk_size]
                    chunks.append(current_chunk)
                    current_chunk = paragraph[self.max_chunk_size - self.overlap_size:]
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
        
        # 添加最后一个块
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def split_text_fixed(self, text: str) -> List[str]:
        """固定长度的文本分片"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.max_chunk_size
            chunk = text[start:end]
            
            # 尝试在句子边界分割
            if end < len(text):
                last_period = chunk.rfind('.')
                last_exclamation = chunk.rfind('!')
                last_question = chunk.rfind('?')
                last_newline = chunk.rfind('\n')
                
                split_point = max(last_period, last_exclamation, last_question, last_newline)
                
                if split_point > start + self.max_chunk_size * 0.7:  # 如果找到合适的分割点
                    chunk = chunk[:split_point + 1]
                    end = start + split_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.overlap_size
        
        logger.info(f"Split text into {len(chunks)} fixed-size chunks")
        return chunks
    
    def process_pdf(self, pdf_path: str) -> List[str]:
        """处理PDF文件并返回分片后的文本"""
        try:
            # 提取文本
            raw_text = self.extract_text_from_pdf(pdf_path)
            
            # 清理文本
            cleaned_text = self.clean_text(raw_text)
            
            # 根据策略分片
            if settings.chunk_strategy == "semantic":
                chunks = self.split_text_semantic(cleaned_text)
            else:
                chunks = self.split_text_fixed(cleaned_text)
            
            # 过滤空块
            chunks = [chunk for chunk in chunks if chunk.strip()]
            
            logger.info(f"Successfully processed PDF: {len(chunks)} chunks created")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise
    
    def get_pdf_info(self, pdf_path: str) -> dict:
        """获取PDF文件信息"""
        try:
            doc = fitz.open(pdf_path)
            info = {
                "page_count": len(doc),
                "file_size": doc.filesize,
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", "")
            }
            doc.close()
            return info
        except Exception as e:
            logger.error(f"Error getting PDF info {pdf_path}: {e}")
            raise 