import axios from 'axios';

// -------------------------------------------------------------------
// 1. axios 인스턴스 생성
// -------------------------------------------------------------------
// baseURL을 설정하여, 앞으로 모든 요청에 기본 URL을 반복해서 입력하지 않도록 합니다.
// .env 파일 등을 통해 환경 변수로 관리하는 것이 가장 좋습니다.
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/',
});

// -------------------------------------------------------------------
// 2. 요청 인터셉터 (Request Interceptor) 설정
// -------------------------------------------------------------------
// 이 부분은 API 요청을 보내기 '전'에 가로채서 특정 작업을 수행하게 만듭니다.
// 여기서는 모든 요청 헤더에 JWT 인증 토큰을 자동으로 추가해주는 역할을 합니다.
apiClient.interceptors.request.use(
  (config) => {
    // 로컬 스토리지에서 'accessToken'을 가져옵니다.
    const token = localStorage.getItem('accessToken');

    // 토큰이 존재한다면,
    if (token) {
      // HTTP 헤더의 'Authorization' 필드에 'Bearer' 방식의 토큰을 추가합니다.
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    // 요청 에러 처리
    return Promise.reject(error);
  }
);

export default apiClient;