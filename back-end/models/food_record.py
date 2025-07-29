from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class FoodRecord(Base):
    __tablename__ = "food_records"
    
    record_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    daily_target_calories = Column(Float, nullable=False)
    daily_total_calories = Column(Float, default=0)
    food_id = Column(Integer, ForeignKey("food.food_id", onupdate="CASCADE"), nullable=False)
    food_name = Column(String(100), nullable=False, index=True)
    calories_kcal = Column(Float, nullable=False)
    protein_g = Column(Float, default=0)
    fat_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)