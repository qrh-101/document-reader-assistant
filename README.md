# DeepResearch - 智能文档研究助手

基于AI技术的智能文档研究助手，能够分析PDF文档并生成专业的结构化研究报告。

## 🚀 项目特性

- 📄 **智能PDF解析**: 支持各种格式的PDF文档，自动提取文本内容
- 🤖 **AI智能分析**: 基于GPT-4大语言模型，深度理解文档内容
- 📝 **结构化报告**: 生成标准Markdown格式的专业研究报告
- 🎨 **现代化UI**: 响应式设计，支持桌面端和移动端
- ⚡ **高性能**: 异步处理，实时进度跟踪
- 🔒 **安全可靠**: 文件上传验证，错误处理机制

## 🏗️ 技术架构

### 后端技术栈
- **FastAPI**: 高性能Python Web框架
- **PyMuPDF**: PDF文档处理库
- **OpenAI**: 大语言模型API
- **Pydantic**: 数据验证和序列化
- **Loguru**: 日志管理
- **Uvicorn**: ASGI服务器

### 前端技术栈
- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript超集
- **Element Plus**: Vue 3组件库
- **TailwindCSS**: 原子化CSS框架
- **Pinia**: Vue状态管理
- **Vite**: 极速前端构建工具

## 📦 项目结构

```
document-reader-assistant/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI应用入口
│   │   ├── core/           # 核心配置
│   │   ├── routers/        # API路由
│   │   ├── services/       # 业务逻辑
│   │   ├── schemas/        # 数据模型
│   │   ├── prompts/        # Prompt模板
│   │   └── utils/          # 工具函数
│   ├── reports/            # 生成的报告存储
│   ├── requirements.txt    # Python依赖
│   └── README.md          # 后端说明
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   ├── pages/         # 页面组件
│   │   ├── api/           # API接口
│   │   ├── stores/        # 状态管理
│   │   ├── types/         # 类型定义
│   │   └── utils/         # 工具函数
│   ├── package.json       # Node.js依赖
│   └── README.md         # 前端说明
├── init_prompts/            # 通用项目初始化/最佳实践/测试最佳实践 prompt
│   ├── backend_init_prompt.md
│   ├── backend_best_practice.md
│   ├── backend_test_best_practice_prompt.md
│   ├── frontend_init_prompt.md
│   ├── frontend_best_practice.md
│   ├── frontend_test_best_practice_prompt.md
│   ├── fullstack_init_prompt.md
│   ├── fullstack_test_best_practice_prompt.md
│   └── ...
└── README.md             # 项目说明
```

> **init_prompts/** 目录下包含通用的项目初始化、开发最佳实践、测试最佳实践 prompt，可用于任意新项目的高效生成和规范化开发。

## 🧑‍💻 Prompt驱动式开发流程

本项目采用分层 prompt 驱动式开发，推荐如下高效协作流程：

1. **项目初始化**：
   - 选择对应的 `*_init_prompt.md`，根据业务需求自动生成分层清晰、结构合理的项目骨架和基础代码。
2. **开发规范落地**：
   - 参考 `*_best_practice.md`，在开发过程中持续对照和优化代码风格、架构、命名、文档、协作等。
3. **自动化测试体系生成**：
   - 使用 `*_test_best_practice_prompt.md`，结合实际项目结构和代码，自动生成高质量、全覆盖的测试文件。
4. **持续集成与交付**：
   - 持续集成、自动化测试，保障项目高质量交付。

> 具体前端/后端/全栈 prompt 使用方法详见 `init_prompts/` 下各自的 `*_prompt_usage_guide.md`。

## 🧪 测试最佳实践

- 前端测试最佳实践详见：`frontend_test_best_practice_prompt.md`
- 后端测试最佳实践详见：`backend_test_best_practice_prompt.md`
- 全栈测试最佳实践详见：`fullstack_test_best_practice_prompt.md`

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- OpenAI API Key

### 1. 克隆项目

```bash
git clone https://github.com/your-username/document-reader-assistant.git
cd document-reader-assistant
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，设置 OpenAI API Key

# 启动后端服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp env.example .env

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📖 使用指南

### 1. 上传文档
- 点击或拖拽PDF文件到上传区域
- 支持最大50MB的PDF文件

### 2. 输入问题
- 描述您的研究问题
- 问题越具体，生成的报告越精准

### 3. 生成报告
- 点击"开始生成报告"按钮
- 等待AI处理完成
- 查看生成的专业报告

### 4. 下载报告
- 支持下载Markdown格式报告
- 支持打印功能
- 支持分享和导出

## 🔧 配置说明

### 后端配置

编辑 `backend/.env` 文件：

```env
# 大模型API配置
LLM_API_KEY=your_dashscope_api_key_here
MODEL_NAME=qwen-turbo
API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_CONTEXT_LENGTH=1000000
MAX_TOKENS_PER_CHUNK=500
TEMPERATURE=0.7

# PDF处理配置
CHUNK_STRATEGY=semantic
MAX_CHUNK_SIZE=2000
OVERLAP_SIZE=200

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

### 前端配置

编辑 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=DeepResearch
```

## 🧪 开发指南

### 后端开发

```bash
cd backend

# 运行测试
pytest

# 代码格式化
black app/
isort app/

# 代码检查
flake8 app/
```

### 前端开发

```bash
cd frontend

# 代码检查
npm run lint

# 代码格式化
npm run format

# 类型检查
npx vue-tsc --noEmit
```

## 🐳 Docker部署

### 后端Docker

```bash
cd backend
docker build -t deepresearch-backend .
docker run -p 8000:8000 deepresearch-backend
```

### 前端Docker

```bash
cd frontend
docker build -t deepresearch-frontend .
docker run -p 3000:80 deepresearch-frontend
```

### Docker Compose

```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - LLM_API_KEY=${LLM_API_KEY}
    volumes:
      - ./backend/reports:/app/reports

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

## 📊 API接口

### 生成报告
```http
POST /api/v1/generate_report
Content-Type: multipart/form-data

file: PDF文件
question: 研究问题
```

### 下载报告
```http
GET /api/v1/download_report/{report_id}
```

### 获取报告列表
```http
GET /api/v1/reports
```

### 获取报告详情
```http
GET /api/v1/reports/{report_id}
```