from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr

class UserBase(BaseModel):
    email: str
    mobile: str
    business_name: str
    address: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class OrderBase(BaseModel):
    cylinder_type_id: int
    quantity: int
    delivery_slot: datetime

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    total_amount: float
    payment_status: str
    order_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class CylinderTypeBase(BaseModel):
    name: str
    capacity: float
    price: float
    available_quantity: int

class CylinderTypeCreate(CylinderTypeBase):
    pass

class CylinderType(CylinderTypeBase):
    id: int

    class Config:
        from_attributes = True
