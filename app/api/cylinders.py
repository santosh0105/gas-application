from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_active_user
from app.db.session import get_db
from app.models.models import User, CylinderType, CylinderInventory, UserRole
from app.schemas.schemas import CylinderTypeCreate, CylinderType as CylinderTypeSchema

router = APIRouter()

@router.post("/cylinder-types/", response_model=CylinderTypeSchema)
def create_cylinder_type(
    cylinder_type: CylinderTypeCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_cylinder_type = CylinderType(**cylinder_type.dict())
    db.add(db_cylinder_type)
    db.commit()
    db.refresh(db_cylinder_type)
    return db_cylinder_type

@router.get("/cylinder-types/", response_model=List[CylinderTypeSchema])
def list_cylinder_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    cylinder_types = db.query(CylinderType).offset(skip).limit(limit).all()
    return cylinder_types

@router.put("/cylinder-types/{cylinder_type_id}/inventory")
def update_cylinder_inventory(
    cylinder_type_id: int,
    quantity: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    cylinder_type = db.query(CylinderType).filter(CylinderType.id == cylinder_type_id).first()
    if not cylinder_type:
        raise HTTPException(status_code=404, detail="Cylinder type not found")
    
    cylinder_type.available_quantity = quantity
    db.add(cylinder_type)
    db.commit()
    db.refresh(cylinder_type)
    return {"message": "Inventory updated successfully"}

@router.get("/cylinders/user/", response_model=List[dict])
def get_user_cylinders(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    cylinders = db.query(CylinderInventory).filter(
        CylinderInventory.user_id == current_user.id
    ).all()
    
    result = []
    for cylinder in cylinders:
        result.append({
            "id": cylinder.id,
            "cylinder_type": cylinder.cylinder_type.name,
            "quantity": cylinder.quantity,
            "status": cylinder.status
        })
    return result
