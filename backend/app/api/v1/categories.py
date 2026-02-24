"""
分类API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.models.models import Category, User

router = APIRouter()

# 预设分类数据
DEFAULT_CATEGORIES = [
    # 数码产品
    {"name": "手机", "parent_id": 1},
    {"name": "电脑", "parent_id": 1},
    {"name": "相机", "parent_id": 1},
    {"name": "镜头", "parent_id": 1},
    {"name": "耳机", "parent_id": 1},
    {"name": "智能手表", "parent_id": 1},
    {"name": "游戏机", "parent_id": 1},
    {"name": "存储设备", "parent_id": 1},
    {"name": "其他数码", "parent_id": 1},
    # 衣服
    {"name": "JK制服", "parent_id": 2},
    {"name": "洛丽塔", "parent_id": 2},
    {"name": "汉服", "parent_id": 2},
    {"name": "上装", "parent_id": 2},
    {"name": "下装", "parent_id": 2},
    {"name": "外套", "parent_id": 2},
    {"name": "鞋", "parent_id": 2},
    {"name": "配饰", "parent_id": 2},
    # 化妆品
    {"name": "底妆", "parent_id": 3},
    {"name": "彩妆", "parent_id": 3},
    {"name": "护肤", "parent_id": 3},
    {"name": "香水", "parent_id": 3},
    {"name": "美容工具", "parent_id": 3},
    # 其他
    {"name": "书籍", "parent_id": 4},
    {"name": "乐器", "parent_id": 4},
    {"name": "运动器材", "parent_id": 4},
    {"name": "家具", "parent_id": 4},
    {"name": "其他", "parent_id": 4},
]

class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    
    class Config:
        from_attributes = True

@router.get("")
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 获取用户的所有分类
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    
    # 如果没有分类，创建预设分类
    if not categories:
        # 一级分类
        parent_categories = [
            {"name": "数码产品", "user_id": current_user.id},
            {"name": "衣服", "user_id": current_user.id},
            {"name": "化妆品", "user_id": current_user.id},
            {"name": "其他", "user_id": current_user.id},
        ]
        
        parent_ids = {}
        for pc in parent_categories:
            cat = Category(**pc)
            db.add(cat)
            db.commit()
            db.refresh(cat)
            parent_ids[cat.name] = cat.id
        
        # 二级分类
        category_mapping = {
            "手机": "数码产品",
            "电脑": "数码产品",
            "相机": "数码产品",
            "镜头": "数码产品",
            "耳机": "数码产品",
            "智能手表": "数码产品",
            "游戏机": "数码产品",
            "存储设备": "数码产品",
            "其他数码": "数码产品",
            "JK制服": "衣服",
            "洛丽塔": "衣服",
            "汉服": "衣服",
            "上装": "衣服",
            "下装": "衣服",
            "外套": "衣服",
            "鞋": "衣服",
            "配饰": "衣服",
            "底妆": "化妆品",
            "彩妆": "化妆品",
            "护肤": "化妆品",
            "香水": "化妆品",
            "美容工具": "化妆品",
            "书籍": "其他",
            "乐器": "其他",
            "运动器材": "其他",
            "家具": "其他",
            "其他": "其他",
        }
        
        for cat_name, parent_name in category_mapping.items():
            if parent_name in parent_ids:
                cat = Category(
                    name=cat_name,
                    parent_id=parent_ids[parent_name],
                    user_id=current_user.id
                )
                db.add(cat)
        
        db.commit()
        categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    
    # 构造成树形结构
    result = []
    for cat in categories:
        if cat.parent_id is None:
            children = [
                {"id": c.id, "name": c.name}
                for c in cat.children
            ]
            result.append({
                "id": cat.id,
                "name": cat.name,
                "children": children
            })
    
    return result

@router.post("")
def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = Category(
        user_id=current_user.id,
        name=category_data.name,
        parent_id=category_data.parent_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category

@router.put("/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    if category_data.name:
        category.name = category_data.name
    
    db.commit()
    db.refresh(category)
    
    return category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 检查是否有子分类
    if category.children:
        raise HTTPException(status_code=400, detail="请先删除子分类")
    
    db.delete(category)
    db.commit()
    
    return {"message": "删除成功"}
