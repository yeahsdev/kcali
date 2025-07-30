# 음식 기록, 조회 API
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database.connection import get_db
from schemas.food import (
    FoodUploadResponse, FoodNutrition, FoodSearchResponse, 
    FoodSearchItem, FoodRecordRequest, FoodRecordResponse, FoodInfo
)
from models.food import Food
from models.food_record import FoodRecord
from models.user import User
from services.ai_service import recognize_food
from services.food_service import calculate_daily_calories
from utils.image_processing import validate_image
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/v1/food/upload", response_model=FoodUploadResponse)
async def upload_food_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    음식 사진을 업로드하고 AI로 인식한 결과를 반환합니다.
    """
    try:
        # 이미지 파일 유효성 검사
        await validate_image(file)

        # 이미지 데이터 읽기
        image_data = await file.read()

        # AI 모델로 음식 인식
        recognition_result = await recognize_food(image_data, db)

        # ==================== 디버깅 코드 1 ====================
        # AI 서비스가 반환한 딕셔너리 결과를 터미널에 출력합니다.
        print(f"--- AI 인식 결과 (recognition_result) ---")
        print(recognition_result)
        print("----------------------------------------")
        # =======================================================
        
        if not recognition_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="음식을 인식할 수 없습니다."
            )

        # 응답 생성
        response = FoodUploadResponse(
            food_name=recognition_result["food_name"],
            confidence=recognition_result["confidence"],
            calories=recognition_result["calories"],
            serving_size=recognition_result["serving_size"],
            nutrition=FoodNutrition(**recognition_result["nutrition"]),
            message=f"{recognition_result['food_name']}이(가) {recognition_result['confidence']*100:.1f}% 확률로 인식되었습니다."
        )

        # ==================== 디버깅 코드 2 ====================
        # 프론트엔드로 보내기 직전의 최종 응답 객체를 JSON 형태로 출력합니다.
        print(f"--- 최종 응답 객체 (response) ---")
        # .model_dump_json()을 쓰면 내용을 예쁘게 볼 수 있습니다.
        print(response.model_dump_json(indent=2)) 
        print("---------------------------------")
        # =======================================================
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"음식 인식 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"음식 인식 처리 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/v1/food/search", response_model=FoodSearchResponse)
async def search_food(
    q: str = Query(..., min_length=1, description="검색어"),
    limit: int = Query(10, ge=1, le=50, description="최대 결과 수"),
    db: Session = Depends(get_db)
):
    """
    음식명으로 검색하여 칼로리 및 영양 정보를 조회합니다.
    
    - **q**: 검색할 음식명 (부분 일치 검색)
    - **limit**: 반환할 최대 결과 수 (1-50, 기본값: 10)
    """
    try:
        # 검색어로 음식 검색 (대소문자 구분 없이 부분 일치)
        query = db.query(Food).filter(
            Food.food.ilike(f"%{q}%")
        )
        
        # 전체 결과 수
        total_count = query.count()
        
        # 제한된 수만큼 결과 가져오기
        foods = query.limit(limit).all()
        
        # 결과 변환
        results = []
        for food in foods:
            results.append(FoodSearchItem(
                food_id=food.food_id,
                food_name=food.food,
                serving_size=food.serving_size,
                calories=food.calories_kcal,
                nutrition=FoodNutrition(
                    protein_g=food.protein_g,
                    fat_g=food.fat_g,
                    carbs_g=food.carbs_g
                )
            ))
        
        return FoodSearchResponse(
            results=results,
            total_count=total_count,
            query=q
        )
        
    except Exception as e:
        logger.error(f"음식 검색 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"음식 검색 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/v1/food/record", response_model=FoodRecordResponse)
async def record_food_intake(
    request: FoodRecordRequest,
    db: Session = Depends(get_db)
):
    """
    사용자의 음식 섭취를 기록합니다.
    
    - **user_id**: 사용자 ID
    - **food_id**: 음식 ID
    - **serving_amount**: 섭취량 배수 (기본값: 1.0)
    """
    try:
        # 사용자 확인
        user = db.query(User).filter(User.user_id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        # 음식 정보 확인
        food = db.query(Food).filter(Food.food_id == request.food_id).first()
        if not food:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="음식을 찾을 수 없습니다."
            )
        
        # 섭취량에 따른 칼로리 및 영양소 계산
        calories = food.calories_kcal * request.serving_amount
        protein = food.protein_g * request.serving_amount
        fat = food.fat_g * request.serving_amount
        carbs = food.carbs_g * request.serving_amount
        
        # 현재 날짜의 총 칼로리 계산 (새 기록 추가 전)
        current_daily_calories = calculate_daily_calories(db, request.user_id)
        
        # 새 기록 추가 후의 총 칼로리
        new_daily_total = current_daily_calories + calories
        
        # 음식 섭취 기록 생성
        food_record = FoodRecord(
            user_id=request.user_id,
            daily_target_calories=float(user.daily_target_calories),
            daily_total_calories=new_daily_total,
            food_id=request.food_id,
            food_name=food.food,
            calories_kcal=calories,
            protein_g=protein,
            fat_g=fat,
            carbs_g=carbs
        )
        
        db.add(food_record)
        db.commit()
        db.refresh(food_record)
        
        # 응답 생성
        recorded_food = FoodInfo(
            food_id=food.food_id,
            food_name=food.food,
            serving_size=f"{request.serving_amount} x {food.serving_size}",
            calories=calories,
            nutrition=FoodNutrition(
                protein_g=protein,
                fat_g=fat,
                carbs_g=carbs
            )
        )
        
        return FoodRecordResponse(
            record_id=food_record.record_id,
            message=f"{food.food}이(가) 성공적으로 기록되었습니다.",
            daily_total_calories=new_daily_total,
            recorded_food=recorded_food
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"음식 기록 중 오류 발생: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"음식 기록 중 오류가 발생했습니다: {str(e)}"
        )