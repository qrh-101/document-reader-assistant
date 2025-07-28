from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid
from loguru import logger

from app.routers import research
from app.core.config import settings

app = FastAPI(
    title="DeepResearch API",
    description="智能文档研究助手API",
    version="1.0.0"
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