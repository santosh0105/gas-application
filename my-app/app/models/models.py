from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    BUSINESS = "business"
    DELIVERY = "delivery"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    business_name = Column(String)
    address = Column(String)
    role = Column(String, default=UserRole.BUSINESS)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    cylinders = relationship("CylinderInventory", back_populates="user")

class CylinderType(Base):
    __tablename__ = "cylinder_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    capacity = Column(Float)
    price = Column(Float)
    available_quantity = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cylinder_type_id = Column(Integer, ForeignKey("cylinder_types.id"))
    quantity = Column(Integer)
    total_amount = Column(Float)
    payment_status = Column(String)  # pending, paid, overdue
    order_status = Column(String)  # pending, confirmed, dispatched, delivered
    delivery_slot = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="orders")
    cylinder_type = relationship("CylinderType")

class CylinderInventory(Base):
    __tablename__ = "cylinder_inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cylinder_type_id = Column(Integer, ForeignKey("cylinder_types.id"))
    quantity = Column(Integer)
    status = Column(String)  # in-use, returned, pending-pickup
    
    # Relationships
    user = relationship("User", back_populates="cylinders")
    cylinder_type = relationship("CylinderType")
