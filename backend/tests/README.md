# 测试说明

> 本测试体系基于 `../backend_test_best_practice_prompt.md` 自动生成，遵循统一的后端测试最佳实践。

## 概述

本目录包含DeepResearch后端的所有测试文件，按照最佳实践组织，确保代码质量和功能可靠性。

## 测试结构

- 详细测试结构、类型、最佳实践请参见：`../backend_test_best_practice_prompt.md`

## 测试类型

### 1. 配置测试 (`test_config.py`)
- 验证环境变量配置
- 检查模型参数设置
- 确认API密钥配置

### 2. API测试 (`test_qwen_api.py`)
- 测试百炼API连接
- 验证模型响应
- 检查API调用参数

### 3. 功能测试 (`test_smart_chunking.py`)
- 测试智能分片算法
- 验证上下文优化
- 检查分片大小计算

### 4. 单元测试
- **PDF服务测试** (`test_pdf_service.py`)
  - 文本清理功能
  - 语义分片算法
  - 固定长度分片
  - 分片重叠处理

- **报告服务测试** (`test_report_service.py`)
  - API调用模拟
  - 报告拼接逻辑
  - 文件保存和读取
  - 错误处理

## 运行测试

### 使用测试运行脚本

```bash
# 运行所有测试
python run_tests.py

# 运行特定类型测试
python run_tests.py config    # 配置验证
python run_tests.py api       # API测试
python run_tests.py chunking  # 智能分片测试
python run_tests.py unit      # 单元测试

# 运行特定测试文件
python run_tests.py pdf_service
python run_tests.py report_service
```

### 使用pytest直接运行

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_pdf_service.py -v
pytest tests/test_report_service.py -v

# 运行特定测试函数
pytest tests/test_pdf_service.py::TestPDFService::test_clean_text -v

# 生成覆盖率报告
pytest --cov=app tests/ --cov-report=html
```

## 测试环境

### 临时目录
- 所有测试使用临时目录，避免污染生产环境
- 测试完成后自动清理临时文件
- 支持并行测试执行

### Mock和Fixtures
- 使用pytest fixtures提供测试数据
- 使用unittest.mock模拟外部依赖
- 提供示例PDF内容和文本内容

### 配置隔离
- 测试时临时修改配置，测试完成后恢复
- 避免测试影响生产配置
- 支持不同环境的测试配置

## 添加新测试

### 1. 创建测试文件
```python
#!/usr/bin/env python3
"""
新功能测试
"""

import pytest
from app.services.your_service import YourService

class TestYourService:
    """新服务测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.service = YourService()
    
    def test_your_function(self):
        """测试新功能"""
        result = self.service.your_function()
        assert result is not None
```

### 2. 更新测试运行脚本
在`run_tests.py`中添加新的测试类型：

```python
elif command == "your_test":
    success = run_specific_test("your_service")
```

### 3. 更新文档
在`tests/README.md`中添加新测试的说明。

## 持续集成

### GitHub Actions
```yaml
- name: Run Tests
  run: |
    cd backend
    python run_tests.py all
```

### 本地开发
```bash
# 开发前运行测试
python run_tests.py unit

# 提交前运行完整测试
python run_tests.py all
```

## 故障排除

### 常见问题

1. **测试失败**: 检查环境变量配置
2. **API测试失败**: 确认网络连接和API密钥
3. **文件权限错误**: 检查临时目录权限
4. **导入错误**: 确认Python路径设置

### 调试技巧

1. 使用`-v`参数查看详细输出
2. 使用`-s`参数查看print输出
3. 使用`--tb=long`查看完整错误信息
4. 使用`pytest --pdb`进入调试模式 