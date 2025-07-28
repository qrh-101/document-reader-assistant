# 项目初始化 Prompt：DeepResearch 全栈服务

## 需求分析
{{ 需求分析 }}

## 主要功能
{{ 主要功能 }}

## 核心流程梳理
{{ 核心流程梳理 }}

## 技术选型
- 后端：FastAPI + Pydantic + Loguru + python-dotenv + pytest
- 前端：Vue3 + Vite + Element Plus + TailwindCSS + Pinia + TypeScript

## 项目结构（推荐）
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

## 开发最佳实践
- 前后端分层解耦，接口清晰，便于协作。
- 类型安全，前后端接口类型强校验。
- 多环境支持，.env 管理。
- 友好日志，分级输出。
- RESTful接口，统一 code/msg/data 结构。
- 全局异常处理，日志记录异常。
- mock与真实数据解耦，便于前端独立开发和接口联调。
- 测试友好，tests 目录下分模块编写测试用例（具体见测试最佳实践）。
- .gitignore 完善，忽略 node_modules、dist、venv、__pycache__、日志、环境变量、测试缓存等。

> ⚠️ 测试体系、mock、CI等请结合《fullstack_test_best_practice_prompt.md》独立生成。
