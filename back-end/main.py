from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging


# 설정값 임포트
from config.settings import PORT
# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# 라우터 임포트 (나중에 추가할 예정)
# from api import auth, food, dashboard
# from database.connection import engine, Base
# 앱 생명주기 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행
    logger.info("Starting up the application...")
    # 데이터베이스 테이블 생성 (나중에 추가)
    # Base.metadata.create_all(bind=engine)
    yield
    # 종료 시 실행
    logger.info("Shutting down the application...")
# FastAPI 인스턴스 생성
app = FastAPI(
    title="Food Calorie Tracker API",
    description="음식 사진으로 칼로리를 계산하고 일일 섭취량을 관리하는 API",
    version="1.0.0",
    lifespan=lifespan
)
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 에러 핸들러
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
# 기본 라우트
@app.get("/")
async def root():
    return {
        "message": "Food Calorie Tracker API",
        "version": "1.0.0",
        "status": "running"
    }
# 헬스체크 엔드포인트
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"  # 나중에 실제 DB 연결 체크로 변경
    }
# API 라우터 등록 (나중에 추가)
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(food.router, prefix="/api/food", tags=["Food"])
# app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
# 개발 서버 실행을 위한 코드
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )