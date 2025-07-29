# DeepResearch 后端服务

本项目为 DeepResearch 智能文档研究助手的后端，基于 FastAPI，支持 PDF 解析、分片、Prompt 渲染、LLM 调用、Markdown 报告拼接、元数据管理、报告下载、提示词多版本管理等。

## 功能特性
- 📄 PDF文档解析与语义分片
- 🤖 大模型API集成（qwen-turbo）
- 📝 结构化Markdown报告生成
- 🔄 异步处理与进度跟踪
- 📁 报告文件管理
- 🔒 文件上传验证
- 📊 完整的日志系统
- 🧠 智能分片优化
- 📈 完整元数据统计
- 🧪 全面测试覆盖
- 🎯 多套提示词管理

## 技术栈
- **FastAPI**: 高性能Web框架
- **PyMuPDF**: PDF文档处理
- **阿里云百炼API**: 大模型API调用 (qwen-turbo)
- **Pydantic**: 数据验证
- **Loguru**: 日志管理
- **Uvicorn**: ASGI服务器
- **pytest**: 测试框架

## 项目结构
```
backend/
├── main.py                  # FastAPI应用入口
├── app/
│   ├── core/                # 配置、日志
│   ├── routers/             # API路由
│   ├── services/            # 业务逻辑
│   ├── schemas/             # 数据模型
│   ├── prompts/             # Prompt模板
│   └── utils/               # 工具函数
├── tests/                   # 后端测试
├── requirements.txt         # Python依赖
├── env.example              # 环境变量示例
├── run_tests.py             # 测试运行脚本
├── README.md                # 后端说明
├── backend_init_prompt.md   # 后端初始化/最佳实践 prompt
├── backend_test_best_practice_prompt.md # 后端测试最佳实践
└── ...
```

## Prompt 驱动开发
- 项目初始化、最佳实践、测试体系 prompt 均在 backend 目录下，适用于本项目的自动化生成和团队协作。
- 初始化见 `backend_init_prompt.md`
- 测试体系见 `backend_test_best_practice_prompt.md`

## 快速开始

### 1. 环境准备
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# 编辑 .env 文件，设置阿里云百炼API Key
```

### 2. 启动服务
```bash
python main.py --host 0.0.0.0 --port 8000
```

### 3. 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 典型API接口
- `POST /api/v1/generate_report`：生成报告
- `GET /api/v1/download_report/{report_id}`：下载报告（Content-Disposition 支持中文标题）
- `GET /api/v1/reports`：报告列表
- `GET /api/v1/reports/{report_id}`：报告详情
- `GET /api/v1/prompts/versions`：可用 Prompt 版本
- `GET /api/v1/prompts/info/{version}`：Prompt 版本详情
- `GET /api/v1/prompts/current`：当前 Prompt 信息

## 测试与开发
```bash
python run_tests.py         # 运行全部测试
python run_tests.py api     # 仅运行API相关测试
python -m pytest tests/ -v  # 直接用pytest运行
black app/                  # 代码格式化
isort app/                  # 导入排序
flake8 app/                 # 代码检查
```

## Docker 部署
```bash
cd backend
docker build -t deepresearch-backend .
docker run -p 8000:8000 deepresearch-backend
```

## 测试最佳实践
- 详见 `backend_test_best_practice_prompt.md`