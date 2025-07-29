# 项目初始化 Prompt：DeepResearch 全栈服务

## 业务背景与目标
本项目为 DeepResearch 智能文档研究助手的全栈实现，聚焦于 PDF 研究报告自动生成业务。目标是实现前后端协同，端到端支持 PDF 上传、研究问题输入、报告生成、进度反馈、报告渲染与下载等完整业务流程。

## 主要功能
- 前端：PDF 上传、问题输入、进度反馈、报告渲染与下载、列表与详情、错误提示、移动端适配
- 后端：PDF 解析分片、Prompt 渲染、LLM 调用、报告拼接、元数据管理、报告下载、Prompt 多版本管理、日志与异常处理
- 前后端接口契约与类型校验
- 端到端集成测试与自动化

## 核心业务流程
1. 用户上传 PDF 并输入研究问题（前端）
2. 前端调用后端 `/generate_report`，展示进度
3. 后端分片、渲染 Prompt、调用 LLM、拼接报告、保存元数据
4. 后端返回报告 ID，前端渲染报告内容
5. 前端支持报告下载（自动命名）、列表、详情、删除等
6. 支持多 Prompt 版本切换与管理

## 技术选型
- 后端：FastAPI + Pydantic + Loguru + python-dotenv + pytest
- 前端：Vue3 + Vite + Element Plus + TailwindCSS + Pinia + TypeScript

## 推荐项目结构
```
project-root/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── .env
│   ├── tests/
│   └── ...
├── frontend/
│   ├── src/
│   ├── public/
│   ├── .env
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.cjs
│   └── ...
└── README.md
```

## 业务相关最佳实践
- 前后端分层解耦，接口清晰，便于协作
- 类型安全，前后端接口类型强校验
- 多环境支持，.env 管理
- 友好日志，分级输出
- RESTful 接口，统一 code/msg/data 结构
- 全局异常处理，日志记录异常
- mock 与真实数据解耦，便于前端独立开发和接口联调
- 测试友好，tests 目录下分模块编写测试用例（具体见测试最佳实践）
- .gitignore 完善，忽略 node_modules、dist、venv、__pycache__、日志、环境变量、测试缓存等

> ⚠️ 测试体系、mock、CI 请结合《fullstack_test_best_practice_prompt.md》独立生成。
