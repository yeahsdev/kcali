from pydantic import BaseModel
from typing import List
from datetime import date

class FoodLogItem(BaseModel):
    id: int
    name: str
    kcal: float

class DailyFoodLogsResponse(BaseModel):
    date: str
    goal_kcal: float
    consumed_kcal: float
    food_logs: List[FoodLogItem]

class FoodAnalyzeResponse(BaseModel):
    message: str
    added_food: dict
    updated_consumed_kcal: float