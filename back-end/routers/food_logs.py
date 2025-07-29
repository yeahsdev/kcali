from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
import os
import tempfile
from database import get_db
from models.food import Food
from models.food_record import FoodRecord
from models.user import User
from schemas.food_logs import DailyFoodLogsResponse, FoodLogItem, FoodAnalyzeResponse
from ai.model import food_classifier
from utils.auth import get_current_user_auth

router = APIRouter(prefix="/api/v1/foods", tags=["food_logs"])

@router.get("/logs/{year}/{month}/{day}/", response_model=DailyFoodLogsResponse)
def get_daily_food_logs(
    year: int,
    month: int,
    day: int,
    current_user: User = Depends(get_current_user_auth),
    db: Session = Depends(get_db)
):
    try:
        target_date = date(year, month, day)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date"
        )
    
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())
    
    food_records = db.query(FoodRecord).filter(
        FoodRecord.user_id == current_user.user_id,
        FoodRecord.datetime >= start_of_day,
        FoodRecord.datetime <= end_of_day
    ).all()
    
    food_logs = []
    total_consumed = 0
    
    for record in food_records:
        food_logs.append(FoodLogItem(
            id=record.record_id,
            name=record.food_name,
            kcal=record.calories_kcal
        ))
        total_consumed += record.calories_kcal
    
    return DailyFoodLogsResponse(
        date=target_date.strftime("%Y-%m-%d"),
        goal_kcal=current_user.daily_target_calories,
        consumed_kcal=total_consumed,
        food_logs=food_logs
    )

@router.post("/analyze/", response_model=FoodAnalyzeResponse)
async def analyze_food_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user_auth),
    db: Session = Depends(get_db)
):
    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        content = await image.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Use AI model to predict food
        food_name, confidence = food_classifier.predict(tmp_file_path)
        
        if confidence < 0.5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not identify food with sufficient confidence"
            )
        
        # Find food in database
        food = db.query(Food).filter(
            func.lower(Food.food) == func.lower(food_name)
        ).first()
        
        if not food:
            # If exact match not found, try to find similar
            food = db.query(Food).filter(
                Food.food.ilike(f"%{food_name}%")
            ).first()
        
        if not food:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Food '{food_name}' not found in database"
            )
        
        # Calculate today's total calories before adding new food
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_calories = db.query(func.sum(FoodRecord.calories_kcal)).filter(
            FoodRecord.user_id == current_user.user_id,
            FoodRecord.datetime >= today_start
        ).scalar() or 0
        
        # Create food record
        food_record = FoodRecord(
            user_id=current_user.user_id,
            food_id=food.food_id,
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
        
        return FoodAnalyzeResponse(
            message="성공적으로 기록되었습니다.",
            added_food={
                "name": food.food,
                "kcal": food.calories_kcal
            },
            updated_consumed_kcal=today_calories + food.calories_kcal
        )
        
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)