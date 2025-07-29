# 项目初始化 Prompt：DeepResearch 智能文档研究助手前端

## 业务背景与目标
本项目为 DeepResearch 智能文档研究助手的前端，聚焦于 PDF 研究报告自动生成业务。目标是为用户提供友好的界面，支持上传 PDF、输入研究问题、实时查看进度、渲染和下载结构化 Markdown 报告，并具备高可用、高可维护、优质用户体验。

## 主要功能
- PDF 文件拖拽上传与校验
- 研究问题输入表单
- 与后端 API 通信，提交生成请求并获取报告
- 实时进度反馈与状态提示
- Markdown 格式研究报告渲染与高亮
- 智能文件下载（自动使用报告标题命名）
- 报告列表与详情页
- 错误处理与用户友好提示
- 移动端适配与响应式布局

## 核心业务流程
1. 用户在界面选择/拖拽 PDF 文件并输入研究问题
2. 前端校验输入内容，调用后端 `/generate_report` 接口
3. 展示处理进度，轮询或等待后端响应
4. 接收后端返回的 Markdown 研究报告及元数据
5. 在界面渲染报告内容，支持下载（文件名自动为报告标题）
6. 支持报告列表、详情、删除等操作

## 技术栈
- Vue3 + Vite + Element Plus + TailwindCSS + Pinia + TypeScript

## 推荐项目结构
```
frontend/
├── src/
│   ├── pages/           # 页面组件（如 HomePage、ReportPage）
│   ├── components/      # 复用型UI组件（如 UploadForm、ReportViewer、ProgressBar）
│   ├── api/             # API 封装（如 research.ts）
│   ├── stores/          # Pinia 状态管理（如 reportStore.ts）
│   ├── types/           # TypeScript 类型声明
│   ├── utils/           # 工具函数（如 request.ts、文件名处理等）
│   ├── App.vue          # 路由壳组件
│   ├── main.ts          # 入口文件
│   └── index.css        # 全局样式
├── public/
├── .env                 # 环境变量
├── package.json
├── tailwind.config.js
├── postcss.config.cjs
└── ...
```

## 业务最佳实践
- 页面只负责布局和业务流转，具体 UI 和交互拆分为复用型组件
- 组件 props/emit 明确，类型强校验，避免隐式依赖
- 业务逻辑与视图分离，API、store、utils 不直接耦合到组件
- API 请求统一封装在 src/api/ 下，便于维护和 mock
- 全局状态管理用 Pinia，管理报告数据和处理状态
- 工具函数统一放在 src/utils/ 下
- 组件样式优先 TailwindCSS，局部细节可用 scoped CSS
- 推荐 TypeScript，提升类型安全和开发体验
- 统一 .gitignore，忽略 node_modules、dist、环境变量、日志等

## 业务相关测试建议
- 结合 `frontend_test_best_practice_prompt.md`，补充：
  - 如何 mock 后端 LLM 响应、报告内容
  - 如何断言报告渲染、下载文件名、进度条、错误提示等主流程
  - 如何覆盖异常流程（如超时、文件过大、API 错误等）
  - 典型集成测试：上传→生成→渲染→下载全链路

> ⚠️ 测试体系、mock、CI 请结合《frontend_test_best_practice_prompt.md》独立生成。
