# KCali Backend API

AI 기반 음식 인식 칼로리 추적 서비스의 백엔드 API입니다.

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 데이터베이스 설정

```bash
# MySQL 데이터베이스 생성
mysql -u root -p
CREATE DATABASE food_calorie_tracker;
exit

# 테이블 생성 (자동으로 생성됨)
# 서버 실행 시 SQLAlchemy가 자동으로 테이블 생성

# 음식 데이터 초기화
python init_food_data.py
```

### 3. AI 모델 설정

```bash
# best_food_model.pth 파일을 back-end 디렉토리에 배치
# 파일이 없어도 서버는 실행되지만 더미 데이터로 작동
```

### 4. 서버 실행

```bash
python main.py
# 서버가 http://localhost:8000 에서 실행됩니다
```

## 📚 API 문서

Swagger UI: http://localhost:8000/docs

## 🔐 인증 방식

현재는 간단한 토큰 방식을 사용합니다:
- 로그인 시 `user_id`를 `access_token`으로 반환
- API 호출 시 `user_id`를 쿼리 파라미터로 전달

## 📋 API 엔드포인트 목록

### 1. 회원 관리

#### 회원가입
```http
POST /api/v1/users/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "password_check": "password123",
  "gender": "male",
  "age": 25,
  "height": 175,
  "weight": 70
}

Response: 200 OK
{
  "message": "회원가입이 완료되었습니다."
}
```

#### 로그인
```http
POST /api/v1/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access_token": "1",
  "user_id": 1
}
```

### 2. 음식 관리

#### 음식 사진 업로드 및 인식
```http
POST /api/v1/food/upload
Content-Type: multipart/form-data

file: [이미지 파일]

Response: 200 OK
{
  "food_name": "burger",
  "confidence": 0.95,
  "calories": 540,
  "serving_size": "1 sandwich (215 g)",
  "nutrition": {
    "protein_g": 29.0,
    "fat_g": 30.0,
    "carbs_g": 40.0
  },
  "message": "burger이(가) 95.0% 확률로 인식되었습니다."
}
```

#### 음식 검색
```http
GET /api/v1/food/search?q=김치&limit=10

Response: 200 OK
{
  "results": [
    {
      "food_id": 1,
      "food_name": "김치찌개",
      "serving_size": "1인분",
      "calories": 270,
      "nutrition": {
        "protein_g": 25.0,
        "fat_g": 15.0,
        "carbs_g": 8.0
      }
    }
  ],
  "total_count": 1,
  "query": "김치"
}
```

#### 음식 섭취 기록
```http
POST /api/v1/food/record
Content-Type: application/json

{
  "user_id": 1,
  "food_id": 1,
  "serving_amount": 1.5
}

Response: 200 OK
{
  "record_id": 1,
  "message": "burger이(가) 성공적으로 기록되었습니다.",
  "daily_total_calories": 810,
  "recorded_food": {
    "food_id": 1,
    "food_name": "burger",
    "serving_size": "1.5 x 1 sandwich (215 g)",
    "calories": 810,
    "nutrition": {
      "protein_g": 43.5,
      "fat_g": 45.0,
      "carbs_g": 60.0
    }
  }
}
```

### 3. 대시보드

#### 오늘의 섭취 현황
```http
GET /api/v1/dashboard/today?user_id=1

Response: 200 OK
{
  "date": "2025-07-29",
  "daily_target_calories": 2000,
  "consumed_calories": 810,
  "remaining_calories": 1190,
  "progress_percentage": 40.5,
  "meals": [
    {
      "record_id": 1,
      "time": "12:30",
      "food_name": "burger",
      "calories": 810
    }
  ]
}
```

#### 섭취 기록 조회
```http
GET /api/v1/dashboard/history?user_id=1&start_date=2025-07-23&end_date=2025-07-29

Response: 200 OK
{
  "records": [
    {
      "date": "2025-07-29",
      "total_calories": 810,
      "target_calories": 2000,
      "meals_count": 1
    }
  ],
  "start_date": "2025-07-23",
  "end_date": "2025-07-29"
}
```

## 🔧 개발 환경 설정

### 환경 변수
현재는 `config/settings.py`에 하드코딩되어 있습니다:
- DATABASE_URL: MySQL 연결 정보
- AI_MODEL_PATH: AI 모델 파일 경로

### 데이터베이스 설정
- Host: localhost
- Port: 3306
- User: user1
- Password: 1user
- Database: food_calorie_tracker

## 📁 프로젝트 구조

```
back-end/
├── api/                # API 엔드포인트
│   ├── auth.py        # 인증 관련 API
│   ├── food.py        # 음식 관련 API
│   └── dashboard.py   # 대시보드 API
├── models/            # SQLAlchemy 모델
├── schemas/           # Pydantic 스키마
├── services/          # 비즈니스 로직
├── utils/             # 유틸리티 함수
├── config/            # 설정 파일
└── main.py           # 애플리케이션 진입점
```

## ⚠️ 주의사항

1. **보안**
   - 현재 비밀번호가 평문으로 저장됩니다
   - 프로덕션 환경에서는 반드시 암호화 구현 필요

2. **데이터베이스**
   - 트리거와 프로시저가 있다면 제거 필요:
   ```sql
   DROP TRIGGER IF EXISTS before_food_record_insert;
   DROP PROCEDURE IF EXISTS register_user;
   ```

3. **AI 모델**
   - `best_food_model.pth` 파일이 없으면 랜덤 예측
   - 19개 음식 카테고리만 지원

4. **이미지 업로드**
   - 최대 파일 크기: 10MB
   - 지원 형식: JPEG, PNG

## 🧪 테스트

```bash
# Swagger UI에서 테스트
http://localhost:8000/docs

# 또는 curl 사용
curl -X POST http://localhost:8000/api/v1/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123"}'
```

## 📞 문제 해결

### 서버가 시작되지 않는 경우
1. Python 버전 확인 (3.8 이상)
2. 의존성 재설치: `pip install -r requirements.txt`
3. MySQL 서버 실행 확인

### 데이터베이스 연결 오류
1. MySQL 서버 실행 상태 확인
2. 데이터베이스 생성 확인
3. `config/settings.py`의 연결 정보 확인

### AI 모델 오류
1. PyTorch 설치 확인
2. 모델 파일 경로 확인
3. 메모리 부족 시 더 작은 배치 크기 사용

## 🤝 프론트엔드 연동 가이드

1. **CORS 설정**
   - 현재 `http://localhost:5173` 허용
   - 필요시 `main.py`에서 수정

2. **인증 처리**
   - 로그인 후 받은 `user_id`를 저장
   - API 호출 시 쿼리 파라미터로 전달

3. **이미지 업로드**
   - FormData 사용
   - 'file' 필드명으로 전송

4. **에러 처리**
   - 모든 에러는 JSON 형식
   - `detail` 필드에 에러 메시지

예시 코드 (JavaScript):
```javascript
// 로그인
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/api/v1/users/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('userId', data.user_id);
  return data;
};

// 음식 업로드
const uploadFood = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/food/upload', {
    method: 'POST',
    body: formData
  });
  return await response.json();
};

// 대시보드 조회
const getDashboard = async () => {
  const userId = localStorage.getItem('userId');
  const response = await fetch(`http://localhost:8000/api/v1/dashboard/today?user_id=${userId}`);
  return await response.json();
};
```