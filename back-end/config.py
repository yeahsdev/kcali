from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "user1"
    db_password: str = "1user"
    db_name: str = "food_calorie_tracker"
    
    # AI Model settings
    model_path: str = "../../best_food_model.pth"
    class_mapping_path: str = "../../class_mapping.json"
    
    class Config:
        env_file = ".env"
    
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

@lru_cache()
def get_settings():
    return Settings()