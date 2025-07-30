# Food_records 테이블 모델
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.connection import Base

class FoodRecord(Base):
    __tablename__ = "food_records"
    
    record_id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    daily_target_calories = Column(Float, nullable=False)
    daily_total_calories = Column(Float, default=0)
    food_id = Column(Integer, ForeignKey("food.food_id"), nullable=False)
    food_name = Column(String(100), nullable=False)
    calories_kcal = Column(Float, nullable=False)
    protein_g = Column(Float, default=0)
    fat_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)
    
    # 관계 설정
    user = relationship("User", back_populates="food_records")
    food = relationship("Food")