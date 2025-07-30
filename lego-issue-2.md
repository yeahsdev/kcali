# KCali 프론트엔드 422 에러 및 데이터베이스 미저장 문제 분석

## 🔴 문제 1: 422 Unprocessable Entity 에러

### 발생 위치
**파일**: `/front-end/src/pages/DashboardPage.jsx`
**라인**: 16번째 줄
```javascript
const response = await apiClient.get('/v1/dashboard/today/');
```

### 문제점
- `user_id` 쿼리 파라미터가 누락됨
- 백엔드는 필수 파라미터로 `user_id`를 요구함

### 해결 방법
```javascript
// 현재 코드
const response = await apiClient.get('/v1/dashboard/today/');

// 수정 필요
const userId = localStorage.getItem('userId'); // 로그인 시 저장된 user_id
const response = await apiClient.get(`/v1/dashboard/today?user_id=${userId}`);
```

---

## 🔴 문제 2: 음식 업로드 후 데이터베이스 미저장

### 발생 위치
**파일**: `/front-end/src/pages/DashboardPage.jsx`
**라인**: 38-58번째 줄

### 문제점
현재 코드는 음식 인식만 하고 데이터베이스에 저장하지 않음:
```javascript
// 현재 코드 (음식 인식만 함)
await apiClient.post('/v1/food/upload', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});
alert('업로드 성공! 데이터를 새로고침합니다.');
```

### 해결 방법
음식 인식 후 기록 API도 호출해야 함:
```javascript
// 1단계: 음식 인식
const uploadResponse = await apiClient.post('/v1/food/upload', formData, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// 2단계: 인식된 음식을 데이터베이스에 저장
const userId = localStorage.getItem('userId');
const foodName = uploadResponse.data.food_name;

// 먼저 음식 검색으로 food_id 찾기
const searchResponse = await apiClient.get(`/v1/food/search?q=${foodName}`);
if (searchResponse.data.results.length > 0) {
  const foodId = searchResponse.data.results[0].food_id;
  
  // 음식 섭취 기록
  await apiClient.post('/v1/food/record', {
    user_id: parseInt(userId),
    food_id: foodId,
    serving_amount: 1.0
  });
}
```

---

## 🔴 문제 3: 로그인 후 user_id 저장 누락

### 확인 필요
로그인 페이지에서 `user_id`를 localStorage에 저장하는지 확인 필요

### 예상 코드 (LoginPage.jsx)
```javascript
const response = await apiClient.post('/v1/users/login/', loginData);
// user_id 저장 확인
localStorage.setItem('userId', response.data.user_id);
localStorage.setItem('accessToken', response.data.access_token);
```

---

## 📋 완전한 해결 순서

1. **로그인 시 user_id 저장 확인**
   - LoginPage.jsx에서 localStorage에 userId 저장

2. **DashboardPage.jsx 수정**
   - fetchData 함수에 user_id 추가
   - handleFileChange 함수에 음식 기록 로직 추가

3. **에러 처리 개선**
   - user_id가 없을 때 로그인 페이지로 리다이렉트
   - 음식을 찾을 수 없을 때 사용자에게 알림

## 🚨 중요 참고사항

백엔드 API 플로우:
1. `/v1/food/upload` - 음식 인식만 (DB 저장 없음)
2. `/v1/food/search` - 음식명으로 food_id 검색
3. `/v1/food/record` - 실제 DB에 섭취 기록 저장
4. `/v1/dashboard/today` - 저장된 데이터 조회 (user_id 필수)