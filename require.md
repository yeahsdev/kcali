# 칼로리 추적 서비스 (KCali) - 프로젝트 요구사항

## 프로젝트 개요

KCali는 사용자가 음식 사진을 촬영하여 업로드하면, AI 모델이 음식을 인식하고 해당 음식의 칼로리 정보를 제공하는 서비스입니다. 사용자의 일일 칼로리 섭취량을 추적하고 관리할 수 있는 대시보드를 제공합니다.

### 핵심 기능
1. **회원 관리**: 회원가입 시 신체 정보를 기반으로 일일 권장 칼로리 자동 계산
2. **음식 인식**: AI 모델을 통한 음식 사진 분석 및 자동 인식
3. **칼로리 추적**: 섭취한 음식의 칼로리 정보 기록 및 관리
4. **대시보드**: 일일 섭취 칼로리 현황 시각화 및 목표 대비 진행률 표시

## 시스템 아키텍처

```
사용자 → Frontend (React) → Backend (FastAPI) → AI Server
                                    ↓
                               Database (MySQL)
```

## 기능 요구사항

### 1. 회원 관리 (✅ 구현 완료)
- **회원가입** (`POST /api/v1/users/signup/`)
  - 이메일, 비밀번호, 성별, 나이, 키, 몸무게 입력
  - BMR 및 일일 권장 칼로리 자동 계산
  - 중복 이메일 검증
  
- **로그인** (`POST /api/v1/users/login/`)
  - 이메일/비밀번호 인증
  - 액세스 토큰 발급

### 2. 음식 인식 및 기록 (✅ 구현 완료)
- **음식 사진 업로드 및 인식** (`POST /api/v1/food/upload`)
  - 이미지 파일 업로드 (JPEG, PNG 지원)
  - 더미 AI 모델로 음식 인식 (실제 AI 서버 대신 랜덤 선택)
  - 음식 인식 결과 및 칼로리 정보 반환
  
- **음식 검색** (`GET /api/v1/food/search`)
  - 음식명으로 검색
  - 칼로리 및 영양 정보 조회
  
- **음식 섭취 기록** (`POST /api/v1/food/record`)
  - 인식된 음식 정보 저장
  - 사용자별 섭취 기록 생성
  - 일일 총 칼로리 업데이트

### 3. 대시보드 (✅ 구현 완료)
- **오늘의 섭취 현황** (`GET /api/v1/dashboard/today`)
  - 일일 목표 칼로리
  - 현재까지 섭취한 칼로리
  - 남은 칼로리
  - 진행률 (%)
  
- **섭취 기록 조회** (`GET /api/v1/dashboard/history`)
  - 날짜별 섭취 기록
  - 음식별 상세 정보

## 데이터베이스 스키마

### users 테이블
- user_id (PK)
- email (UNIQUE)
- password
- gender (M/F)
- age
- height
- weight
- daily_target_calories

### food 테이블
- food_id (PK)
- food (음식명, UNIQUE)
- serving_size
- calories_kcal
- protein_g
- fat_g
- carbs_g

### food_records 테이블
- record_id (PK)
- datetime
- user_id (FK)
- daily_target_calories
- daily_total_calories
- food_id (FK)
- food_name
- calories_kcal
- protein_g
- fat_g
- carbs_g

## 미구현 백엔드 API 상세

### 1. POST /api/v1/food/upload
**기능**: 음식 사진을 업로드하고 AI 인식 결과를 받습니다.

**Request**:
- Content-Type: multipart/form-data
- Body: image file

**Response**:
```json
{
  "food_name": "김치찌개",
  "confidence": 0.95,
  "calories": 450,
  "nutrition": {
    "protein_g": 25.0,
    "fat_g": 15.0,
    "carbs_g": 30.0
  }
}
```

### 2. GET /api/v1/food/search
**기능**: 음식명으로 데이터베이스에서 칼로리 정보를 검색합니다.

**Request**:
- Query Parameters: `q` (검색어)

**Response**:
```json
{
  "results": [
    {
      "food_id": 1,
      "food_name": "김치찌개",
      "serving_size": "1인분",
      "calories": 450,
      "nutrition": {
        "protein_g": 25.0,
        "fat_g": 15.0,
        "carbs_g": 30.0
      }
    }
  ]
}
```

### 3. POST /api/v1/food/record
**기능**: 사용자의 음식 섭취를 기록합니다.

**Request**:
```json
{
  "user_id": 1,
  "food_id": 1,
  "serving_amount": 1.0
}
```

**Response**:
```json
{
  "record_id": 123,
  "message": "음식이 성공적으로 기록되었습니다.",
  "daily_total_calories": 1300
}
```

### 4. GET /api/v1/dashboard/today
**기능**: 오늘의 칼로리 섭취 현황을 조회합니다.

**Request**:
- Headers: Authorization (user_id)

**Response**:
```json
{
  "date": "2025-07-29",
  "daily_target_calories": 2000,
  "consumed_calories": 1300,
  "remaining_calories": 700,
  "progress_percentage": 65,
  "meals": [
    {
      "record_id": 123,
      "time": "08:30",
      "food_name": "김치찌개",
      "calories": 450
    }
  ]
}
```

### 5. GET /api/v1/dashboard/history
**기능**: 지정된 기간의 섭취 기록을 조회합니다.

**Request**:
- Query Parameters: 
  - `start_date` (YYYY-MM-DD)
  - `end_date` (YYYY-MM-DD)
- Headers: Authorization (user_id)

**Response**:
```json
{
  "records": [
    {
      "date": "2025-07-29",
      "total_calories": 1300,
      "target_calories": 2000,
      "meals_count": 3
    }
  ]
}
```

## 개발 우선순위

1. **Phase 1**: 음식 데이터베이스 구축 ✅
   - food 테이블에 기본 음식 데이터 입력 ✅
   - CSV 파일에서 데이터 로드 스크립트 작성 ✅ (`init_food_data.py`)

2. **Phase 2**: AI 연동 API 개발 ✅
   - 이미지 업로드 엔드포인트 ✅
   - AI 서버 통신 모듈 ✅ (더미 AI 구현)
   - 음식 인식 결과 처리 ✅

3. **Phase 3**: 음식 기록 API 개발
   - 음식 검색 기능
   - 섭취 기록 저장
   - 일일 칼로리 집계

4. **Phase 4**: 대시보드 API 개발
   - 오늘의 섭취 현황 조회
   - 기간별 기록 조회
   - 통계 데이터 생성

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy, MySQL
- **Frontend**: React, Vite
- **AI Model**: 별도 AI 서버 (구현 필요)
- **인증**: 현재 간단한 토큰 방식 (개선 필요)

## 보안 고려사항

1. 비밀번호 암호화 필요 (현재 평문 저장)
2. JWT 토큰 기반 인증 구현 필요 (별도 지시 전까지 구현하지 않음)
3. API Rate Limiting 필요
4. 이미지 업로드 시 파일 검증 필요 ✅ (파일 크기, 형식 검증 구현)

## 실행 방법

### 1. 백엔드 서버 실행
```bash
cd back-end
python main.py
```

### 2. 음식 데이터 초기화 (최초 1회)
```bash
cd back-end
python init_food_data.py
```

### 3. API 테스트
- Swagger UI: http://localhost:8000/docs
- 음식 인식 API: POST http://localhost:8000/api/v1/food/upload
  - multipart/form-data로 이미지 파일 전송
  - 지원 형식: JPEG, PNG (최대 10MB)

  1. POST /api/v1/food/upload - 음식 사진 업로드 및 AI 인식 ✅
  2. GET /api/v1/food/search - 음식 검색 ✅
  3. POST /api/v1/food/record - 음식 섭취 기록 ✅
  4. GET /api/v1/dashboard/today - 오늘의 섭취 현황
  5. GET /api/v1/dashboard/history - 섭취 기록 조회

 데이터베이스 스키마 검토 완료

  주요 충돌 사항:
        
  1. 트리거 충돌 🔴
    - before_food_record_insert 트리거가 백엔드의 serving_amount 계산을 무시
    - 백엔드에서 계산한 칼로리가 트리거에 의해 덮어씌워짐
  2. 중복 로직 ⚠️
    - 회원가입 프로시저와 백엔드 API 로직 중복
    - 칼로리 계산이 트리거와 Python 코드에서 중복

  해결 방법:

  -- 충돌 해결을 위한 SQL
  DROP TRIGGER IF EXISTS before_food_record_insert;
  DROP PROCEDURE IF EXISTS register_user;

  결론:

  - 테이블 구조는 완벽히 호환 ✅
  - 트리거와 프로시저만 제거하면 충돌 없이 작동 가능
  - 모든 비즈니스 로직은 백엔드 API에서 처리하는 것이 권장됨

  DATABASE_COMPATIBILITY.md 파일에 상세한 분석 결과를 저장했습니다.
