from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.food_record import FoodRecord
from schemas.food_record import DailySummaryResponse
from routers.users import get_current_user
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DailySummaryResponse)
def get_daily_summary(
    date: Optional[datetime] = Query(None, description="Date for summary (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not date:
        date = datetime.now()
    
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    food_records = db.query(FoodRecord).filter(
        FoodRecord.user_id == current_user.user_id,
        FoodRecord.datetime >= start_of_day,
        FoodRecord.datetime <= end_of_day
    ).all()
    
    total_consumed = sum(record.calories_kcal for record in food_records)
    daily_target = current_user.daily_target_calories
    remaining = max(0, daily_target - total_consumed)
    percentage = (total_consumed / daily_target * 100) if daily_target > 0 else 0
    
    return {
        "daily_target_calories": daily_target,
        "total_consumed": total_consumed,
        "remaining": remaining,
        "percentage": round(percentage, 1),
        "meals": food_records
    }

@router.get("/weekly")
def get_weekly_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    records = db.query(
        db.func.date(FoodRecord.datetime).label("date"),
        db.func.sum(FoodRecord.calories_kcal).label("total_calories")
    ).filter(
        FoodRecord.user_id == current_user.user_id,
        FoodRecord.datetime >= start_date,
        FoodRecord.datetime <= end_date
    ).group_by(
        db.func.date(FoodRecord.datetime)
    ).all()
    
    return {
        "target_calories": current_user.daily_target_calories,
        "weekly_data": [
            {
                "date": str(record.date),
                "total_calories": float(record.total_calories)
            }
            for record in records
        ]
    }