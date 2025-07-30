# 데이터베이스 호환성 검토 보고서

## 현재 상황

백엔드 API와 데이터베이스 스키마(database.md) 간의 호환성을 검토한 결과입니다.

## 호환성 분석

### ✅ 완벽히 호환되는 부분

1. **테이블 구조**
   - users, food, food_records 테이블 모두 SQLAlchemy 모델과 일치
   - 모든 필드명과 데이터 타입이 정확히 매칭

2. **데이터 타입**
   - DECIMAL → Float (SQLAlchemy)
   - VARCHAR → String
   - TIMESTAMP → DateTime
   - 모든 타입이 올바르게 매핑됨

3. **제약 조건**
   - PRIMARY KEY, FOREIGN KEY, UNIQUE 제약이 모두 호환
   - 인덱스도 적절히 설정됨

### ⚠️ 충돌 가능한 부분

1. **트리거 문제**
   ```sql
   -- 트리거가 food 테이블에서 직접 칼로리를 가져옴
   SET NEW.calories_kcal = v_calories;  -- serving_amount 미고려
   ```
   
   백엔드 코드:
   ```python
   # serving_amount를 고려하여 계산
   calories = food.calories_kcal * request.serving_amount
   ```

2. **중복 로직**
   - 회원가입: 프로시저 vs Python 코드
   - 칼로리 계산: 트리거 vs Python 서비스

## 해결 방안

### 옵션 1: 트리거 비활성화 (권장)
```sql
-- 트리거 삭제
DROP TRIGGER IF EXISTS before_food_record_insert;

-- 프로시저 삭제 (백엔드 API 사용)
DROP PROCEDURE IF EXISTS register_user;
```

### 옵션 2: 트리거 수정
serving_amount를 고려하도록 트리거 수정이 필요하나, 
트리거에서는 serving_amount 정보를 받을 수 없으므로 비현실적

## 권장 사항

1. **즉시 조치**
   - 트리거 `before_food_record_insert` 삭제
   - 프로시저 `register_user` 삭제
   - 모든 로직은 백엔드 API에서 처리

2. **데이터베이스는 단순 저장소로**
   - 비즈니스 로직은 애플리케이션 레이어에서
   - 데이터베이스는 데이터 무결성만 보장

3. **마이그레이션 스크립트**
   ```sql
   -- 안전한 마이그레이션
   DROP TRIGGER IF EXISTS before_food_record_insert;
   DROP PROCEDURE IF EXISTS register_user;
   ```

## 결론

현재 백엔드 API는 데이터베이스 스키마와 구조적으로는 완벽히 호환되지만,
트리거와 프로시저로 인한 로직 충돌이 발생할 수 있습니다.
트리거와 프로시저를 제거하면 문제없이 작동합니다.