# DeepResearch 前端

本项目为 DeepResearch 智能文档研究助手的前端，基于 Vue3 + TypeScript + Element Plus 构建，支持 PDF 上传、研究问题输入、进度反馈、报告渲染与下载、列表与详情、错误提示、移动端适配等。

## 功能特性
- 🎨 现代化UI设计，响应式布局
- 📄 拖拽上传PDF文件
- 🤖 实时进度跟踪
- 📝 Markdown报告渲染
- 📥 智能文件下载，自动使用报告标题命名
- 📱 移动端适配
- 🎯 TypeScript类型安全
- 📊 完整统计信息展示
- 🎯 智能内容过滤，避免重复信息
- 🧪 完整的测试体系

## 技术栈
- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript超集
- **Vite**: 极速的前端构建工具
- **Element Plus**: Vue 3组件库
- **TailwindCSS**: 原子化CSS框架
- **Pinia**: Vue状态管理
- **Vue Router**: 官方路由管理器
- **Vitest**: 单元测试框架
- **@testing-library/vue**: Vue组件测试库

## 项目结构
```
frontend/
├── src/
│   ├── components/          # 可复用组件
│   ├── pages/               # 页面组件
│   ├── api/                 # API接口
│   ├── stores/              # 状态管理
│   ├── types/               # 类型定义
│   ├── utils/               # 工具函数
│   ├── __tests__/           # 集成测试
│   ├── App.vue              # 根组件
│   ├── main.ts              # 应用入口
│   └── index.css            # 全局样式
├── public/                  # 静态资源
├── package.json             # 项目配置
├── README.md                # 前端说明
├── frontend_init_prompt.md  # 前端初始化/最佳实践 prompt
├── frontend_test_best_practice_prompt.md # 前端测试最佳实践
└── ...
```

## Prompt 驱动开发
- 项目初始化、最佳实践、测试体系 prompt 均在 frontend 目录下，适用于本项目的自动化生成和团队协作。
- 初始化见 `frontend_init_prompt.md`
- 测试体系见 `frontend_test_best_practice_prompt.md`

## 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 配置环境变量
```bash
cp env.example .env
# 编辑 .env 文件，配置API地址
```

### 3. 启动开发服务器
```bash
npm run dev
```

访问 http://localhost:3000 查看应用。

### 4. 构建生产版本
```bash
npm run build
```

构建产物将生成在 `dist` 目录中。

## 开发与测试
```bash
npm run test                # 运行所有测试
npm run lint                # 代码检查
npm run format              # 代码格式化
npx vue-tsc --noEmit        # 类型检查
```

## Docker 部署
```bash
docker build -t deepresearch-frontend .
docker run -p 3000:80 deepresearch-frontend
```

## 测试最佳实践
- 详见 `frontend_test_best_practice_prompt.md`