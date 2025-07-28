# 通用前端测试最佳实践 Prompt

本 prompt 适用于所有已生成的业务前端项目（如 Vue3/Vite/TypeScript），结合实际项目结构和代码，自动生成高质量、规范化的测试体系和测试文件。

---

## 🧪 前端测试最佳实践

为保证前端项目的健壮性、可维护性和开发效率，建议同步建设自动化测试体系。具体建议如下：

### 1. 测试文件组织与目录结构
- **单元测试**：测试文件与被测组件/函数/Store 同级，命名为 `xxx.spec.ts(x)` 或 `xxx.test.ts(x)`，便于就近维护和查找。
- **集成测试/端到端测试**：集中放在 `src/__tests__/` 或 `e2e/` 目录下，关注业务流转和用户操作全流程。

### 2. 测试类型与用例设计
- 单元测试、组件测试、集成测试、端到端（E2E）测试分层设计。

### 3. Mock 与依赖隔离
- 使用 Vitest/Jest/Testing Library 的 mock 能力，隔离 API 请求、全局依赖、第三方库等。
- 推荐 MSW（Mock Service Worker）或 jest.mock/axios-mock-adapter 进行接口 mock。
- 对于全局 store，可用 mock store 或自定义测试 store。

### 4. 路径与环境兼容
- 测试环境建议与开发环境一致（如 Vite + Vitest），保证测试用例在本地、CI/CD 环境下均可直接运行。
- 配置 `jsdom` 作为测试环境，模拟浏览器 API。
- 保证 TypeScript 类型校验通过，测试代码同样遵循类型安全。

### 5. 测试脚本与运行
- `package.json` 已配置标准测试命令：
  - `npm run test`：运行所有测试
  - `npm run test:unit`：运行单元测试
  - `npm run test:watch`：监听模式
  - `npm run test:coverage`：生成覆盖率报告
  - `npm run test:e2e`：运行端到端测试（如集成 Cypress）

### 6. CI/CD 集成建议
- 在 CI 流程中集成自动化测试，确保每次提交均通过全部测试。
- 集成覆盖率工具（如 `vitest --coverage`），持续提升代码质量。
- E2E 测试可在 PR 合并前自动运行，保障主流程稳定。

### 7. 典型测试文件建议
- `*.spec.ts(x)` / `*.test.ts(x)`：单元/组件测试（与业务代码同级）
- `AppFlow.spec.ts` 等：集成测试（集中存放）
- `e2e/` 目录下存放端到端测试脚本

### 8. 进阶最佳实践补充
- 组件内部所有依赖对象字段访问（如 `metadata.processing_time`）应加可选链（`?.`）或默认值（`?? 0`），保证健壮性，防止测试或运行时因 mock 不全报错。
- 前端测试 mock 只需保证主流程（如 createReport、fetchReportDetail、currentReport），无需模拟完整响应式链条或所有字段细节。
- 集成测试断言只关注页面主内容（如“测试报告”“内容”），不必断言所有元数据细节，避免陷入 mock 死循环。
- 推荐使用 `await waitFor` 等异步断言，确保页面渲染完成后再断言内容。

通过以上最佳实践，前端项目可实现高质量、可扩展的测试体系，支持开发过程中的快速回归与功能验证，大幅提升开发效率与代码可靠性。 