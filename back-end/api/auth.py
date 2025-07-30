from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.connection import get_db
from models.user import User
from schemas.user import SignupRequest, SignupResponse, LoginRequest, LoginResponse
from services.calorie_service import calculate_bmr, calculate_daily_calories

router = APIRouter()

@router.post("/v1/users/signup/", response_model=SignupResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """회원가입 API"""
    
    # 비밀번호 확인
    if request.password != request.password_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호가 일치하지 않습니다."
        )
    
    # gender 변환 (male -> M, female -> F)
    gender_code = 'M' if request.gender == 'male' else 'F'
    
    # BMR 계산 및 일일 권장 칼로리 계산
    bmr = calculate_bmr(gender_code, request.age, request.height, request.weight)
    daily_calories = calculate_daily_calories(bmr)
    
    # 사용자 생성
    try:
        new_user = User(
            email=request.email,
            password=request.password,  # 평문 저장
            gender=gender_code,
            age=request.age,
            height=request.height,
            weight=request.weight,
            daily_target_calories=daily_calories
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return SignupResponse(message="회원가입이 완료되었습니다.")
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용중인 이메일입니다."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/v1/users/login/", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """로그인 API"""
    
    # 사용자 조회
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다."
        )
    
    # 비밀번호 확인 (평문 비교)
    if user.password != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 일치하지 않습니다."
        )
    
    # JWT 대신 user_id를 토큰으로 사용
    return LoginResponse(
        access_token=str(user.user_id),
        user_id=user.user_id
    )