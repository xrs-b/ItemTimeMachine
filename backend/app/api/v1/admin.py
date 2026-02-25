"""
管理员API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import User
from app.api.v1.auth import get_current_user

router = APIRouter()

# 检查是否为管理员
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.is_admin != 1:
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user

class UserUpdate(BaseModel):
    is_active: int

@router.get("/users")
def get_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取所有用户列表"""
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """更新用户状态（禁用/启用）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 不能禁用管理员
    if user.is_admin == 1:
        raise HTTPException(status_code=400, detail="不能禁用管理员")
    
    user.is_active = data.is_active
    db.commit()
    
    return {"message": "更新成功"}
