# 음식 처리 로직
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.food_record import FoodRecord
from models.user import User
from typing import Optional

def calculate_daily_calories(db: Session, user_id: int, target_date: Optional[date] = None) -> float:
    """
    특정 날짜의 사용자 총 칼로리 섭취량을 계산합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 사용자 ID
        target_date: 계산할 날짜 (기본값: 오늘)
    
    Returns:
        해당 날짜의 총 칼로리
    """
    if target_date is None:
        target_date = date.today()
    
    # 해당 날짜의 시작과 끝
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())
    
    # 해당 날짜의 모든 식사 기록의 칼로리 합계
    total_calories = db.query(func.sum(FoodRecord.calories_kcal)).filter(
        and_(
            FoodRecord.user_id == user_id,
            FoodRecord.datetime >= start_of_day,
            FoodRecord.datetime <= end_of_day
        )
    ).scalar()
    
    return float(total_calories or 0)