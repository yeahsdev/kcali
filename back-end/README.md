# KCali Backend API Documentation

## 개요
KCali 백엔드 서버는 FastAPI로 구축된 RESTful API 서버입니다. 음식 사진 AI 분석, 식단 기록 관리, 사용자 인증 등의 기능을 제공합니다.

## 기술 스택
- **Framework**: FastAPI
- **Database**: MySQL
- **AI Model**: PyTorch (ResNet18)
- **Authentication**: 간단한 Bearer Token (user_id 기반)

## 설치 및 실행

### 1. 필수 요구사항
- Python 3.8+
- MySQL 서버 (localhost:3306)
- MySQL 계정: user1 / 1user

### 2. 패키지 설치
```bash
cd back-end
pip install -r requirements.txt
```

### 3. 데이터베이스 설정
- MySQL에 `food_calorie_tracker` 데이터베이스가 필요합니다
- `database.md` 파일의 SQL 스크립트를 실행하여 테이블을 생성하세요

### 4. 서버 실행
```bash
python main.py
```
서버는 `http://localhost:8000`에서 실행됩니다.

## API 문서
Swagger UI: `http://localhost:8000/docs`

## 구현된 API 엔드포인트

### 🍔 음식 및 식단 기록 API (Food & Log API)

#### 1. 특정 날짜의 식단 기록 조회
- **Method**: `GET`
- **Endpoint**: `/api/v1/foods/logs/{YYYY}/{MM}/{DD}/`
- **Authentication**: Required (Bearer token)
- **Headers**: 
  ```
  Authorization: Bearer {user_id}
  ```
- **URL Parameters**:
  - `YYYY`: 년도 (예: 2025)
  - `MM`: 월 (예: 07)
  - `DD`: 일 (예: 28)
- **Success Response (200 OK)**:
  ```json
  {
    "date": "2025-07-28",
    "goal_kcal": 2000,
    "consumed_kcal": 360,
    "food_logs": [
      {
        "id": 1,
        "name": "계란 후라이",
        "kcal": 180
      },
      {
        "id": 2,
        "name": "닭가슴살 샐러드",
        "kcal": 180
      }
    ]
  }
  ```

#### 2. 음식 사진 분석 및 기록
- **Method**: `POST`
- **Endpoint**: `/api/v1/foods/analyze/`
- **Authentication**: Required (Bearer token)
- **Headers**: 
  ```
  Authorization: Bearer {user_id}
  ```
- **Request Body**: `multipart/form-data`
  - `image`: 음식 사진 파일 (jpg, png 등)
- **Success Response (201 Created)**:
  ```json
  {
    "message": "성공적으로 기록되었습니다.",
    "added_food": {
      "name": "고구마 맛탕",
      "kcal": 250
    },
    "updated_consumed_kcal": 610
  }
  ```

### 👤 사용자 인증 API

#### 1. 회원가입
- **Method**: `POST`
- **Endpoint**: `/api/v1/users/signup/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "password_check": "password123",
    "gender": "male",
    "age": 29,
    "height": 175,
    "weight": 70
  }
  ```
- **Success Response (201 Created)**:
  ```json
  {
    "message": "회원가입이 성공적으로 완료되었습니다.",
    "user": {
      "email": "user@example.com"
    }
  }
  ```

#### 2. 로그인
- **Method**: `POST`
- **Endpoint**: `/api/v1/users/login/`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "message": "로그인 성공",
    "user_id": 1
  }
  ```

## 프론트엔드 연동 가이드

### 1. 인증 방식
- 로그인 성공 시 받은 `user_id`를 저장합니다
- API 요청 시 Authorization 헤더에 `Bearer {user_id}` 형식으로 전달합니다
- 예시:
  ```javascript
  const response = await fetch('http://localhost:8000/api/v1/foods/logs/2025/07/28/', {
    headers: {
      'Authorization': `Bearer ${userId}`
    }
  });
  ```

### 2. 음식 사진 업로드 예시
```javascript
const formData = new FormData();
formData.append('image', imageFile);

const response = await fetch('http://localhost:8000/api/v1/foods/analyze/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userId}`
  },
  body: formData
});
```

### 3. CORS 설정
백엔드 서버는 모든 origin에서의 요청을 허용하도록 설정되어 있습니다.

## 주의사항

### 보안 관련
⚠️ **현재 구현은 개발 환경용입니다**
- 비밀번호가 평문으로 저장됩니다
- 인증 토큰이 단순 user_id입니다
- 프로덕션 환경에서는 반드시 보안을 강화해야 합니다

### AI 모델
- AI 모델 파일(`best_food_model.pth`)이 필요합니다
- 음식 클래스 매핑 파일(`class_mapping.json`)이 필요합니다
- 현재 34개의 음식 카테고리를 인식할 수 있습니다

#### 인식 가능한 음식 목록
1. apple_pie (애플파이)
2. Baked Potato (구운 감자)
3. burger (버거)
4. butter_naan (버터 난)
5. chai (차이)
6. chapati (차파티)
7. cheesecake (치즈케이크)
8. chicken_curry (치킨 커리)
9. chole_bhature (촐레 바투레)
10. Crispy Chicken (크리스피 치킨)
11. dal_makhani (달 마카니)
12. dhokla (도클라)
13. Donut (도넛)
14. fried_rice (볶음밥)
15. Fries (감자튀김)
16. Hot Dog (핫도그)
17. ice_cream (아이스크림)
18. idli (이들리)
19. jalebi (잘레비)
20. kaathi_rolls (카티 롤)
21. kadai_paneer (카다이 파니르)
22. kulfi (쿨피)
23. masala_dosa (마살라 도사)
24. momos (모모)
25. omelette (오믈렛)
26. paani_puri (파니 푸리)
27. pakode (파코데)
28. pav_bhaji (파브 바지)
29. pizza (피자)
30. samosa (사모사)
31. Sandwich (샌드위치)
32. sushi (스시)
33. Taco (타코)
34. Taquito (타키토)

### 데이터베이스
- 음식 영양 정보는 `food` 테이블에 미리 저장되어 있어야 합니다 (완료)
- `food_nutrition.csv` 파일을 데이터베이스에 임포트해야 합니다 (완료)

1. 서버 실행 테스트

  기본 실행 테스트

  cd /Users/baejaemyeong/Desktop/coding/INTEL-APP/kcali_2025-07-28/kcali/back-end
  python main.py

  임포트 테스트 (서버 실행 전 확인)

  python -c "from main import app; print('✅ 서버 임포트 성공')"

  2. API 엔드포인트 테스트

  서버가 실행된 후 다른 터미널에서:

  기본 헬스체크

  curl http://localhost:8000/
  curl http://localhost:8000/health

  회원가입 테스트

  curl -X POST "http://localhost:8000/api/v1/users/signup/" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@example.com",
      "password": "test123",
      "password_check": "test123",
      "gender": "male",
      "age": 25,
      "height": 175,
      "weight": 70
    }'

  로그인 테스트

  curl -X POST "http://localhost:8000/api/v1/users/login/" \
    -H "Content-Type: application/json" \
    -d '{
      "email": "test@example.com",
      "password": "test123"
    }'

  식단 조회 테스트 (로그인 후 user_id 사용)

  curl -X GET "http://localhost:8000/api/v1/foods/logs/2025/07/29/" \
    -H "Authorization: Bearer 1"

  3. 데이터베이스 연결 테스트

  python -c "
  import pymysql
  try:
      conn = pymysql.connect(host='localhost', port=3306, user='user1', password='1user', database='food_calorie_tracker')
      print('✅ 데이터베이스 연결 성공')
      conn.close()
  except Exception as e:
      print(f'❌ 데이터베이스 연결 실패: {e}')
  "

  4. Swagger UI 테스트

  서버 실행 후 브라우저에서:
  - http://localhost:8000/docs - Swagger UI
  - http://localhost:8000/redoc - ReDoc

  5. 문제 해결

  자주 발생하는 문제들:

  패키지 누락

  pip install -r requirements.txt

  데이터베이스 연결 실패

  - MySQL 서버가 실행 중인지 확인
  - user1/1user 계정 존재 확인
  - food_calorie_tracker 데이터베이스 존재 확인

  포트 충돌

  # 8000 포트 사용 중인 프로세스 확인
  lsof -i :8000
  # 또는 다른 포트로 실행
  python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8001)"

  ---
  # Swagger UI로 API 테스트하는 방법 (처음부터 끝까지)

  1. 서버 실행하기

  터미널에서:
  cd /Users/baejaemyeong/Desktop/coding/INTEL-APP/kcali_2025-07-28/kcali/back-end
  python main.py

  서버가 실행되면 이런 메시지가 나옵니다:
  INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

  2. Swagger UI 접속

  브라우저에서:
  http://localhost:8000/docs

  3. 회원가입하기

  3-1. 회원가입 API 찾기

  - POST /api/v1/users/signup/ 섹션을 찾습니다
  - 초록색 "POST" 버튼을 클릭합니다

  3-2. 회원가입 실행

  1. "Try it out" 버튼 클릭
  2. Request body에 다음 내용 입력:
  {
    "email": "test@example.com",
    "password": "test123",
    "password_check": "test123",
    "gender": "male",
    "age": 25,
    "height": 175,
    "weight": 70
  }
  3. "Execute" 버튼 클릭
  4. 응답 확인:
  {
    "message": "회원가입이 성공적으로 완료되었습니다.",
    "user": {
      "email": "test@example.com"
    }
  }

  4. 로그인하기

  4-1. 로그인 API 찾기

  - POST /api/v1/users/login/ 섹션을 찾습니다
  - 초록색 "POST" 버튼을 클릭합니다

  4-2. 로그인 실행

  1. "Try it out" 버튼 클릭
  2. Request body에 다음 내용 입력:
  {
    "email": "test@example.com",
    "password": "test123"
  }
  3. "Execute" 버튼 클릭
  4. 응답에서 user_id 값을 복사해둡니다:
  {
    "message": "로그인 성공",
    "user_id": 1
  }
  4. → user_id: 1 이 값을 기억해두세요!

  5. 식단 기록 조회하기

  5-1. 식단 조회 API 찾기

  - GET /api/v1/foods/logs/{year}/{month}/{day}/ 섹션을 찾습니다
  - 파란색 "GET" 버튼을 클릭합니다

  5-2. 인증 정보 입력

  1. "Try it out" 버튼 클릭
  2. Parameters 섹션에서:
    - year: 2025
    - month: 7
    - day: 29
    - user_id (query): 1 (로그인에서 받은 user_id)
    - 또는 x-user-id (header): 1 (둘 중 하나만 입력)

  5-3. 실행

  1. "Execute" 버튼 클릭
  2. 응답 확인:
  {
    "date": "2025-07-29",
    "goal_kcal": 2000,
    "consumed_kcal": 0,
    "food_logs": []
  }

  6. 음식 사진 분석하기

  6-1. 음식 분석 API 찾기

  - POST /api/v1/foods/analyze/ 섹션을 찾습니다
  - 초록색 "POST" 버튼을 클릭합니다

  6-2. 이미지 업로드

  1. "Try it out" 버튼 클릭
  2. Parameters 섹션에서:
    - user_id (query): 1 (로그인에서 받은 user_id)
    - 또는 x-user-id (header): 1
  3. Request body 섹션에서:
    - image: "Choose File" 버튼을 클릭해서 음식 사진 선택

  6-3. 실행

  1. "Execute" 버튼 클릭
  2. 응답 확인:
  {
    "message": "성공적으로 기록되었습니다.",
    "added_food": {
      "name": "pizza",
      "kcal": 285
    },
    "updated_consumed_kcal": 285
  }

  7. 다시 식단 조회하기

  음식을 추가한 후 다시 5번 과정을 반복하면:
  {
    "date": "2025-07-29",
    "goal_kcal": 2000,
    "consumed_kcal": 285,
    "food_logs": [
      {
        "id": 1,
        "name": "pizza",
        "kcal": 285
      }
    ]
  }

  💡 주요 팁

  1. user_id는 꼭 기억하세요 - 로그인 후 받은 숫자
  2. query 또는 header 둘 중 하나만 user_id 입력
  3. 이미지는 음식 사진이어야 AI가 인식 가능
  4. 각 단계마다 응답 코드가 200이나 201이면 성공

  이 순서대로 하면 모든 API를 Swagger UI에서 테스트할 수 있습니다!