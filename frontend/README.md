# DeepResearch 前端

> 本项目采用分层 prompt 驱动式开发，推荐结合 `frontend_init_prompt.md`、`frontend_best_practice.md`、`frontend_test_best_practice_prompt.md` 快速生成高质量代码和测试体系。详见根目录及 `init_prompts/` 下相关 prompt 文件。

智能文档研究助手的前端应用，基于Vue3 + TypeScript + Element Plus构建。

## 功能特性

- 🎨 现代化UI设计，响应式布局
- 📄 拖拽上传PDF文件
- 🤖 实时进度跟踪
- 📝 Markdown报告渲染
- 📱 移动端适配
- 🎯 TypeScript类型安全

## 技术栈

- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript超集
- **Vite**: 极速的前端构建工具
- **Element Plus**: Vue 3组件库
- **TailwindCSS**: 原子化CSS框架
- **Pinia**: Vue状态管理
- **Vue Router**: 官方路由管理器

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

复制环境变量示例文件：

```bash
cp env.example .env
```

编辑 `.env` 文件，配置API地址：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
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

## 项目结构

```
frontend/
├── src/
│   ├── components/          # 可复用组件
│   │   ├── Header.vue      # 页面头部
│   │   ├── UploadForm.vue  # 文件上传表单
│   │   ├── ReportViewer.vue # 报告查看器
│   │   └── ProgressBar.vue # 进度条组件
│   ├── pages/              # 页面组件
│   │   ├── HomePage.vue    # 首页
│   │   ├── ReportPage.vue  # 报告页面
│   │   └── NotFoundPage.vue # 404页面
│   ├── api/                # API接口
│   │   └── research.ts     # 研究相关API
│   ├── stores/             # 状态管理
│   │   └── reportStore.ts  # 报告状态
│   ├── types/              # 类型定义
│   │   ├── api.d.ts        # API类型
│   │   └── report.d.ts     # 报告类型
│   ├── utils/              # 工具函数
│   │   └── request.ts      # HTTP请求封装
│   ├── router/             # 路由配置
│   │   └── index.ts        # 路由定义
│   ├── App.vue             # 根组件
│   ├── main.ts             # 应用入口
│   └── index.css           # 全局样式
├── public/                 # 静态资源
├── package.json            # 项目配置
├── vite.config.ts          # Vite配置
├── tailwind.config.js      # TailwindCSS配置
├── tsconfig.json           # TypeScript配置
├── README.md               # 项目说明
└── init_prompts/          # 项目初始化、开发、测试最佳实践 prompt 文件
```

> 根目录及 `../init_prompts/` 目录下包含通用的前端项目初始化、开发最佳实践、测试最佳实践 prompt，可用于任意新项目的高效生成和规范化开发。

## 推荐 Prompt 使用流程

1. 用 `frontend_init_prompt.md` 生成项目结构和基础代码。
2. 按 `frontend_best_practice.md` 规范持续开发和优化。
3. 项目代码生成后，用 `frontend_test_best_practice_prompt.md` 自动生成测试体系。
4. 持续集成、自动化测试，保障项目高质量交付。

> 详细用法见根目录 `frontend_prompt_usage_guide.md`。

## 开发指南

### 组件开发

- 使用Composition API编写组件
- 使用TypeScript定义props和emits类型
- 遵循Vue 3最佳实践

```vue
<script setup lang="ts">
interface Props {
  title: string
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  submit: [value: string]
}>()
</script>
```

### 状态管理

使用Pinia进行状态管理：

```typescript
import { defineStore } from 'pinia'

export const useReportStore = defineStore('report', () => {
  const reports = ref<ReportInfo[]>([])
  
  const createReport = async (file: File, question: string) => {
    // 业务逻辑
  }
  
  return {
    reports,
    createReport
  }
})
```

### API调用

使用封装的request工具：

```typescript
import { generateReport } from '@/api/research'

const result = await generateReport(file, question)
```

### 样式开发

- 优先使用TailwindCSS类名
- 复杂样式使用scoped CSS
- 遵循设计系统规范

## 代码规范

### ESLint配置

项目使用ESLint进行代码检查：

```bash
npm run lint
```

### Prettier格式化

使用Prettier进行代码格式化：

```bash
npm run format
```

### TypeScript检查

```bash
npx vue-tsc --noEmit
```

## 部署

### 开发环境

```bash
npm run dev
```

### 生产环境

```bash
npm run build
npm run preview
```

### Docker部署

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License 

## 🧪 测试最佳实践

- 前端测试最佳实践详见：`../frontend_test_best_practice_prompt.md` 