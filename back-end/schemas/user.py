from pydantic import BaseModel, EmailStr, validator
from typing import Optional

# 회원가입 요청 스키마
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    password_check: str
    gender: str  # "male" or "female"
    age: int
    height: float
    weight: float
    
    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ['male', 'female']:
            raise ValueError('Gender must be either "male" or "female"')
        return v.lower()
    
    @validator('age')
    def validate_age(cls, v):
        if v < 1 or v > 150:
            raise ValueError('Age must be between 1 and 150')
        return v
    
    @validator('height')
    def validate_height(cls, v):
        if v < 50 or v > 300:
            raise ValueError('Height must be between 50 and 300 cm')
        return v
    
    @validator('weight')
    def validate_weight(cls, v):
        if v < 20 or v > 500:
            raise ValueError('Weight must be between 20 and 500 kg')
        return v

# 회원가입 응답 스키마
class SignupResponse(BaseModel):
    message: str

# 로그인 요청 스키마
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 로그인 응답 스키마
class LoginResponse(BaseModel):
    access_token: str
    user_id: int

# 사용자 정보 스키마
class UserInfo(BaseModel):
    user_id: int
    email: str
    gender: str
    age: int
    height: float
    weight: float
    daily_target_calories: float
    
    class Config:
        orm_mode = True