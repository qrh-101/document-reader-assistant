# 项目初始化 Prompt：DeepResearch FastAPI 前端服务

## 需求分析
为 "DeepResearch" 后端服务构建配套的前端应用，提供友好的用户界面用于上传PDF文档、输入研究问题，并展示生成的研究报告。

## 主要功能
- PDF文件上传功能
- 研究问题输入表单
- 与后端API通信，提交请求并获取研究报告
- 展示生成的Markdown格式研究报告
- 显示处理进度和状态信息

## 核心流程梳理
1. 用户在界面中选择PDF文件并输入研究问题
2. 前端验证输入内容并提交至后端 `/generate_report` 接口
3. 显示处理进度，等待后端响应
4. 接收后端返回的Markdown研究报告
5. 在界面上渲染并展示研究报告内容

## 技术栈
- Vue3 + Vite + Element Plus + TailwindCSS + Pinia + TypeScript

## 项目结构（推荐）
```
front/
├── src/
│   ├── pages/           # 页面组件
│   ├── components/      # 复用型UI组件
│   ├── api/             # API 封装
│   ├── stores/          # 状态管理
│   ├── types/           # TypeScript 类型声明
│   ├── utils/           # 工具函数
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

## 开发最佳实践
- 页面只负责布局和业务流转，具体UI和交互拆分为复用型组件。
- 组件 props/emit 明确，类型强校验，避免隐式依赖。
- 业务逻辑与视图分离，API、store、utils 不直接耦合到组件。
- API 请求统一封装在 src/api/ 下，便于维护和 mock。
- 全局状态管理用 Pinia，管理研究报告数据和处理状态。
- 工具函数统一放在 src/utils/ 下。
- 组件样式优先 TailwindCSS，局部细节可用 scoped CSS。
- 推荐 TypeScript，提升类型安全和开发体验。
- 统一 .gitignore，忽略 node_modules、dist、环境变量、日志等。

> ⚠️ 测试体系、mock、CI等请结合《frontend_test_best_practice_prompt.md》独立生成。
