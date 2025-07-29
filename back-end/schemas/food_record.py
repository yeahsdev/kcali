from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class FoodRecordBase(BaseModel):
    food_id: int
    
class FoodRecordCreate(FoodRecordBase):
    user_id: int

class FoodRecordResponse(BaseModel):
    record_id: int
    datetime: datetime
    user_id: int
    food_id: int
    food_name: str
    calories_kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float
    
    class Config:
        from_attributes = True

class DailySummaryResponse(BaseModel):
    daily_target_calories: float
    total_consumed: float
    remaining: float
    percentage: float
    meals: List[FoodRecordResponse]