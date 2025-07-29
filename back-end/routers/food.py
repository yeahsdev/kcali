from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.food import Food
from models.food_record import FoodRecord
from models.user import User
from schemas.food import FoodResponse, FoodRecognitionResponse
from schemas.food_record import FoodRecordCreate, FoodRecordResponse
from routers.users import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/food", tags=["food"])

@router.post("/recognize", response_model=FoodRecognitionResponse)
async def recognize_food(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return {
        "food_name": "김치찌개",
        "confidence": 0.95,
        "nutrition": {
            "calories_kcal": 450.0,
            "protein_g": 15.0,
            "fat_g": 10.0,
            "carbs_g": 30.0
        }
    }

@router.post("/records", response_model=FoodRecordResponse)
def create_food_record(
    record: FoodRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    food = db.query(Food).filter(Food.food_id == record.food_id).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    today_calories = db.query(FoodRecord).filter(
        FoodRecord.user_id == current_user.user_id,
        FoodRecord.datetime >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).with_entities(
        db.func.sum(FoodRecord.calories_kcal).label("total")
    ).scalar() or 0
    
    food_record = FoodRecord(
        user_id=current_user.user_id,
        food_id=record.food_id,
        daily_target_calories=current_user.daily_target_calories,
        food_name=food.food,
        calories_kcal=food.calories_kcal,
        protein_g=food.protein_g,
        fat_g=food.fat_g,
        carbs_g=food.carbs_g,
        daily_total_calories=today_calories + food.calories_kcal
    )
    
    db.add(food_record)
    db.commit()
    db.refresh(food_record)
    
    return food_record

@router.get("/records", response_model=List[FoodRecordResponse])
def get_food_records(
    date: datetime = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(FoodRecord).filter(FoodRecord.user_id == current_user.user_id)
    
    if date:
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = query.filter(
            FoodRecord.datetime >= start_of_day,
            FoodRecord.datetime <= end_of_day
        )
    
    return query.order_by(FoodRecord.datetime.desc()).all()