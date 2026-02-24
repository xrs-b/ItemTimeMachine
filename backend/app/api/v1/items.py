"""
物品API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.core.database import get_db
from app.models.models import Item, ItemImage, User
from app.api.v1.auth import get_current_user
from datetime import date as date_type

router = APIRouter()

# Pydantic模型
class ItemBase(BaseModel):
    name: str
    category_id: Optional[int] = None
    brand: Optional[str] = None
    purchase_date: date
    purchase_price: float
    platform: Optional[str] = None
    description: Optional[str] = None
    second_hand_price: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    platform: Optional[str] = None
    description: Optional[str] = None
    second_hand_price: Optional[float] = None

class ItemResponse(ItemBase):
    id: int
    user_id: int
    estimated_value: Optional[float] = None
    days_since_purchase: Optional[int] = None
    created_at: datetime
    images: List[dict] = []
    
    class Config:
        from_attributes = True

# 工具函数
def calculate_days_since_purchase(purchase_date: date) -> int:
    today = date.today()
    return (today - purchase_date).days

# API路由
@router.get("")
def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Item).filter(Item.user_id == current_user.id)
    
    # 筛选条件
    if category_id:
        query = query.filter(Item.category_id == category_id)
    if brand:
        query = query.filter(Item.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))
    if start_date:
        query = query.filter(Item.purchase_date >= start_date)
    if end_date:
        query = query.filter(Item.purchase_date <= end_date)
    
    # 按购买日期倒序
    query = query.order_by(Item.purchase_date.desc())
    
    # 分页
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 处理返回数据
    result = []
    for item in items:
        item_dict = {
            "id": item.id,
            "name": item.name,
            "category_id": item.category_id,
            "category_name": item.category.name if item.category else None,
            "brand": item.brand,
            "purchase_date": item.purchase_date,
            "purchase_price": item.purchase_price,
            "platform": item.platform,
            "description": item.description,
            "second_hand_price": item.second_hand_price,
            "estimated_value": item.estimated_value,
            "days_since_purchase": calculate_days_since_purchase(item.purchase_date),
            "created_at": item.created_at,
            "images": [
                {
                    "id": img.id,
                    "image_url": f"/static/images/{img.image_path}",
                    "thumbnail_url": f"/static/thumbnails/{img.image_path}",
                    "sort_order": img.sort_order
                }
                for img in sorted(item.images, key=lambda x: x.sort_order)
            ]
        }
        result.append(item_dict)
    
    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size,
        "has_more": (page * page_size) < total
    }

@router.get("/{item_id}")
def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    return {
        "id": item.id,
        "name": item.name,
        "category_id": item.category_id,
        "category_name": item.category.name if item.category else None,
        "brand": item.brand,
        "purchase_date": item.purchase_date,
        "purchase_price": item.purchase_price,
        "platform": item.platform,
        "description": item.description,
        "second_hand_price": item.second_hand_price,
        "estimated_value": item.estimated_value,
        "days_since_purchase": calculate_days_since_purchase(item.purchase_date),
        "created_at": item.created_at,
        "images": [
            {
                "id": img.id,
                "image_url": f"/static/images/{img.image_path}",
                "thumbnail_url": f"/static/thumbnails/{img.image_path}",
                "sort_order": img.sort_order
            }
            for img in sorted(item.images, key=lambda x: x.sort_order)
        ]
    }

@router.post("")
def create_item(
    item_data: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = Item(
        user_id=current_user.id,
        name=item_data.name,
        category_id=item_data.category_id,
        brand=item_data.brand,
        purchase_date=item_data.purchase_date,
        purchase_price=item_data.purchase_price,
        platform=item_data.platform,
        description=item_data.description,
        second_hand_price=item_data.second_hand_price,
        estimated_value=item_data.second_hand_price or item_data.purchase_price,
        days_since_purchase=calculate_days_since_purchase(item_data.purchase_date)
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item

@router.put("/{item_id}")
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    # 更新字段
    update_data = item_data.model_dump(exclude_unset=True)
    if "purchase_date" in update_data:
        update_data["days_since_purchase"] = calculate_days_since_purchase(update_data["purchase_date"])
    
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    db.delete(item)
    db.commit()
    
    return {"message": "删除成功"}
