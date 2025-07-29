from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    food: str
    serving_size: str
    calories_kcal: float
    protein_g: Optional[float] = 0
    fat_g: Optional[float] = 0
    carbs_g: Optional[float] = 0

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    food_id: int
    
    class Config:
        from_attributes = True

class FoodRecognitionResponse(BaseModel):
    food_name: str
    confidence: float
    nutrition: dict