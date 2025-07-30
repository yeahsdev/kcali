#!/usr/bin/env python3
"""
음식 데이터 초기화 스크립트
CSV 파일에서 음식 데이터를 읽어 데이터베이스에 로드합니다.
"""

import csv
import os
import sys
from pathlib import Path

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(str(Path(__file__).parent))

from database.connection import engine, Base, SessionLocal
from models.food import Food
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_food_data():
    """CSV 파일에서 음식 데이터를 로드하여 데이터베이스에 저장"""
    
    # CSV 파일 경로
    csv_path = Path(__file__).parent.parent / "docs-for-dev" / "food_nutrition.csv"
    
    if not csv_path.exists():
        logger.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        return
    
    # 데이터베이스 세션 생성
    db = SessionLocal()
    
    try:
        # 테이블 생성
        Base.metadata.create_all(bind=engine)
        
        # 기존 데이터 삭제 (선택사항)
        existing_count = db.query(Food).count()
        if existing_count > 0:
            logger.info(f"기존 데이터 {existing_count}개가 있습니다.")
            response = input("기존 데이터를 삭제하고 새로 로드하시겠습니까? (y/N): ")
            if response.lower() == 'y':
                db.query(Food).delete()
                db.commit()
                logger.info("기존 데이터를 삭제했습니다.")
            else:
                logger.info("기존 데이터를 유지합니다.")
                return
        
        # CSV 파일 읽기 및 데이터 로드
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            count = 0
            
            for row in csv_reader:
                try:
                    # 데이터베이스에 음식 추가
                    food_item = Food(
                        food=row['food'],
                        serving_size=row['serving_size'],
                        calories_kcal=float(row['calories_kcal']),
                        protein_g=float(row['protein_g']),
                        fat_g=float(row['fat_g']),
                        carbs_g=float(row['carbs_g'])
                    )
                    
                    db.add(food_item)
                    count += 1
                    
                    # 10개마다 커밋
                    if count % 10 == 0:
                        db.commit()
                        logger.info(f"{count}개 항목 로드됨...")
                        
                except Exception as e:
                    logger.error(f"항목 로드 실패 ({row['food']}): {str(e)}")
                    continue
            
            # 마지막 커밋
            db.commit()
            logger.info(f"총 {count}개의 음식 데이터를 성공적으로 로드했습니다.")
            
    except Exception as e:
        logger.error(f"데이터 로드 중 오류 발생: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    logger.info("음식 데이터 초기화를 시작합니다...")
    load_food_data()
    logger.info("음식 데이터 초기화가 완료되었습니다.")