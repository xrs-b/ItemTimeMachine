"""
物品API - 包含图片上传功能
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from app.core.database import get_db
from app.models.models import Item, ItemImage, User
from app.api.v1.auth import get_current_user
import os
import uuid
from PIL import Image
from io import BytesIO

router = APIRouter()

# 图片存储目录
UPLOAD_DIR = "/code/data/images"
THUMBNAIL_DIR = "/code/data/thumbnails"

# 确保目录存在
def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# 图片大小限制 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

def create_thumbnail(image_data: bytes, filename: str) -> str:
    """生成缩略图"""
    img = Image.open(BytesIO(image_data))
    img.thumbnail((300, 300))
    thumb_filename = f"thumb_{filename}"
    thumb_path = os.path.join(THUMBNAIL_DIR, thumb_filename)
    img.save(thumb_path, img.format or 'JPEG')
    return thumb_filename

def calculate_days_since_purchase(purchase_date: date) -> int:
    today = date.today()
    return (today - purchase_date).days

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

# API路由
@router.get("")
def get_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Item).filter(Item.user_id == current_user.id)
    
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
    query = query.options(joinedload(Item.category)).order_by(desc(Item.purchase_date))
    
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    
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
            "estimated_value": item.estimated_value or item.purchase_price,
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
    item = db.query(Item).options(
        joinedload(Item.category),
        joinedload(Item.images)
    ).filter(
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
        "estimated_value": item.estimated_value or item.purchase_price,
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
    
    update_data = item_data.model_dump(exclude_unset=False)
    # 删除None值，让SQLAlchemy保持原值
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    if "purchase_date" in update_data and update_data["purchase_date"]:
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

# 图片上传API
@router.post("/{item_id}/images")
async def upload_image(
    item_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 确保目录存在
    ensure_dirs()
    
    # 检查物品是否存在且属于当前用户
    item = db.query(Item).filter(
        Item.id == item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    # 检查文件大小
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过10MB")
    
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    
    # 保存原图
    original_path = os.path.join(UPLOAD_DIR, filename)
    with open(original_path, "wb") as f:
        f.write(contents)
    
    # 生成缩略图
    thumb_filename = create_thumbnail(contents, filename)
    
    # 获取当前最大排序
    max_order = db.query(ItemImage).filter(ItemImage.item_id == item_id).count()
    
    # 保存到数据库
    image = ItemImage(
        item_id=item_id,
        image_type="original",
        image_path=filename,
        sort_order=max_order
    )
    db.add(image)
    db.commit()
    
    return {
        "id": image.id,
        "image_url": f"/static/images/{filename}",
        "thumbnail_url": f"/static/thumbnails/{thumb_filename}"
    }

@router.delete("/images/{image_id}")
def delete_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    image = db.query(ItemImage).filter(ItemImage.id == image_id).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    # 检查物品是否属于当前用户
    item = db.query(Item).filter(
        Item.id == image.item_id,
        Item.user_id == current_user.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    # 删除文件
    if os.path.exists(os.path.join(UPLOAD_DIR, image.image_path)):
        os.remove(os.path.join(UPLOAD_DIR, image.image_path))
    
    thumb_path = os.path.join(THUMBNAIL_DIR, f"thumb_{image.image_path}")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    db.delete(image)
    db.commit()
    
    return {"message": "删除成功"}
