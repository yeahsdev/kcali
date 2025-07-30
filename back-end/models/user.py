from sqlalchemy import Column, Integer, String, Enum, DECIMAL
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    gender = Column(Enum('M', 'F'), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(DECIMAL(5, 2), nullable=False)
    weight = Column(DECIMAL(5, 2), nullable=False)
    daily_target_calories = Column(DECIMAL(7, 2), nullable=False)
    
    # 관계 설정
    food_records = relationship("FoodRecord", back_populates="user")