from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://user1:1user@localhost:3306/food_calorie_tracker"
    model_path: str = "../../best_food_model.pth"
    class_mapping_path: str = "../../class_mapping.json"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()