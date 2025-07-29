import os
from typing import Dict, Any
from loguru import logger
from app.core.config import settings
from app.prompts.prompt_manager import prompt_manager

class PromptService:
    """Prompt构建与参数渲染服务"""
    
    def __init__(self):
        self.prompt_version = settings.prompt_version
        logger.info(f"初始化PromptService，使用提示词版本: {self.prompt_version}")
    
    def _load_prompt_template(self) -> str:
        """加载系统Prompt模板"""
        try:
            template = prompt_manager.load_prompt(self.prompt_version)
            logger.info(f"成功加载提示词版本: {self.prompt_version}")
            return template
        except Exception as e:
            logger.error(f"加载提示词版本 {self.prompt_version} 失败: {e}")
            # 尝试加载默认版本
            try:
                template = prompt_manager.load_prompt("default")
                logger.info("回退到默认提示词版本")
                return template
            except Exception as e2:
                logger.error(f"加载默认提示词也失败: {e2}")
                return self._get_default_template()
    
    def _get_default_template(self) -> str:
        """获取默认的Prompt模板"""
        return """# 智能文档研究助手系统提示词

你是一个专业的文档研究助手，擅长分析PDF文档内容并生成结构化的研究报告。

## 任务描述
基于用户提供的研究问题和PDF文档片段，生成高质量的Markdown格式研究报告。

## 用户问题
{question}

## PDF文档片段内容
{chunk_content}

## 输出要求

### 1. 内容要求
- 基于提供的PDF片段内容进行分析
- 结合用户的研究问题进行深入探讨
- 确保内容准确、客观、有逻辑性
- 避免重复和冗余内容

### 2. 格式要求
- 使用标准的Markdown格式
- 合理使用标题层级（#、##、###等）
- 适当使用列表、引用、强调等格式
- 保持段落结构清晰

### 3. 结构要求
- 如果这是第一个片段，请包含报告标题和引言
- 如果是中间片段，请专注于具体内容分析
- 如果是最后一个片段，请包含总结和结论
- 确保与前后片段的逻辑连贯性

### 4. 字数控制
- 每个片段的输出控制在{max_tokens}字以内
- 确保内容完整，不要截断重要信息

## 注意事项
1. 只基于提供的PDF片段内容进行分析
2. 保持客观中立的分析态度
3. 使用专业但易懂的语言
4. 确保内容的逻辑性和连贯性
5. 如果片段内容与问题关联度不高，请说明并适当调整分析角度"""
    
    def render_prompt(self, question: str, chunk_content: str, chunk_index: int = 0, total_chunks: int = 1) -> str:
        """渲染Prompt模板"""
        try:
            # 准备模板参数
            template_params = {
                "question": question,
                "chunk_content": chunk_content,
                "max_tokens": settings.max_tokens_per_chunk,
                "chunk_index": chunk_index,
                "total_chunks": total_chunks
            }
            
            # 使用提示词管理器格式化模板
            rendered_prompt = prompt_manager.format_prompt(self.prompt_version, **template_params)
            
            logger.info(f"成功渲染提示词，版本: {self.prompt_version}, 片段: {chunk_index + 1}/{total_chunks}")
            return rendered_prompt
            
        except Exception as e:
            logger.error(f"渲染提示词失败: {e}")
            raise
    
    def build_chat_messages(self, question: str, chunk_content: str, chunk_index: int = 0, total_chunks: int = 1) -> list:
        """构建聊天消息格式"""
        try:
            system_prompt = self.render_prompt(question, chunk_content, chunk_index, total_chunks)
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"请基于上述要求，分析PDF片段内容并生成研究报告。这是第{chunk_index + 1}个片段，共{total_chunks}个片段。"
                }
            ]
            
            return messages
            
        except Exception as e:
            logger.error(f"Error building chat messages: {e}")
            raise
    
    def validate_prompt_params(self, question: str, chunk_content: str) -> bool:
        """验证Prompt参数"""
        if not question or not question.strip():
            logger.error("Question is empty or invalid")
            return False
        
        if not chunk_content or not chunk_content.strip():
            logger.error("Chunk content is empty or invalid")
            return False
        
        if len(question) > 1000:
            logger.error("Question is too long (max 1000 characters)")
            return False
        
        return True
    
    def get_prompt_stats(self, question: str, chunk_content: str) -> Dict[str, Any]:
        """获取Prompt统计信息"""
        return {
            "question_length": len(question),
            "chunk_content_length": len(chunk_content),
            "max_tokens_per_chunk": settings.max_tokens_per_chunk,
            "model_name": settings.model_name,
            "temperature": settings.temperature,
            "prompt_version": self.prompt_version
        }
    
    def get_available_prompt_versions(self) -> list:
        """获取可用的提示词版本列表"""
        return prompt_manager.get_available_versions()
    
    def get_prompt_info(self, version: str = None) -> Dict:
        """获取提示词信息"""
        if version is None:
            version = self.prompt_version
        return prompt_manager.get_prompt_info(version) 