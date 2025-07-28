# DeepResearch 后端服务

> 本项目采用分层 prompt 驱动式开发，推荐结合 `backend_init_prompt.md`、`backend_best_practice.md`、`backend_test_best_practice_prompt.md` 快速生成高质量代码和测试体系。详见根目录及 `init_prompts/` 下相关 prompt 文件。

智能文档研究助手的后端API服务，提供PDF文档解析、大模型调用和报告生成功能。

## 功能特性

- 📄 PDF文档解析与语义分片
- 🤖 阿里云百炼API集成 (qwen-turbo模型)
- 📝 结构化Markdown报告生成
- 🔄 异步处理与进度跟踪
- 📁 报告文件管理
- 🔒 文件上传验证
- 📊 完整的日志系统

## 技术栈

- **FastAPI**: 高性能Web框架
- **PyMuPDF**: PDF文档处理
- **阿里云百炼API**: 大模型API调用 (qwen-turbo)
- **Pydantic**: 数据验证
- **Loguru**: 日志管理
- **Uvicorn**: ASGI服务器

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量示例文件并配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，设置必要的配置项：

```env
# 百炼API配置
LLM_API_KEY=your_dashscope_api_key_here
MODEL_NAME=qwen-turbo
API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
MAX_TOKENS_PER_CHUNK=500
```

### 3. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. 访问API文档

启动服务后，访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API接口

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

## 项目结构

```
backend/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── core/
│   │   ├── config.py        # 配置管理
│   │   └── logger.py        # 日志配置
│   ├── routers/
│   │   └── research.py      # 研究接口路由
│   ├── schemas/
│   │   └── report_schema.py # 数据模型
│   ├── services/
│   │   ├── pdf_service.py   # PDF处理服务
│   │   ├── prompt_service.py # Prompt构建服务
│   │   └── report_service.py # 报告生成服务
│   ├── prompts/
│   │   └── system_prompt.md # 系统Prompt模板
│   └── utils/
│       └── file_io.py       # 文件IO工具
├── reports/                 # 生成的报告存储目录
├── uploads/                 # 上传文件临时目录
├── logs/                    # 日志文件目录
├── requirements.txt         # Python依赖
├── env.example             # 环境变量示例
├── README.md               # 项目说明
└── init_prompts/          # 项目初始化、开发、测试 prompt 文件
```

> 根目录及 `../init_prompts/` 目录下包含通用的后端项目初始化、开发最佳实践、测试最佳实践 prompt，可用于任意新项目的高效生成和规范化开发。

## 推荐 Prompt 使用流程

1. 用 `backend_init_prompt.md` 生成项目结构和基础代码。
2. 按 `backend_best_practice.md` 规范持续开发和优化。
3. 项目代码生成后，用 `backend_test_best_practice_prompt.md` 自动生成测试体系。
4. 持续集成、自动化测试，保障项目高质量交付。

> 详细用法见根目录 `init_prompts/backend_prompt_usage_guide.md`。

## 配置说明

### 大模型API配置

- `LLM_API_KEY`: 百炼API密钥
- `MODEL_NAME`: 使用的模型名称（默认qwen-turbo）
- `API_BASE`: API基础URL
- `MODEL_CONTEXT_LENGTH`: 模型上下文长度（默认1000000）
- `MAX_TOKENS_PER_CHUNK`: 每个片段的最大token数
- `TEMPERATURE`: 生成温度参数

### PDF处理配置

- `CHUNK_STRATEGY`: 分片策略（semantic/fixed）
- `MAX_CHUNK_SIZE`: 最大分片大小
- `OVERLAP_SIZE`: 分片重叠大小

### 文件配置

- `REPORTS_DIR`: 报告存储目录
- `UPLOAD_DIR`: 上传文件目录
- `MAX_FILE_SIZE`: 最大文件大小（字节）

## 测试结构

- 后端测试最佳实践详见：`../backend_test_best_practice_prompt.md`

## 开发指南

### 添加新的API接口

1. 在 `app/routers/` 目录下创建新的路由文件
2. 在 `app/schemas/` 目录下定义数据模型
3. 在 `app/services/` 目录下实现业务逻辑
4. 在 `app/main.py` 中注册路由

### 运行测试

```bash
# 运行所有测试
python run_tests.py

# 运行特定类型的测试
python run_tests.py config    # 配置验证测试
python run_tests.py api       # API测试（需要真实API密钥）
python run_tests.py chunking  # 智能分片测试
python run_tests.py unit      # 单元测试

# 运行特定测试文件
python run_tests.py pdf_service
python run_tests.py report_service

# 使用pytest直接运行
pytest tests/ -v
pytest tests/test_pdf_service.py -v
pytest tests/test_report_service.py -v

# 生成测试覆盖率报告
pytest --cov=app tests/
```

### 代码规范

- 使用Black进行代码格式化
- 使用isort进行导入排序
- 使用flake8进行代码检查

```bash
# 格式化代码
black app/

# 排序导入
isort app/

# 代码检查
flake8 app/
```

## 部署

### Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 生产环境配置

1. 设置生产环境变量
2. 配置反向代理（Nginx）
3. 设置SSL证书
4. 配置日志轮转
5. 设置监控和告警

## 故障排除

### 常见问题

1. **PDF解析失败**: 检查PDF文件是否损坏或加密
2. **API调用失败**: 验证百炼API密钥和网络连接
3. **文件上传失败**: 检查文件大小和类型限制
4. **内存不足**: 调整分片大小和并发数

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log
```

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License 