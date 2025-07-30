# KCali 프론트엔드-백엔드 연결 문제 분석 보고서

## 🔴 주요 문제점

### 1. API 베이스 URL 설정 오류 (가장 심각한 문제)

**파일**: `/front-end/src/api/client.js`
**위치**: 5번째 줄
**현재 코드**:
```javascript
baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001/api/',
```

**문제점**:
- 포트 번호가 잘못됨: 8001 → 8000
- 백엔드는 8000 포트에서 실행되는데 프론트엔드는 8001로 요청을 보냄

**수정 필요**:
```javascript
baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
```

---

### 2. Authorization 헤더 불일치

**파일**: `/front-end/src/api/client.js`
**위치**: 9-20번째 줄
**현재 코드**:
```javascript
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
```

**문제점**:
- 프론트엔드는 JWT Bearer 토큰 방식을 사용
- 백엔드는 단순히 user_id를 토큰으로 사용하고, 쿼리 파라미터로 전달받음
- 불필요한 Authorization 헤더가 전송되어 백엔드에서 무시됨

---

### 3. 데이터 타입 변환 누락

**파일**: `/front-end/src/pages/SignupPage.jsx`
**위치**: 27번째 줄
**현재 코드**:
```javascript
const response = await apiClient.post('/v1/users/signup/', formData);
```

**문제점**:
- HTML input의 number 타입도 실제로는 문자열로 전송됨
- 백엔드는 age, height, weight를 정수형으로 기대함
- 타입 불일치로 인한 400 Bad Request 발생 가능

**수정 필요**:
```javascript
const response = await apiClient.post('/v1/users/signup/', {
  ...formData,
  age: parseInt(formData.age),
  height: parseInt(formData.height),
  weight: parseInt(formData.weight)
});
```

---

### 4. 환경 변수 파일 부재

**필요한 파일**: `/front-end/.env`
**현재 상태**: 파일이 존재하지 않음

**문제점**:
- 환경 변수 VITE_API_URL이 설정되지 않아 하드코딩된 기본값 사용
- 개발/프로덕션 환경 전환이 어려움

**생성 필요**:
```env
VITE_API_URL=http://localhost:8000/api/
```

---

## 📊 문제 우선순위

1. **긴급**: API 베이스 URL 수정 (포트 8001 → 8000)
2. **중요**: 데이터 타입 변환 추가
3. **권장**: 환경 변수 파일 생성
4. **선택**: Authorization 헤더 로직 수정

## 🔧 즉시 해결 방법

### 방법 1: 환경 변수 설정 (권장)
프론트엔드 디렉토리에 `.env` 파일 생성:
```bash
cd front-end
echo "VITE_API_URL=http://localhost:8000/api/" > .env
```

### 방법 2: 하드코딩 수정
`/front-end/src/api/client.js` 파일의 5번째 줄을 직접 수정

## 💡 추가 권장사항

1. **CORS 설정 확인**: 백엔드의 CORS 설정은 올바르게 되어 있음 (localhost:5173 허용)
2. **에러 처리 개선**: 프론트엔드에서 더 구체적인 에러 메시지 표시
3. **개발자 도구 활용**: Network 탭에서 실제 요청 URL과 응답 확인

## 🎯 결론

가장 큰 문제는 **포트 번호 불일치**입니다. 프론트엔드가 8001 포트로 요청을 보내지만, 백엔드는 8000 포트에서 실행되고 있습니다. 이 문제만 해결하면 API 연결이 정상적으로 작동할 것입니다.