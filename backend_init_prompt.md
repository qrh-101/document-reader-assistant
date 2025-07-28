# 🎯 项目初始化 Prompt：DeepResearch FastAPI 后端服务

## 🧩 项目背景
本项目为 “DeepResearch” 应用提供后端支撑服务，聚焦于接收用户问题与PDF文档、调度Prompt模板、组织调用大模型接口、分片处理文档内容并最终合成结构化Markdown研究报告。

## 💡 核心能力
- 接收用户上传的PDF和问题，完成PDF分片解析；
- 按照系统Prompt模板调度大模型生成内容；
- 拼接Markdown内容为完整报告；
- 提供RESTful API供前端调用；
- 支持配置llm生成的每个片段输出字数（默认500字）；
- 支持多Prompt模板灵活扩展。

---

## 🔧 技术选型
- **FastAPI**：高性能 Web 框架；
- **Pydantic**：数据模型与校验；
- **Loguru**：日志系统；
- **python-dotenv**：环境变量配置；
- **pytest**：测试框架；
- **openai / deep-api-sdk**：大模型 API 调用；
- **PyMuPDF / pdfplumber**：PDF 内容提取与分片。

---

## 📂 项目结构（推荐）

```text
backend/
├── app/
│ ├── main.py # FastAPI 入口，注册中间件、事件、路由
│ ├── core/
│ │ ├── config.py # 配置管理（含 max_tokens_per_chunk 等）
│ │ └── logger.py # 日志配置
│ ├── routers/
│ │ └── research.py # 研究接口路由（如 /generate_report）
│ ├── models/
│ │ └── prompt_model.py # 系统Prompt模型与解析
│ ├── schemas/
│ │ └── report_schema.py # 请求与响应结构定义
│ ├── services/
│ │ ├── prompt_service.py # Prompt构建与参数渲染逻辑
│ │ ├── pdf_service.py # PDF解析与分片
│ │ └── report_service.py # 调用LLM生成+拼接报告逻辑
│ ├── prompts/
│ │ └── system_prompt.md # 主系统Prompt模板（可多版本扩展）
│ └── utils/
│ └── file_io.py # 文件上传、格式转换、临时缓存工具
├── .env # 环境变量（API key、环境配置等）
├── requirements.txt
├── tests/ # 单元测试
│ └── test_research.py
└── README.md
```

---

## 🧭 核心流程

### 1. 用户上传PDF并输入研究问题
- 请求格式：multipart/form-data
- 字段：`file`（PDF），`question`（string）
- 系统接收并验证用户输入的合法性

### 2. 后端处理流程
- **Step 1：PDF解析与语义分片**
  - 使用 PyMuPDF/pdfplumber 解析PDF文档内容
  - 根据配置的分片策略（语义完整性优先）将文档切分为多个片段
  - 保证每个片段具有相对完整的语义信息

- **Step 2：Prompt模板渲染**
  - 加载系统Prompt模板（位于 `app/prompts/system_prompt.md`）
  - 将用户问题、PDF片段内容填充到Prompt模板中
  - 准备大模型调用参数

- **Step 3：分段调用大模型**
  - 依次对每个PDF片段调用大模型API
  - 控制每个片段生成内容的token上限（默认500，可配置）
  - 收集各片段生成的Markdown格式内容

- **Step 4：报告整合与返回**
  - 按顺序拼接所有片段生成的内容
  - 构建完整的结构化Markdown研究报告
  - 返回包含完整报告和元数据的响应结果

---

## 📌 示例接口定义

### POST `/generate_report`
```json
Request:
{
  "question": "请分析数字医疗在老龄化社会的影响。",
  "file": "example.pdf"
}

Response:
{
  "code": 200,
  "msg": "success",
  "data": {
    "markdown_report": "# 数字医疗与老龄化社会\n\n## 引言\n\n在当前老龄化趋势中，数字医疗...\n\n## 主要影响\n\n### 提高医疗服务可达性\n\n随着人口老龄化的加剧...\n\n### 优化医疗资源配置\n\n数字医疗技术能够...",
    "report_metadata": {
      "total_chunks": 6,
      "processed_chunks": 6,
      "token_per_chunk": 500
    }
  }
}
```

### 🔄 接口处理流程说明
1.PDF分片处理
- 将上传的PDF文档按语义段落切分为多个片段
- 每个片段独立处理，确保内容完整性和上下文连贯性
2.分段调用大模型
- 对每个PDF片段，结合用户问题和系统Prompt模板生成请求
- 依次调用大模型API获取Markdown格式的报告片段
- 支持配置每个片段的最大token数（默认500）
3.报告整合
- 将所有生成的Markdown片段按逻辑顺序拼接
- 生成完整的结构化研究报告文档
4.结果返回
- 返回完整的Markdown格式研究报告
- 包含处理元数据信息（处理的片段数、token配置等）

---

## ⚙️ 核心配置项（.env 示例）

```env
OPENAI_API_KEY=sk-xxx
MAX_TOKENS_PER_CHUNK=500
MODEL_NAME=gpt-4
CHUNK_STRATEGY=semantic
```

---

## 🧪 单元测试建议
- test_prompt_service.py：验证Prompt渲染是否正确；
- test_pdf_service.py：验证PDF分片效果；
- test_report_service.py：测试拼接流程与模型调用模拟；
- test_generate_report_api.py：接口全流程测试。

## ✅ 推荐实践
- 每种Prompt使用独立markdown模板存放在 app/prompts/；
- 各类业务逻辑封装在 services 层，避免routers臃肿；
- 支持mock调用与真实LLM调用解耦；
- 所有请求响应结构统一采用 code/msg/data 三段式 schema；
- 日志支持 request_id，方便链路追踪；
- 模板中每段输出支持最多token限制，默认500，可配置。