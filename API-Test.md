# KCali API 테스트 가이드

## 🚀 테스트 환경 설정

### 1. 필수 준비사항

```bash
# 1. MySQL 서버 실행
# 2. 데이터베이스 생성 (최초 1회)
mysql -u root -p
CREATE DATABASE IF NOT EXISTS food_calorie_tracker;
exit

# 3. Python 가상환경 활성화
cd back-end
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows

# 4. 의존성 설치 (최초 1회)
pip install -r requirements.txt

# 6. AI 모델 파일 준비 (선택사항)
# best_food_model.pth 파일을 back-end 디렉토리에 복사
# 없어도 서비스는 작동하지만 정확도가 낮음

# 7. 서버 실행
python main.py
```

### 2. 테스트 도구

- **Swagger UI**: http://localhost:8000/docs (가장 쉬움)
- **cURL**: 터미널에서 직접 테스트
- **Postman**: GUI 기반 테스트
- **Python**: requests 라이브러리 사용

## 🌟 Swagger UI 테스트 가이드 (권장)

Swagger UI는 브라우저에서 API를 테스트할 수 있는 가장 쉬운 방법입니다.

### Swagger UI 접속
1. 서버 실행 후 브라우저에서 http://localhost:8000/docs 접속
2. 모든 API 엔드포인트가 카테고리별로 정리되어 표시됨

### 테스트 순서 (전체 플로우)

#### 1️⃣ 회원가입 테스트
1. **Authentication** 섹션에서 `POST /api/v1/users/signup/` 클릭
2. **Try it out** 버튼 클릭
3. Request body 예시 수정:
   ```json
   {
     "email": "swagger@test.com",
     "password": "test1234",
     "password_check": "test1234",
     "gender": "male",
     "age": 25,
     "height": 175,
     "weight": 70
   }
   ```
4. **Execute** 버튼 클릭
5. Response에서 "회원가입이 완료되었습니다." 확인

#### 2️⃣ 로그인 테스트
1. `POST /api/v1/users/login/` 클릭
2. **Try it out** 버튼 클릭
3. Request body 입력:
   ```json
   {
     "email": "swagger@test.com",
     "password": "test1234"
   }
   ```
4. **Execute** 버튼 클릭
5. Response에서 `user_id` 값 복사 (예: 1)
   - 이 값을 메모해두세요! 다른 API에서 사용합니다.

#### 3️⃣ 음식 검색 테스트
1. **Food** 섹션에서 `GET /api/v1/food/search` 클릭
2. **Try it out** 버튼 클릭
3. Parameters 입력:
   - `q`: burger (검색어)
   - `limit`: 10 (선택사항)
4. **Execute** 버튼 클릭
5. 검색 결과에서 `food_id` 확인 (예: burger의 food_id = 3)

#### 4️⃣ 음식 사진 업로드 테스트
1. `POST /api/v1/food/upload` 클릭
2. **Try it out** 버튼 클릭
3. **Choose File** 버튼 클릭하여 이미지 선택
   - 아무 음식 사진이나 선택 (JPEG/PNG)
   - 테스트 이미지가 없다면 인터넷에서 음식 사진 다운로드
4. **Execute** 버튼 클릭
5. AI가 인식한 음식명과 칼로리 확인

#### 5️⃣ 음식 섭취 기록 테스트
1. `POST /api/v1/food/record` 클릭
2. **Try it out** 버튼 클릭
3. Request body 입력:
   ```json
   {
     "user_id": 1,      // 로그인에서 받은 user_id
     "food_id": 3,      // 검색에서 찾은 food_id
     "serving_amount": 1.5
   }
   ```
4. **Execute** 버튼 클릭
5. 기록 성공 메시지와 일일 총 칼로리 확인

#### 6️⃣ 대시보드 확인
1. **Dashboard** 섹션에서 `GET /api/v1/dashboard/today` 클릭
2. **Try it out** 버튼 클릭
3. Parameters 입력:
   - `user_id`: 1 (로그인에서 받은 값)
4. **Execute** 버튼 클릭
5. 오늘의 섭취 현황 확인:
   - 목표 칼로리
   - 섭취한 칼로리
   - 진행률
   - 먹은 음식 목록

#### 7️⃣ 기록 히스토리 조회
1. `GET /api/v1/dashboard/history` 클릭
2. **Try it out** 버튼 클릭
3. Parameters 입력:
   - `user_id`: 1
   - `start_date`: (비워두면 7일 전부터)
   - `end_date`: (비워두면 오늘까지)
4. **Execute** 버튼 클릭
5. 날짜별 섭취 기록 확인

### Swagger UI 팁

#### 🎯 Response 확인하기
- **Code**: HTTP 상태 코드 (200 = 성공)
- **Response body**: JSON 형식의 응답 데이터
- **Response headers**: 응답 헤더 정보

#### 🎨 Response 예시 미리보기
- 각 API의 **Responses** 섹션에서 예상 응답 형식 확인 가능
- **Schema** 탭에서 데이터 구조 확인

#### 🔍 에러 처리 확인
- 잘못된 데이터로 테스트하여 에러 메시지 확인
- 예: 중복 이메일로 회원가입, 잘못된 비밀번호로 로그인

#### 📋 데이터 복사하기
- Response body의 JSON을 클릭하면 전체 선택
- Ctrl+C (Cmd+C)로 복사하여 다른 곳에서 사용

### Swagger UI 장점
- ✅ 설치 불필요 (브라우저만 있으면 OK)
- ✅ 실시간 API 문서
- ✅ 파일 업로드 쉬움
- ✅ 자동 완성 기능
- ✅ 응답 예시 제공

## 📋 API 엔드포인트 테스트

### 1. 회원가입 API

#### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/users/signup/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "password_check": "password123",
    "gender": "male",
    "age": 25,
    "height": 175,
    "weight": 70
  }'
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/users/signup/"
data = {
    "email": "test@example.com",
    "password": "password123",
    "password_check": "password123",
    "gender": "male",
    "age": 25,
    "height": 175,
    "weight": 70
}

response = requests.post(url, json=data)
print(response.json())
```

#### 예상 응답
```json
{
  "message": "회원가입이 완료되었습니다."
}
```

#### 에러 케이스
- 이메일 중복: 400 Bad Request
- 비밀번호 불일치: 400 Bad Request

---

### 2. 로그인 API

#### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/users/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/users/login/"
data = {
    "email": "test@example.com",
    "password": "password123"
}

response = requests.post(url, json=data)
result = response.json()
print(f"User ID: {result['user_id']}")
print(f"Token: {result['access_token']}")

# user_id 저장 (이후 API에서 사용)
USER_ID = result['user_id']
```

#### 예상 응답
```json
{
  "access_token": "1",
  "user_id": 1
}
```

---

### 3. 음식 사진 업로드 및 인식 API

#### cURL
```bash
# 테스트 이미지가 필요합니다
curl -X POST "http://localhost:8000/api/v1/food/upload" \
  -F "file=@/path/to/food_image.jpg"
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/food/upload"

# 테스트 이미지 파일 준비
with open('food_image.jpg', 'rb') as f:
    files = {'file': ('food.jpg', f, 'image/jpeg')}
    response = requests.post(url, files=files)
    
result = response.json()
print(f"음식명: {result['food_name']}")
print(f"칼로리: {result['calories']}")
print(f"신뢰도: {result['confidence']}")
```

#### 예상 응답
```json
{
  "food_name": "burger",
  "confidence": 0.95,
  "calories": 540.0,
  "serving_size": "1 sandwich (215 g)",
  "nutrition": {
    "protein_g": 29.0,
    "fat_g": 30.0,
    "carbs_g": 40.0
  },
  "message": "burger이(가) 95.0% 확률로 인식되었습니다."
}
```

#### 테스트 이미지 생성 (임시)
```python
# 테스트용 더미 이미지 생성
from PIL import Image

img = Image.new('RGB', (100, 100), color='red')
img.save('test_food.jpg')
```

---

### 4. 음식 검색 API

#### cURL
```bash
# 김치로 검색
curl -X GET "http://localhost:8000/api/v1/food/search?q=김치&limit=5"

# burger로 검색
curl -X GET "http://localhost:8000/api/v1/food/search?q=burger"
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/food/search"
params = {
    "q": "chicken",
    "limit": 10
}

response = requests.get(url, params=params)
result = response.json()

print(f"검색 결과: {result['total_count']}개")
for food in result['results']:
    print(f"- {food['food_name']}: {food['calories']} kcal")
```

#### 예상 응답
```json
{
  "results": [
    {
      "food_id": 11,
      "food_name": "Crispy Chicken",
      "serving_size": "2 pieces (150 g)",
      "calories": 380.0,
      "nutrition": {
        "protein_g": 28.0,
        "fat_g": 22.0,
        "carbs_g": 16.0
      }
    },
    {
      "food_id": 9,
      "food_name": "chicken_curry",
      "serving_size": "1 cup (200 g)",
      "calories": 270.0,
      "nutrition": {
        "protein_g": 25.0,
        "fat_g": 15.0,
        "carbs_g": 8.0
      }
    }
  ],
  "total_count": 2,
  "query": "chicken"
}
```

---

### 5. 음식 섭취 기록 API

#### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/food/record" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "food_id": 3,
    "serving_amount": 1.5
  }'
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/food/record"
data = {
    "user_id": USER_ID,  # 로그인에서 받은 user_id
    "food_id": 3,        # burger의 food_id
    "serving_amount": 1.5 # 1.5인분
}

response = requests.post(url, json=data)
result = response.json()

print(f"기록 ID: {result['record_id']}")
print(f"오늘 총 칼로리: {result['daily_total_calories']}")
```

#### 예상 응답
```json
{
  "record_id": 1,
  "message": "burger이(가) 성공적으로 기록되었습니다.",
  "daily_total_calories": 810.0,
  "recorded_food": {
    "food_id": 3,
    "food_name": "burger",
    "serving_size": "1.5 x 1 sandwich (215 g)",
    "calories": 810.0,
    "nutrition": {
      "protein_g": 43.5,
      "fat_g": 45.0,
      "carbs_g": 60.0
    }
  }
}
```

---

### 6. 오늘의 섭취 현황 API

#### cURL
```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/today?user_id=1"
```

#### Python
```python
import requests

url = "http://localhost:8000/api/v1/dashboard/today"
params = {"user_id": USER_ID}

response = requests.get(url, params=params)
result = response.json()

print(f"날짜: {result['date']}")
print(f"목표 칼로리: {result['daily_target_calories']}")
print(f"섭취 칼로리: {result['consumed_calories']}")
print(f"남은 칼로리: {result['remaining_calories']}")
print(f"진행률: {result['progress_percentage']}%")
print("\n오늘 먹은 음식:")
for meal in result['meals']:
    print(f"- {meal['time']} {meal['food_name']}: {meal['calories']} kcal")
```

#### 예상 응답
```json
{
  "date": "2025-07-29",
  "daily_target_calories": 2418.5,
  "consumed_calories": 810.0,
  "remaining_calories": 1608.5,
  "progress_percentage": 33.5,
  "meals": [
    {
      "record_id": 1,
      "time": "14:30",
      "food_name": "burger",
      "calories": 810.0
    }
  ]
}
```

---

### 7. 섭취 기록 조회 API

#### cURL
```bash
# 최근 7일
curl -X GET "http://localhost:8000/api/v1/dashboard/history?user_id=1"

# 특정 기간
curl -X GET "http://localhost:8000/api/v1/dashboard/history?user_id=1&start_date=2025-07-20&end_date=2025-07-29"
```

#### Python
```python
import requests
from datetime import datetime, timedelta

url = "http://localhost:8000/api/v1/dashboard/history"
params = {
    "user_id": USER_ID,
    "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
    "end_date": datetime.now().strftime("%Y-%m-%d")
}

response = requests.get(url, params=params)
result = response.json()

print(f"기간: {result['start_date']} ~ {result['end_date']}")
for record in result['records']:
    print(f"- {record['date']}: {record['total_calories']} kcal (목표: {record['target_calories']})")
```

#### 예상 응답
```json
{
  "records": [
    {
      "date": "2025-07-29",
      "total_calories": 810.0,
      "target_calories": 2418.5,
      "meals_count": 1
    }
  ],
  "start_date": "2025-07-23",
  "end_date": "2025-07-29"
}
```

## 🔄 전체 플로우 테스트

```python
import requests
import time

BASE_URL = "http://localhost:8000"

# 1. 회원가입
signup_data = {
    "email": f"test_{int(time.time())}@example.com",
    "password": "test123",
    "password_check": "test123",
    "gender": "female",
    "age": 30,
    "height": 165,
    "weight": 55
}
response = requests.post(f"{BASE_URL}/api/v1/users/signup/", json=signup_data)
print("1. 회원가입:", response.json())

# 2. 로그인
login_data = {
    "email": signup_data["email"],
    "password": signup_data["password"]
}
response = requests.post(f"{BASE_URL}/api/v1/users/login/", json=login_data)
login_result = response.json()
user_id = login_result["user_id"]
print("2. 로그인:", login_result)

# 3. 음식 검색
response = requests.get(f"{BASE_URL}/api/v1/food/search?q=burger")
search_result = response.json()
food_id = search_result["results"][0]["food_id"] if search_result["results"] else None
print("3. 음식 검색:", search_result["total_count"], "개 발견")

# 4. 음식 기록
if food_id:
    record_data = {
        "user_id": user_id,
        "food_id": food_id,
        "serving_amount": 1.0
    }
    response = requests.post(f"{BASE_URL}/api/v1/food/record", json=record_data)
    print("4. 음식 기록:", response.json()["message"])

# 5. 대시보드 확인
response = requests.get(f"{BASE_URL}/api/v1/dashboard/today?user_id={user_id}")
dashboard = response.json()
print("5. 오늘의 현황:")
print(f"   - 목표: {dashboard['daily_target_calories']} kcal")
print(f"   - 섭취: {dashboard['consumed_calories']} kcal")
print(f"   - 진행률: {dashboard['progress_percentage']}%")
```

## 🐛 문제 해결

### 1. 서버가 시작되지 않음
```bash
# Python 버전 확인 (3.8 이상 필요)
python --version

# MySQL 연결 확인
mysql -u user1 -p1user -h localhost
```

### 2. 이미지 업로드 실패
- 파일 크기 확인 (최대 10MB)
- 파일 형식 확인 (JPEG, PNG만 지원)
- Content-Type 헤더 제거 (multipart/form-data 자동 설정)

### 3. 음식이 인식되지 않음
- AI 모델 파일 위치 확인: `/back-end/best_food_model.pth`
- 지원되는 음식 카테고리 확인 (19개)
- 로그 확인: 콘솔에서 경고 메시지 확인

### 4. 데이터베이스 오류
```bash
# 테이블 존재 확인
mysql -u user1 -p1user food_calorie_tracker -e "SHOW TABLES;"

# 음식 데이터 확인
mysql -u user1 -p1user food_calorie_tracker -e "SELECT COUNT(*) FROM food;"

# 데이터 재초기화
python init_food_data.py
```

## 📊 Postman Collection

Postman에서 Import → Raw text → 아래 JSON 붙여넣기:

```json
{
  "info": {
    "name": "KCali API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Signup",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\",\n  \"password_check\": \"password123\",\n  \"gender\": \"male\",\n  \"age\": 25,\n  \"height\": 175,\n  \"weight\": 70\n}"
        },
        "url": "{{base_url}}/api/v1/users/signup/"
      }
    },
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"test@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": "{{base_url}}/api/v1/users/login/"
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000",
      "type": "string"
    }
  ]
}
```

## ✅ 체크리스트

- [✅] MySQL 서버 실행
- [✅] 데이터베이스 생성
- [✅] Python 의존성 설치
- [✅] 서버 실행
- [✅] Swagger UI 접속 확인
- [ ] 회원가입 테스트
- [ ] 로그인 테스트
- [ ] 이미지 업로드 테스트
- [ ] 음식 검색 테스트
- [ ] 음식 기록 테스트
- [ ] 대시보드 테스트

모든 테스트가 성공하면 서비스를 사용할 준비가 완료됩니다!