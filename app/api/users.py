from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import get_current_active_user, get_password_hash
from app.db.session import get_db
from app.models.models import User, UserRole
from app.schemas.schemas import UserCreate, User as UserSchema, UserUpdate

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Set admin role for any email containing 'admin'
    is_admin = 'admin' in user.email.lower()
    
    db_user = User(
        email=user.email,
        mobile=user.mobile,
        business_name=user.business_name,
        address=user.address,
        hashed_password=get_password_hash(user.password),
        role="admin" if is_admin else "business"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/me", response_model=UserSchema)
def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password" and value:
            value = get_password_hash(value)
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/users/", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    users = db.query(User).offset(skip).limit(limit).all()
    return users
