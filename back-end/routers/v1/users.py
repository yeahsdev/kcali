from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserSignup, UserLogin, SignupResponse, LoginResponse
from services.nutrition import calculate_daily_calories

router = APIRouter(prefix="/api/v1/users", tags=["v1_users"])

@router.post("/signup/", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Calculate daily target calories
    daily_target_calories = calculate_daily_calories(
        user_data.gender, 
        user_data.age, 
        user_data.height, 
        user_data.weight
    )
    
    # Create new user with plain password
    db_user = User(
        email=user_data.email,
        password=user_data.password,  # Store plain password
        gender=user_data.gender,
        age=user_data.age,
        height=user_data.height,
        weight=user_data.weight,
        daily_target_calories=daily_target_calories
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return SignupResponse(
        message="회원가입이 성공적으로 완료되었습니다.",
        user={"email": db_user.email}
    )

@router.post("/login/", response_model=LoginResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify plain password
    if user.password != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Return user_id instead of JWT tokens
    return LoginResponse(
        message="로그인 성공",
        user_id=user.user_id
    )