"""
Pytest配置文件
"""

import pytest
import tempfile
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.config import settings

@pytest.fixture(scope="session")
def temp_test_dir():
    """创建临时测试目录"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture(autouse=True)
def setup_test_environment(temp_test_dir):
    """设置测试环境"""
    # 保存原始配置
    original_reports_dir = settings.reports_dir
    original_upload_dir = settings.upload_dir
    original_log_file = settings.log_file
    
    # 设置测试目录
    settings.reports_dir = os.path.join(temp_test_dir, "reports")
    settings.upload_dir = os.path.join(temp_test_dir, "uploads")
    settings.log_file = os.path.join(temp_test_dir, "logs", "test.log")
    
    # 创建必要的目录
    os.makedirs(settings.reports_dir, exist_ok=True)
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
    
    yield
    
    # 恢复原始配置
    settings.reports_dir = original_reports_dir
    settings.upload_dir = original_upload_dir
    settings.log_file = original_log_file

@pytest.fixture
def sample_pdf_content():
    """示例PDF内容"""
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"

@pytest.fixture
def sample_text_content():
    """示例文本内容"""
    return """
    人工智能的发展历程
    
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    
    发展历程
    
    人工智能的发展可以分为几个阶段：
    
    1. 初期发展（1950-1969）
    在这个阶段，人工智能的概念刚刚提出，主要研究领域包括问题求解、自然语言处理等。
    
    2. 第一次低谷（1970-1980）
    由于技术限制和资金问题，人工智能研究进入低谷期。
    
    3. 复兴期（1980-1990）
    专家系统的兴起带动了人工智能的复兴。
    
    4. 快速发展期（1990至今）
    机器学习、深度学习等技术的突破推动了人工智能的快速发展。
    
    应用领域
    
    人工智能在各个领域都有广泛应用：
    
    - 医疗健康：疾病诊断、药物研发
    - 金融：风险评估、智能投顾
    - 教育：个性化学习、智能辅导
    - 交通：自动驾驶、交通优化
    - 制造业：智能制造、质量控制
    
    未来展望
    
    随着技术的不断进步，人工智能将在更多领域发挥重要作用，为人类社会的发展做出更大贡献。
    """ 