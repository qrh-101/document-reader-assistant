# 🎯 项目初始化 Prompt：DeepResearch FastAPI 后端服务

## 🧩 业务背景与目标
本项目为 DeepResearch 智能文档研究助手的后端，聚焦于 PDF 研究报告自动生成业务。目标是支持 PDF 解析、分片、Prompt 渲染、LLM 调用、Markdown 报告拼接、元数据管理、报告下载、提示词多版本管理等核心能力，提供高可用、高可维护的 API 服务。

## 💡 核心能力
- 接收用户上传的 PDF 和研究问题，完成 PDF 分片解析
- 按照系统 Prompt 模板渲染，调用大模型生成内容
- 拼接 Markdown 内容为完整报告，保存元数据
- 提供 RESTful API 供前端调用
- 支持多 Prompt 模板灵活扩展，支持版本切换
- 支持每个片段输出最大 token 数（默认500）
- 支持报告下载（Content-Disposition 支持中文标题）
- 完整日志、异常处理、进度反馈

---

## 🛠 技术选型
- **FastAPI**：高性能 Web 框架
- **Pydantic**：数据模型与校验
- **Loguru**：日志系统
- **python-dotenv**：环境变量配置
- **pytest**：测试框架
- **openai / deep-api-sdk**：大模型 API 调用
- **PyMuPDF / pdfplumber**：PDF 内容提取与分片

---

## 📂 推荐项目结构
```
backend/
├── app/
│   ├── main.py                # FastAPI 入口
│   ├── core/                  # 配置、日志
│   ├── routers/               # 研究接口路由（如 /generate_report）
│   ├── models/                # Prompt 模型与解析
│   ├── schemas/               # 请求与响应结构定义
│   ├── services/              # Prompt 构建、PDF 解析、报告生成等
│   ├── prompts/               # 主系统 Prompt 模板（多版本扩展）
│   └── utils/                 # 文件上传、格式转换、临时缓存等
├── .env                       # 环境变量（API key、Prompt 版本等）
├── requirements.txt
├── tests/                     # 单元测试
└── README.md
```

---

## 🧬 核心业务流程
1. 用户上传 PDF 并输入研究问题（multipart/form-data，字段：file、question）
2. 系统接收并校验用户输入的合法性
3. PDF 解析与语义分片（PyMuPDF/pdfplumber，语义完整优先）
4. 加载系统 Prompt 模板（支持多版本，位于 app/prompts/）
5. 将用户问题、PDF 片段内容填充到 Prompt 模板，准备大模型参数
6. 依次对每个 PDF 片段调用大模型 API，控制每片段最大 token 数
7. 收集各片段生成的 Markdown 格式内容
8. 按顺序拼接所有片段内容，构建完整结构化 Markdown 研究报告
9. 保存报告及元数据，返回报告 ID
10. 支持报告下载（Content-Disposition 支持中文标题，前端可自动命名）
11. 支持报告详情、列表、删除、Prompt 版本管理等接口

---

## 🧩 典型接口定义
- `POST /generate_report`：生成报告
- `GET /download_report/{report_id}`：下载报告（Content-Disposition 支持中文标题）
- `GET /reports`：报告列表
- `GET /reports/{report_id}`：报告详情
- `GET /prompts/versions`：可用 Prompt 版本
- `GET /prompts/info/{version}`：Prompt 版本详情
- `GET /prompts/current`：当前 Prompt 信息

---

## 🧪 业务相关测试建议
- 结合 `backend_test_best_practice_prompt.md`，补充：
  - 如何 mock LLM 响应、PDF 分片、Prompt 渲染
  - 如何断言报告内容、元数据、下载文件名、接口响应等
  - 如何覆盖异常流程（如分片失败、LLM 超时、下载编码等）
  - 典型集成测试：上传→分片→生成→拼接→下载全链路

---

## ✅ 推荐实践
- 每种 Prompt 使用独立 markdown 模板，存放在 app/prompts/
- 各类业务逻辑封装在 services 层，避免 routers 臃肿
- 支持 mock 调用与真实 LLM 调用解耦
- 所有请求响应结构统一采用 code/msg/data 三段式 schema
- 日志支持 request_id，便于链路追踪
- 模板中每段输出支持最大 token 限制，默认500，可配置

> ⚠️ 测试体系、mock、CI 请结合《backend_test_best_practice_prompt.md》独立生成。