# DeepResearch 后端测试最佳实践 Prompt

本 prompt 适用于已生成的后端或全栈项目，结合实际项目结构和代码，自动生成高质量、规范化的后端测试体系和测试文件。

---

## 🧪 后端测试最佳实践

为保证后端服务的健壮性、可维护性和开发效率，建议在项目初始化时同步生成完善的自动化测试体系。具体最佳实践如下：

### 1. 统一测试目录结构
- 所有测试文件统一放在 `backend/tests/` 目录下，结构清晰，便于管理和扩展。
- 每个核心模块（如 services、schemas、routers）建议对应独立的测试文件（如 `test_pdf_service.py`、`test_report_service.py`）。
- 提供 `conftest.py` 配置全局fixture，实现测试环境隔离、临时目录、样例数据等。

### 2. 测试用例设计
- **单元测试**：聚焦于单一函数/类的功能正确性，mock外部依赖，保证测试原子性。
- **集成测试**：覆盖模块间协作流程，如报告生成全流程、接口调用等。
- **配置与环境测试**：如 `test_config.py`，确保环境变量、模型参数等配置项正确加载。
- **API测试**：如 `test_qwen_api.py`，可通过pytest marker（如 `@pytest.mark.api`）与主流程隔离，默认跳过，需真实API key时手动运行。

### 3. Mock与依赖隔离
- 对大模型API、文件IO等外部依赖，优先使用 `unittest.mock` 进行mock，避免真实请求，提升测试速度与稳定性。
- 对于异步API，使用 `pytest-asyncio` 支持async测试与mock。

### 4. 路径与导入兼容
- 在每个测试文件开头添加如下代码，确保`app`模块可被正确导入：
  ```python
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent
  sys.path.insert(0, str(project_root))
  ```
- 保证本地开发、CI环境下均可直接运行所有测试。

### 5. 测试脚本与运行
- 提供统一的测试运行脚本（如 `run_tests.py`），支持：
  - 一键运行全部测试
  - 跳过/单独运行API测试（如 `python run_tests.py api`）
  - 输出详细报告与覆盖率统计
- 推荐命令：
  ```bash
  python run_tests.py           # 运行全部测试（跳过API测试）
  python run_tests.py api       # 仅运行API相关测试
  python -m pytest tests/ -v    # 直接用pytest运行
  ```

### 6. CI/CD集成建议
- 在CI流程中集成自动化测试，确保每次提交均通过全部测试。
- 可选集成覆盖率工具（如 `pytest-cov`），持续提升代码质量。

### 7. 示例测试文件建议
- `test_config.py`：环境变量与配置项校验
- `test_pdf_service.py`：PDF分片与清洗逻辑
- `test_report_service.py`：报告拼接、存储、mock大模型调用
- `test_qwen_api.py`：API连通性（默认跳过）
- `conftest.py`：全局fixture与测试环境隔离

通过以上最佳实践，项目初始化时即可生成高质量、可扩展的测试体系，支持开发过程中的快速回归与功能验证，大幅提升开发效率与代码可靠性。 