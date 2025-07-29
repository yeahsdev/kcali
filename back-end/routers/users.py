from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.user import User
from schemas.user import UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

def get_current_user(
    user_id: Optional[int] = None,
    x_user_id: Optional[int] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    uid = user_id or x_user_id
    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID required"
        )
    
    user = db.query(User).filter(User.user_id == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/me", response_model=UserResponse)
def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_info(
    height: Optional[float] = None,
    weight: Optional[float] = None,
    age: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if height:
        current_user.height = height
    if weight:
        current_user.weight = weight
    if age:
        current_user.age = age
    
    if height or weight or age:
        from routers.auth import calculate_bmr
        current_user.daily_target_calories = calculate_bmr(
            current_user.gender,
            current_user.age,
            current_user.height,
            current_user.weight
        )
    
    db.commit()
    db.refresh(current_user)
    
    return current_user