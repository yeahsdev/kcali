from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    gender: str
    age: int
    height: float
    weight: float

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