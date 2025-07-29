from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse, UserLoginResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])

def calculate_bmr(gender: str, age: int, height: float, weight: float) -> float:
    if gender == 'M':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return round(bmr * 1.55, 0)

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    daily_target_calories = calculate_bmr(user.gender, user.age, user.height, user.weight)
    
    db_user = User(
        email=user.email,
        password=user.password,
        gender=user.gender,
        age=user.age,
        height=user.height,
        weight=user.weight,
        daily_target_calories=daily_target_calories
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=UserLoginResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credentials.email,
        User.password == user_credentials.password
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {"user_id": user.user_id, "email": user.email}