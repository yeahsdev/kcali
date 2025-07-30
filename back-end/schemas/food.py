# 음식 관련 Pydantic 스키마
from pydantic import BaseModel
from typing import Optional

class FoodNutrition(BaseModel):
    protein_g: float
    fat_g: float
    carbs_g: float

class FoodInfo(BaseModel):
    food_id: int
    food_name: str
    serving_size: str
    calories: float
    nutrition: FoodNutrition
    
    class Config:
        orm_mode = True

class FoodUploadResponse(BaseModel):
    food_name: str
    confidence: float
    calories: float
    serving_size: str
    nutrition: FoodNutrition
    message: Optional[str] = None

class FoodSearchItem(BaseModel):
    food_id: int
    food_name: str
    serving_size: str
    calories: float
    nutrition: FoodNutrition
    
    class Config:
        orm_mode = True

class FoodSearchResponse(BaseModel):
    results: list[FoodSearchItem]
    total_count: int
    query: str

class FoodRecordRequest(BaseModel):
    user_id: int
    food_id: int
    serving_amount: float = 1.0

class FoodRecordResponse(BaseModel):
    record_id: int
    message: str
    daily_total_calories: float
    recorded_food: FoodInfo