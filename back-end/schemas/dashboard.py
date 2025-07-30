# 대시보드 응답 스키마
from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional

class MealRecord(BaseModel):
    record_id: int
    time: str  # HH:MM 형식
    food_name: str
    calories: float
    
    class Config:
        orm_mode = True

class DashboardTodayResponse(BaseModel):
    date: str  # YYYY-MM-DD 형식
    daily_target_calories: float
    consumed_calories: float
    remaining_calories: float
    progress_percentage: float
    meals: List[MealRecord]

class DailyHistory(BaseModel):
    date: str  # YYYY-MM-DD 형식
    total_calories: float
    target_calories: float
    meals_count: int

class DashboardHistoryResponse(BaseModel):
    records: List[DailyHistory]
    start_date: str
    end_date: str