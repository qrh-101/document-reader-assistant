"""
提示词管理器
用于加载和管理不同版本的提示词模板
"""
import os
from pathlib import Path
from typing import Dict, Optional
from loguru import logger


class PromptManager:
    """提示词管理器"""
    
    def __init__(self, prompts_dir: str = None):
        """
        初始化提示词管理器
        
        Args:
            prompts_dir: 提示词文件目录，默认为当前文件所在目录
        """
        if prompts_dir is None:
            prompts_dir = Path(__file__).parent
        
        self.prompts_dir = Path(prompts_dir)
        self._available_versions = self._discover_prompt_versions()
        
        logger.info(f"提示词管理器初始化完成，发现 {len(self._available_versions)} 个版本")
        logger.info(f"可用版本: {list(self._available_versions.keys())}")
    
    def _discover_prompt_versions(self) -> Dict[str, str]:
        """
        发现可用的提示词版本
        
        Returns:
            版本名称到文件路径的映射
        """
        versions = {}
        
        # 查找所有 system_prompt_*.md 文件
        for file_path in self.prompts_dir.glob("system_prompt_*.md"):
            version_name = file_path.stem.replace("system_prompt_", "")
            versions[version_name] = str(file_path)
            logger.debug(f"发现提示词版本: {version_name} -> {file_path}")
        
        # 查找默认的 system_prompt.md 文件
        default_prompt = self.prompts_dir / "system_prompt.md"
        if default_prompt.exists():
            versions["default"] = str(default_prompt)
            logger.debug(f"发现默认提示词: default -> {default_prompt}")
        
        return versions
    
    def get_available_versions(self) -> list:
        """
        获取所有可用的提示词版本
        
        Returns:
            可用版本列表
        """
        return list(self._available_versions.keys())
    
    def load_prompt(self, version: str = "default") -> str:
        """
        加载指定版本的提示词
        
        Args:
            version: 提示词版本，默认为 "default"
            
        Returns:
            提示词内容
            
        Raises:
            ValueError: 当指定版本不存在时
        """
        if version not in self._available_versions:
            available = self.get_available_versions()
            raise ValueError(f"提示词版本 '{version}' 不存在。可用版本: {available}")
        
        # 每次都从文件读取最新内容
        file_path = self._available_versions[version]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"成功加载提示词版本: {version} (文件: {file_path})")
                return content
        except Exception as e:
            logger.error(f"加载提示词版本 {version} 失败: {e}")
            raise
    
    def format_prompt(self, version: str, **kwargs) -> str:
        """
        格式化提示词模板
        
        Args:
            version: 提示词版本
            **kwargs: 模板参数
            
        Returns:
            格式化后的提示词
        """
        prompt_template = self.load_prompt(version)
        
        try:
            formatted_prompt = prompt_template.format(**kwargs)
            logger.debug(f"成功格式化提示词版本: {version}")
            return formatted_prompt
        except KeyError as e:
            logger.error(f"格式化提示词失败，缺少参数: {e}")
            raise
        except Exception as e:
            logger.error(f"格式化提示词失败: {e}")
            raise
    
    def reload_prompts(self):
        """重新加载所有提示词（兼容旧接口，无实际作用）"""
        self._available_versions = self._discover_prompt_versions()
        logger.info("提示词版本列表已刷新")
    
    def get_prompt_info(self, version: str) -> Dict:
        """
        获取提示词信息
        
        Args:
            version: 提示词版本
            
        Returns:
            提示词信息字典
        """
        if version not in self._available_versions:
            return {"error": f"版本 {version} 不存在"}
        
        file_path = Path(self._available_versions[version])
        info = {
            "version": version,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
            "last_modified": file_path.stat().st_mtime if file_path.exists() else 0
        }
        
        return info


# 全局提示词管理器实例
prompt_manager = PromptManager() 