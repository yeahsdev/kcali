from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import mysql.connector

# CORS를 위한 미들웨어 추가
from fastapi.middleware.cors import CORSMiddleware

# --- 보안 설정 ---
SECRET_KEY = "your-super-secret-key-that-no-one-should-know"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 데이터베이스 설정 ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'intel1234',
    'database': 'food_calorie_tracker'
}

# FastAPI 앱 인스턴스
app = FastAPI()

# --- CORS 미들웨어 설정 ---
# 프론트엔드 개발 환경의 주소 (예: http://localhost:3000)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080", # 필요한 다른 프론트엔드 주소 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 모든 메소드 허용
    allow_headers=["*"], # 모든 헤더 허용
)

# --- 데이터베이스 모델 ---
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    password: str

# --- 유틸리티 함수 ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(email: str) -> UserInDB | None:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT email, full_name, password, disabled FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_data = cursor.fetchone()
        if user_data:
            return UserInDB(
                email=user_data[0],
                full_name=user_data[1],
                password=user_data[2],
                disabled=bool(user_data[3])
            )
        return None
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """토큰을 디코딩하여 현재 사용자를 식별합니다."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user

# --- API 엔드포인트 ---
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    인증된 현재 사용자의 정보를 반환합니다.
    이 엔드포인트를 호출하려면 HTTP Header에 'Authorization: Bearer <토큰>'이 필요합니다.
    """
    return current_user