# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

# Kcali: AI 음식 분석 서비스 API 명세

본 문서는 Kcali 서비스의 프론트엔드와 백엔드 간의 통신을 위한 API 규격을 정의합니다.

**Base URL:** `https://api.your-service.com`

---

## 認証 (Authentication)

로그인을 제외한 모든 API 요청은 HTTP Header에 JWT Access Token을 포함하여 전송해야 합니다.

* **Header Key:** `Authorization`
* **Header Value:** `Bearer [Access Token]`

---

## 👤 사용자 API (User API)

### 1. 회원가입

사용자의 정보를 받아 새로운 계정을 생성합니다.

* **Method:** `POST`
* **Endpoint:** `/api/v1/users/signup/`
* **Request Body:**

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

* **Success Response (201 Created):**

    ```json
    {
      "message": "회원가입이 성공적으로 완료되었습니다.",
      "user": {
        "email": "user@example.com"
      }
    }
    ```

### 2. 로그인 (JWT 토큰 발급)

사용자 인증 후, API 접근을 위한 Access Token과 Refresh Token을 발급합니다.

* **Method:** `POST`
* **Endpoint:** `/api/v1/users/login/`
* **Request Body:**

    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```

* **Success Response (200 OK):**

    ```json
    {
      "message": "로그인 성공",
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG..."
    }
    ```

---

## 📊 대시보드 API (Dashboard API)

### 1. 일일 대시보드 데이터 조회

로그인한 사용자의 오늘 날짜 기준 섭취/목표 칼로리 및 음식 기록을 조회합니다.

* **Method:** `GET`
* **Endpoint:** `/api/v1/dashboard/today/`
* **Authentication:** **Required (JWT)**
* **Success Response (200 OK):**

    ```json
    {
      "goal_kcal": 2000,
      "consumed_kcal": 360,
      "food_logs": [
        {
          "id": 1,
          "name": "계란 후라이",
          "kcal": 180,
          "time": "아침"
        },
        {
          "id": 2,
          "name": "닭가슴살 샐러드",
          "kcal": 180,
          "time": "점심"
        }
      ]
    }
    ```

---

## 🍔 음식 API (Food API)

### 1. 음식 사진 분석 및 기록

사용자가 업로드한 음식 사진을 분석하고, 식단 기록에 추가합니다.

* **Method:** `POST`
* **Endpoint:** `/api/v1/foods/analyze/`
* **Authentication:** **Required (JWT)**
* **Request Body:** `multipart/form-data` 형식의 이미지 파일 (key: `image`)
* **Success Response (201 Created):**

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