"""
统计API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date, datetime
from app.core.database import get_db
from app.models.models import Item, Category, User
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/summary")
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取总体统计"""
    # 总花费
    total_expense = db.query(func.sum(Item.purchase_price)).filter(
        Item.user_id == current_user.id
    ).scalar() or 0
    
    # 物品数量
    total_items = db.query(func.count(Item.id)).filter(
        Item.user_id == current_user.id
    ).scalar() or 0
    
    # 二手总价值
    total_estimated = db.query(func.sum(Item.estimated_value)).filter(
        Item.user_id == current_user.id
    ).scalar() or 0
    
    return {
        "total_expense": total_expense,
        "total_items": total_items,
        "total_estimated_value": total_estimated,
        "depreciation": total_expense - total_estimated
    }

@router.get("/by-category")
def get_by_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """按分类统计"""
    results = db.query(
        Category.name,
        func.count(Item.id).label("count"),
        func.sum(Item.purchase_price).label("total")
    ).join(
        Item, Item.category_id == Category.id
    ).filter(
        Item.user_id == current_user.id
    ).group_by(Category.name).all()
    
    return [
        {"category": r[0], "count": r[1], "total": r[2] or 0}
        for r in results
    ]

@router.get("/by-platform")
def get_by_platform(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """按平台统计"""
    results = db.query(
        Item.platform,
        func.count(Item.id).label("count"),
        func.sum(Item.purchase_price).label("total")
    ).filter(
        Item.user_id == current_user.id,
        Item.platform.isnot(None)
    ).group_by(Item.platform).all()
    
    return [
        {"platform": r[0], "count": r[1], "total": r[2] or 0}
        for r in results
    ]

@router.get("/trend")
def get_trend(
    year: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """月度消费趋势"""
    if not year:
        year = datetime.now().year
    
    results = db.query(
        func.strftime("%m", Item.purchase_date).label("month"),
        func.sum(Item.purchase_price).label("total"),
        func.count(Item.id).label("count")
    ).filter(
        Item.user_id == current_user,
        func.strftime("%Y", Item.purchase_date) == str(year)
    ).group_by("month").all()
    
    # 补齐所有月份
    monthly_data = {f"{i:02d}": {"total": 0, "count": 0} for i in range(1, 13)}
    
    for r in results:
        month = r[0]
        monthly_data[month] = {"total": r[1] or 0, "count": r[2]}
    
    return [
        {"month": month, **data}
        for month, data in monthly_data.items()
    ]
