from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.models.models import User, Order, CylinderType
from app.schemas.schemas import OrderCreate, Order as OrderSchema

router = APIRouter()

@router.post("/orders/", response_model=OrderSchema)
def create_order(
    order: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify cylinder type exists and has available quantity
    cylinder_type = db.query(CylinderType).filter(CylinderType.id == order.cylinder_type_id).first()
    if not cylinder_type:
        raise HTTPException(status_code=404, detail="Cylinder type not found")
    if cylinder_type.available_quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Not enough cylinders available")
    
    # Calculate total amount
    total_amount = cylinder_type.price * order.quantity
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        cylinder_type_id=order.cylinder_type_id,
        quantity=order.quantity,
        total_amount=total_amount,
        payment_status="pending",
        order_status="pending",
        delivery_slot=order.delivery_slot
    )
    
    # Update available quantity
    cylinder_type.available_quantity -= order.quantity
    
    db.add(db_order)
    db.add(cylinder_type)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/", response_model=List[OrderSchema])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        orders = db.query(Order).offset(skip).limit(limit).all()
    else:
        orders = db.query(Order).filter(Order.user_id == current_user.id).offset(skip).limit(limit).all()
    return orders

@router.get("/orders/{order_id}", response_model=OrderSchema)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return order

@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role not in ["admin", "delivery"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.order_status = status
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"message": "Order status updated successfully"}
