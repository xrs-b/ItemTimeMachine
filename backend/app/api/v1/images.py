"""
图片API
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import ItemImage, Item, User
from app.api.v1.auth import get_current_user
import os
import uuid
from PIL import Image
from io import BytesIO

router = APIRouter()

# 图片存储目录
UPLOAD_DIR = "/data/images"
THUMBNAIL_DIR = "/data/thumbnails"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# 图片大小限制 (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

def create_thumbnail(image_data: bytes, filename: str) -> str:
    """生成缩略图"""
    img = Image.open(BytesIO(image_data))
    
    # 缩略图尺寸
    img.thumbnail((300, 300))
    
    # 保存缩略图
    thumb_filename = f"thumb_{filename}"
    thumb_path = os.path.join(THUMBNAIL_DIR, thumb_filename)
    
    img.save(thumb_path, img.format or 'JPEG')
    
    return thumb_filename

@router.post("/items/{item_id}/images")
async def upload_image(
    item_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
    
    # 保存缩略图记录
    thumb_image = ItemImage(
        item_id=item_id,
        image_type="thumbnail",
        image_path=thumb_filename,
        sort_order=max_order
    )
    db.add(thumb_image)
    
    db.commit()
    
    return {
        "id": image.id,
        "image_url": f"/static/images/{filename}",
        "thumbnail_url": f"/static/thumbnails/{thumb_filename}"
    }

@router.delete("/{image_id}")
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
    
    # 删除缩略图
    thumb_path = os.path.join(THUMBNAIL_DIR, f"thumb_{image.image_path}")
    if os.path.exists(thumb_path):
        os.remove(thumb_path)
    
    # 删除同类型的其他图片
    db.query(ItemImage).filter(
        ItemImage.item_id == image.item_id,
        ItemImage.image_type == image.image_type
    ).delete()
    
    db.commit()
    
    return {"message": "删除成功"}
