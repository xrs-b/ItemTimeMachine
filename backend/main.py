"""
ItemTimeMachine 后端入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1 import auth, items, categories, statistics, admin

app = FastAPI(
    title="ItemTimeMachine API",
    description="物品时光机后端API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(items.router, prefix="/api/v1/items", tags=["物品"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["分类"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["统计"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["管理员"])

# 挂载静态文件
import os
static_dir = "/code/data"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def startup():
    # 延迟创建数据库表
    from app.core.database import engine, Base
    Base.metadata.create_all(bind=engine)
    
    # 确保目录存在
    os.makedirs("/code/data/images", exist_ok=True)
    os.makedirs("/code/data/thumbnails", exist_ok=True)

@app.get("/")
def root():
    return {"message": "ItemTimeMachine API"}

@app.get("/health")
def health():
    return {"status": "ok"}
