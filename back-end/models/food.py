from sqlalchemy import Column, Integer, String, Float
from database import Base

class Food(Base):
    __tablename__ = "food"
    
    food_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    food = Column(String(100), unique=True, nullable=False, index=True)
    serving_size = Column(String(50), nullable=False)
    calories_kcal = Column(Float, nullable=False)
    protein_g = Column(Float, default=0)
    fat_g = Column(Float, default=0)
    carbs_g = Column(Float, default=0)