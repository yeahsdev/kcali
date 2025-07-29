from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    gender: str
    age: int
    height: float
    weight: float

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    password_check: str
    gender: str
    age: int
    height: float
    weight: float
    
    @validator('password_check')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() in ['male', 'm']:
            return 'M'
        elif v.lower() in ['female', 'f']:
            return 'F'
        else:
            raise ValueError('gender must be male or female')

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    user_id: int
    daily_target_calories: float
    
    class Config:
        from_attributes = True

class UserLoginResponse(BaseModel):
    user_id: int
    email: str

class SignupResponse(BaseModel):
    message: str
    user: dict

class LoginResponse(BaseModel):
    message: str
    user_id: int