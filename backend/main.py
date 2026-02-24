"""
ItemTimeMachine 后端入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, items, categories, images, statistics
from app.core.database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

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
app.include_router(images.router, prefix="/api/v1/images", tags=["图片"])
app.include_router(statistics.router, prefix="/api/v1/statistics", tags=["统计"])

@app.get("/")
def root():
    return {"message": "ItemTimeMachine API"}

@app.get("/health")
def health():
    return {"status": "ok"}
