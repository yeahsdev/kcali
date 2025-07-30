# 하드코딩된 설정값
DATABASE_URL = "mysql+pymysql://user1:1user@localhost:3306/food_calorie_tracker"
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "user1"
DB_PASSWORD = "1user"
DB_NAME = "food_calorie_tracker"

# 애플리케이션 설정
PORT = 8000
DEBUG = True

# JWT 설정
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# AI 모델 설정
AI_MODEL_PATH = "best_food_model.pth"  # 모델 파일 경로
AI_MODEL_URL = "http://localhost:8001/predict"  # 외부 AI 서버 (사용하지 않음)
AI_MODEL_TIMEOUT = 30

# 업로드 설정
MAX_UPLOAD_SIZE = 10485760  # 10MB
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png", "webp"]