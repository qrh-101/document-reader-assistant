from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import argparse
import time
import uuid
from contextlib import asynccontextmanager
from loguru import logger

from app.routers import research
from app.core.config import settings

# 默认值
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# 命令行参数解析
parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, default=None, help="环境变量文件名，如 .env 或 .env.prod")
parser.add_argument("--host", type=str, default=None, help="服务主机地址")
parser.add_argument("--port", type=int, default=None, help="服务端口")
args, _ = parser.parse_known_args()

# 加载环境变量文件
if args.env:
    from dotenv import load_dotenv
    load_dotenv(args.env)

host = args.host or os.getenv("HOST") or DEFAULT_HOST
port = args.port or int(os.getenv("PORT") or DEFAULT_PORT)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("DeepResearch API 启动完成！")
    logger.info(f"后端接口文档: http://127.0.0.1:{port}/docs")
    logger.info(f"后端根路由: http://127.0.0.1:{port}/")
    logger.info(f"健康检查: http://127.0.0.1:{port}/health")
    yield
    logger.info("DeepResearch API 正在关闭...")

app = FastAPI(
    title="DeepResearch API",
    description="智能文档研究助手API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # 前端开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info(f"Request {request_id}: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Request {request_id} completed in {process_time:.2f}s")
    
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": "Internal server error",
            "data": None
        }
    )

# 注册路由
app.include_router(research.router, prefix="/api/v1", tags=["research"])

@app.get("/")
async def root():
    return {
        "code": 200,
        "msg": "DeepResearch API is running",
        "data": {
            "version": "1.0.0",
            "status": "healthy"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "code": 200,
        "msg": "success",
        "data": {
            "status": "healthy",
            "timestamp": time.time()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        factory=False
    ) 