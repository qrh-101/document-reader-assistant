# DeepResearch - 智能文档研究助手

基于AI技术的智能文档研究助手，能够分析PDF文档并生成专业的结构化研究报告。

## 🚀 项目特性

- 📄 智能PDF解析：支持多格式PDF文档，自动提取文本内容
- 🤖 AI智能分析：集成大语言模型，深度理解文档内容
- 📝 结构化报告生成：输出标准Markdown格式的专业研究报告
- 🎨 现代化UI：响应式设计，支持桌面端和移动端
- ⚡ 高性能异步处理：后端异步、前端实时进度反馈
- 🔒 文件上传验证与错误处理：安全可靠
- 📊 完整统计与技术参数展示：报告元数据、分片、模型参数等
- 🧪 完善的自动化测试体系：前后端/全栈测试最佳实践

## 🏗️ 项目结构

```
document-reader-assistant/
├── backend/                 # 后端服务
│   ├── main.py              # FastAPI应用入口
│   ├── app/                 # 后端核心代码
│   ├── tests/               # 后端测试
│   └── README.md            # 后端说明
├── frontend/                # 前端应用
│   ├── src/                 # 前端核心代码
│   ├── __tests__/           # 前端集成测试
│   └── README.md            # 前端说明
├── backend_init_prompt.md   # 后端初始化/最佳实践 prompt
├── frontend_init_prompt.md  # 前端初始化/最佳实践 prompt
├── fullstack_init_prompt.md # 全栈初始化/最佳实践 prompt
├── backend_test_best_practice_prompt.md   # 后端测试最佳实践
├── frontend_test_best_practice_prompt.md  # 前端测试最佳实践
├── fullstack_test_best_practice_prompt.md # 全栈测试最佳实践
└── README.md                # 项目说明
```

## 🧑‍💻 Prompt 驱动开发流程

本项目采用分层 prompt 驱动开发，所有初始化、最佳实践、测试体系 prompt 均在根目录下，适用于本项目的自动化生成和团队协作。

- 项目初始化：见 `*_init_prompt.md`
- 测试体系生成：见 `*_test_best_practice_prompt.md`

## 🧪 测试最佳实践

- 前端测试最佳实践详见：`frontend_test_best_practice_prompt.md`
- 后端测试最佳实践详见：`backend_test_best_practice_prompt.md`
- 全栈测试最佳实践详见：`fullstack_test_best_practice_prompt.md`

## 🛠️ 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- 阿里云百炼API Key

### 1. 解压项目包
请将下载的 zip 包解压到任意目录，例如：
```
D:\projects\document-reader-assistant
```
进入项目根目录：
```
cd D:\projects\document-reader-assistant
```

### 2. 后端设置
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# 编辑 .env 文件，设置阿里云百炼API Key
python main.py --host 0.0.0.0 --port 8000
```

### 3. 前端设置
```bash
cd frontend
npm install
cp env.example .env
# 编辑 .env 文件，配置API地址
npm run dev
```

### 4. 访问应用
- 前端应用: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📝 主要功能与业务流程

1. 用户上传PDF并输入研究问题
2. 前端校验后调用后端 `/generate_report` 接口
3. 后端分片、渲染Prompt、调用大模型、拼接报告、保存元数据
4. 前端实时展示进度，渲染报告内容，支持下载（文件名自动为报告标题）
5. 支持报告列表、详情、删除、Prompt多版本切换

## 🧩 典型API接口
- `POST /api/v1/generate_report`：生成报告
- `GET /api/v1/download_report/{report_id}`：下载报告（Content-Disposition 支持中文标题）
- `GET /api/v1/reports`：报告列表
- `GET /api/v1/reports/{report_id}`：报告详情
- `GET /api/v1/prompts/versions`：可用 Prompt 版本
- `GET /api/v1/prompts/info/{version}`：Prompt 版本详情
- `GET /api/v1/prompts/current`：当前 Prompt 信息

## 🧪 开发与测试

### 后端开发
```bash
cd backend
python run_tests.py         # 运行全部测试
python run_tests.py api     # 仅运行API相关测试
python -m pytest tests/ -v  # 直接用pytest运行
black app/                  # 代码格式化
isort app/                  # 导入排序
flake8 app/                 # 代码检查
```

### 前端开发
```bash
cd frontend
npm run test                # 运行所有测试
npm run lint                # 代码检查
npm run format              # 代码格式化
npx vue-tsc --noEmit        # 类型检查
```

## 🐳 Docker 部署

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

## 📝 其它说明
- 详细后端、前端开发说明见各自子目录下 README.md。