"""
数据库模型
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Integer, default=0)  # 0:普通用户, 1:管理员
    is_active = Column(Integer, default=1)  # 1:正常, 0:禁用
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联
    items = relationship("Item", back_populates="user")
    categories = relationship("Category", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联
    user = relationship("User", back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="children")
    items = relationship("Item", back_populates="category")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    brand = Column(String(50), nullable=True)
    purchase_date = Column(Date, nullable=False)
    purchase_price = Column(Float, nullable=False)
    platform = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    second_hand_price = Column(Float, nullable=True)
    estimated_value = Column(Float, nullable=True)
    days_since_purchase = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联
    user = relationship("User", back_populates="items")
    category = relationship("Category", back_populates="items")
    images = relationship("ItemImage", back_populates="item", cascade="all, delete-orphan")

class ItemImage(Base):
    __tablename__ = "item_images"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    image_type = Column(String(20), default="original")  # original / thumbnail
    image_path = Column(String(255), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联
    item = relationship("Item", back_populates="images")
