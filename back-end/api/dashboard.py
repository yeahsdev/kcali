# 대시보드 데이터 API
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date, timedelta
from typing import Optional
from database.connection import get_db
from schemas.dashboard import DashboardTodayResponse, MealRecord, DashboardHistoryResponse, DailyHistory
from models.user import User
from models.food_record import FoodRecord
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/v1/dashboard/today", response_model=DashboardTodayResponse)
async def get_today_dashboard(
    user_id: int = Query(..., description="사용자 ID"),
    db: Session = Depends(get_db)
):
    """
    오늘의 칼로리 섭취 현황을 조회합니다.
    
    - **user_id**: 사용자 ID (헤더나 쿼리 파라미터로 전달)
    """
    try:
        # 사용자 확인
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        # 오늘 날짜
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        # 오늘의 식사 기록 조회
        today_records = db.query(FoodRecord).filter(
            and_(
                FoodRecord.user_id == user_id,
                FoodRecord.datetime >= start_of_day,
                FoodRecord.datetime <= end_of_day
            )
        ).order_by(FoodRecord.datetime).all()
        
        # 총 칼로리 계산
        consumed_calories = sum(record.calories_kcal for record in today_records)
        daily_target = float(user.daily_target_calories)
        remaining_calories = daily_target - consumed_calories
        progress_percentage = (consumed_calories / daily_target * 100) if daily_target > 0 else 0
        
        # 식사 기록 변환
        meals = []
        for record in today_records:
            meals.append(MealRecord(
                record_id=record.record_id,
                time=record.datetime.strftime("%H:%M"),
                food_name=record.food_name,
                calories=record.calories_kcal
            ))
        
        return DashboardTodayResponse(
            date=today.strftime("%Y-%m-%d"),
            daily_target_calories=daily_target,
            consumed_calories=consumed_calories,
            remaining_calories=remaining_calories,
            progress_percentage=min(progress_percentage, 100),  # 100% 초과 방지
            meals=meals
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"대시보드 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"대시보드 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/v1/dashboard/history", response_model=DashboardHistoryResponse)
async def get_dashboard_history(
    user_id: int = Query(..., description="사용자 ID"),
    start_date: Optional[date] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    지정된 기간의 섭취 기록을 조회합니다.
    
    - **user_id**: 사용자 ID
    - **start_date**: 조회 시작 날짜 (기본값: 7일 전)
    - **end_date**: 조회 종료 날짜 (기본값: 오늘)
    """
    try:
        # 사용자 확인
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        # 기본값 설정 (최근 7일)
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=6)
        
        # 날짜 유효성 검사
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="시작 날짜는 종료 날짜보다 이전이어야 합니다."
            )
        
        # 기간별 칼로리 집계
        daily_stats = db.query(
            func.date(FoodRecord.datetime).label('date'),
            func.sum(FoodRecord.calories_kcal).label('total_calories'),
            func.count(FoodRecord.record_id).label('meals_count')
        ).filter(
            and_(
                FoodRecord.user_id == user_id,
                func.date(FoodRecord.datetime) >= start_date,
                func.date(FoodRecord.datetime) <= end_date
            )
        ).group_by(
            func.date(FoodRecord.datetime)
        ).order_by(
            func.date(FoodRecord.datetime).desc()
        ).all()
        
        # 결과 변환
        records = []
        for stat in daily_stats:
            records.append(DailyHistory(
                date=stat.date.strftime("%Y-%m-%d"),
                total_calories=float(stat.total_calories),
                target_calories=float(user.daily_target_calories),
                meals_count=stat.meals_count
            ))
        
        return DashboardHistoryResponse(
            records=records,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"기록 조회 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"기록 조회 중 오류가 발생했습니다: {str(e)}"
        )