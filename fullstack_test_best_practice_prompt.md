# 通用全栈测试最佳实践 Prompt

本 prompt 适用于所有已生成的业务全栈项目，结合实际前后端项目结构和代码，自动生成高质量、规范化的测试体系和测试文件。

---

## 🧪 全栈测试最佳实践

### 一、后端测试最佳实践
- 统一测试目录结构，所有测试文件统一放在 `backend/tests/` 目录下，结构清晰，便于管理和扩展。
- 每个核心模块（如 services、schemas、routers）建议对应独立的测试文件（如 `test_pdf_service.py`、`test_report_service.py`）。
- 提供 `conftest.py` 配置全局fixture，实现测试环境隔离、临时目录、样例数据等。
- 单元测试、集成测试、配置与环境测试、API测试分层设计。
- 对大模型API、文件IO等外部依赖，优先使用 `unittest.mock` 进行mock，避免真实请求，提升测试速度与稳定性。
- 对于异步API，使用 `pytest-asyncio` 支持async测试与mock。
- 在每个测试文件开头添加如下代码，确保`app`模块可被正确导入：
  ```python
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent
  sys.path.insert(0, str(project_root))
  ```
- 保证本地开发、CI环境下均可直接运行所有测试。
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
- 在CI流程中集成自动化测试，确保每次提交均通过全部测试。
- 可选集成覆盖率工具（如 `pytest-cov`），持续提升代码质量。
- 示例测试文件建议：
  - `test_config.py`：环境变量与配置项校验
  - `test_pdf_service.py`：PDF分片与清洗逻辑
  - `test_report_service.py`：报告拼接、存储、mock大模型调用
  - `test_qwen_api.py`：API连通性（默认跳过）
  - `conftest.py`：全局fixture与测试环境隔离

### 二、前端测试最佳实践
- 单元测试与被测组件/函数/Store 同级，命名为 `xxx.spec.ts(x)` 或 `xxx.test.ts(x)`，便于就近维护和查找。
- 集成测试/端到端测试集中放在 `src/__tests__/` 或 `e2e/` 目录下，关注业务流转和用户操作全流程。
- 单元测试、组件测试、集成测试、端到端（E2E）测试分层设计。
- 使用 Vitest/Jest/Testing Library 的 mock 能力，隔离 API 请求、全局依赖、第三方库等。
- 推荐 MSW（Mock Service Worker）或 jest.mock/axios-mock-adapter 进行接口 mock。
- 对于全局 store，可用 mock store 或自定义测试 store。
- 测试环境建议与开发环境一致（如 Vite + Vitest），保证测试用例在本地、CI/CD 环境下均可直接运行。
- 配置 `jsdom` 作为测试环境，模拟浏览器 API。
- 保证 TypeScript 类型校验通过，测试代码同样遵循类型安全。
- `package.json` 已配置标准测试命令：
  - `npm run test`：运行所有测试
  - `npm run test:unit`：运行单元测试
  - `npm run test:watch`：监听模式
  - `npm run test:coverage`：生成覆盖率报告
  - `npm run test:e2e`：运行端到端测试（如集成 Cypress）
- 在 CI 流程中集成自动化测试，确保每次提交均通过全部测试。
- 集成覆盖率工具（如 `vitest --coverage`），持续提升代码质量。
- E2E 测试可在 PR 合并前自动运行，保障主流程稳定。
- 典型测试文件建议：
  - `*.spec.ts(x)` / `*.test.ts(x)`：单元/组件测试（与业务代码同级）
  - `AppFlow.spec.ts` 等：集成测试（集中存放）
  - `e2e/` 目录下存放端到端测试脚本
- 组件内部所有依赖对象字段访问（如 `metadata.processing_time`）应加可选链（`?.`）或默认值（`?? 0`），保证健壮性，防止测试或运行时因 mock 不全报错。
- 前端测试 mock 只需保证主流程（如 createReport、fetchReportDetail、currentReport），无需模拟完整响应式链条或所有字段细节。
- 集成测试断言只关注页面主内容（如“测试报告”“内容”），不必断言所有元数据细节，避免陷入 mock 死循环。
- 推荐使用 `await waitFor` 等异步断言，确保页面渲染完成后再断言内容。

# DeepResearch 全栈测试最佳实践 Prompt

本 prompt 适用于所有已生成的业务全栈项目，结合实际前后端项目结构和代码，自动生成高质量、规范化的测试体系和测试文件。

---

## 🧪 业务相关补充建议

- 端到端集成测试：前端上传→后端分片→LLM 生成→报告拼接→前端渲染与下载
- mock 后端 LLM、PDF 分片、Prompt 渲染，前端 mock store、API
- 断言报告内容、元数据、下载文件名、进度条、错误提示等主流程
- 覆盖异常流程与边界场景
- 多 Prompt 版本切换与回退的集成测试
- 下载接口与前端解析需断言 Content-Disposition 兼容性与中文标题
- 日志、异常、进度反馈等全链路测试

通过以上最佳实践，全栈项目可实现高质量、可扩展的测试体系，支持开发过程中的快速回归与功能验证，大幅提升开发效率与代码可靠性。 