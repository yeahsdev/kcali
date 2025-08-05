# Kcali: AI 음식 인식 칼로리 추적 서비스

[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

**Kcali**는 사용자가 음식 사진을 업로드하면, AI가 음식을 인식하여 칼로리와 영양 정보를 자동으로 기록하고 관리해주는 웹 서비스입니다. 건강한 식습관을 만들고 목표 칼로리를 관리할 수 있도록 돕습니다.

## ✨ 주요 기능

* **AI 음식 인식**: 음식 사진을 찍어 올리면 AI가 자동으로 음식을 인식하고 데이터베이스에서 영양 정보를 찾아줍니다.
* **실시간 칼로리 추적**: 섭취한 음식의 칼로리를 기록하고, 일일 목표 섭취량 대비 현재 진행 상황을 시각적으로 보여줍니다.
* **개인화된 목표 설정**: 회원가입 시 입력한 신체 정보(성별, 나이, 키, 몸무게)를 바탕으로 개인에게 맞는 일일 권장 칼로리를 자동으로 계산합니다.
* **대시보드**: 오늘의 섭취 칼로리, 목표 칼로리, 남은 칼로리를 한눈에 파악할 수 있는 대시보드를 제공합니다.
* **섭취 기록 조회**: 과거의 식단 기록을 날짜별로 조회하여 식습관을 분석할 수 있습니다.

## 🛠️ 기술 스택

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **프론트엔드** | React (Vite) | 사용자 인터페이스 구축 |
| **백엔드** | FastAPI (Python) | API 서버 구축 및 비즈니스 로직 처리 |
| **데이터베이스** | MySQL | 사용자 정보, 음식 데이터, 식단 기록 저장 |
| **AI (머신러닝)** | PyTorch | 음식 이미지 인식을 위한 딥러닝 모델 |
| **ORM** | SQLAlchemy | Python 코드와 데이터베이스 간의 상호작용 |

## 🚀 프로젝트 시작하기

### 1. 사전 준비

* **MySQL** 서버가 설치 및 실행되어 있어야 합니다.
* **Python 3.11** 이상 버전이 설치되어 있어야 합니다.
* **Node.js** (LTS 버전 권장)가 설치되어 있어야 합니다.

### 2. 백엔드 설정 및 실행

```bash
# 1. 프로젝트 클론 후 back-end 폴더로 이동
cd back-end

# 2. 데이터베이스 생성 (최초 1회)
# MySQL에 접속하여 아래 쿼리 실행
CREATE DATABASE food_calorie_tracker;

# 3. Python 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# 4. 필수 라이브러리 설치
pip install -r requirements.txt

# 5. 음식 데이터베이스 초기화 (최초 1회)
python init_food_data.py

# 6. (선택사항) AI 모델 파일 준비
# best_food_model.pth 파일을 back-end 폴더 내에 위치시킵니다.
# 파일이 없어도 서버는 실행되지만, 음식 인식 정확도가 떨어집니다.

# 7. 백엔드 서버 실행
python main.py

서버가 http://127.0.0.1:8000에서 실행됩니다. API 문서는 http://127.0.0.1:8000/docs에서 확인할 수 있습니다.

### 3. 프론트엔드 설정 및 실행

# 1. 새 터미널을 열고 front-end 폴더로 이동
cd front-end

# 2. 필수 라이브러리 설치
npm install

# 3. 프론트엔드 개발 서버 실행
npm run dev

애플리케이션이 http://localhost:5173에서 실행됩니다. 브라우저를 열어 접속하세요.


Markdown

# Kcali: AI 음식 인식 칼로리 추적 서비스

[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)

**Kcali**는 사용자가 음식 사진을 업로드하면, AI가 음식을 인식하여 칼로리와 영양 정보를 자동으로 기록하고 관리해주는 웹 서비스입니다. 건강한 식습관을 만들고 목표 칼로리를 관리할 수 있도록 돕습니다.

## ✨ 주요 기능

* **AI 음식 인식**: 음식 사진을 찍어 올리면 AI가 자동으로 음식을 인식하고 데이터베이스에서 영양 정보를 찾아줍니다.
* **실시간 칼로리 추적**: 섭취한 음식의 칼로리를 기록하고, 일일 목표 섭취량 대비 현재 진행 상황을 시각적으로 보여줍니다.
* **개인화된 목표 설정**: 회원가입 시 입력한 신체 정보(성별, 나이, 키, 몸무게)를 바탕으로 개인에게 맞는 일일 권장 칼로리를 자동으로 계산합니다.
* **대시보드**: 오늘의 섭취 칼로리, 목표 칼로리, 남은 칼로리를 한눈에 파악할 수 있는 대시보드를 제공합니다.
* **섭취 기록 조회**: 과거의 식단 기록을 날짜별로 조회하여 식습관을 분석할 수 있습니다.

## 🛠️ 기술 스택

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **프론트엔드** | React (Vite) | 사용자 인터페이스 구축 |
| **백엔드** | FastAPI (Python) | API 서버 구축 및 비즈니스 로직 처리 |
| **데이터베이스** | MySQL | 사용자 정보, 음식 데이터, 식단 기록 저장 |
| **AI (머신러닝)** | PyTorch | 음식 이미지 인식을 위한 딥러닝 모델 |
| **ORM** | SQLAlchemy | Python 코드와 데이터베이스 간의 상호작용 |

## 🚀 프로젝트 시작하기

### 1. 사전 준비

* **MySQL** 서버가 설치 및 실행되어 있어야 합니다.
* **Python 3.11** 이상 버전이 설치되어 있어야 합니다.
* **Node.js** (LTS 버전 권장)가 설치되어 있어야 합니다.

### 2. 백엔드 설정 및 실행

```bash
# 1. 프로젝트 클론 후 back-end 폴더로 이동
cd back-end

# 2. 데이터베이스 생성 (최초 1회)
# MySQL에 접속하여 아래 쿼리 실행
CREATE DATABASE food_calorie_tracker;

# 3. Python 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# 4. 필수 라이브러리 설치
pip install -r requirements.txt

# 5. 음식 데이터베이스 초기화 (최초 1회)
python init_food_data.py

# 6. (선택사항) AI 모델 파일 준비
# best_food_model.pth 파일을 back-end 폴더 내에 위치시킵니다.
# 파일이 없어도 서버는 실행되지만, 음식 인식 정확도가 떨어집니다.

# 7. 백엔드 서버 실행
python main.py
서버가 http://127.0.0.1:8000에서 실행됩니다. API 문서는 http://127.0.0.1:8000/docs에서 확인할 수 있습니다.

3. 프론트엔드 설정 및 실행
Bash

# 1. 새 터미널을 열고 front-end 폴더로 이동
cd front-end

# 2. 필수 라이브러리 설치
npm install

# 3. 프론트엔드 개발 서버 실행
npm run dev
애플리케이션이 http://localhost:5173에서 실행됩니다. 브라우저를 열어 접속하세요.

📁 프로젝트 구조
kcali/
├── back-end/           # FastAPI 백엔드 서버
│   ├── api/            # API 라우터 (엔드포인트)
│   ├── models/         # SQLAlchemy DB 모델
│   ├── schemas/        # Pydantic 데이터 검증 스키마
│   ├── services/       # 비즈니스 로직 (AI, 칼로리 계산 등)
│   ├── main.py         # FastAPI 앱 실행 파일
│   └── requirements.txt
│
└── front-end/          # React 프론트엔드
    ├── src/
    │   ├── api/        # API 클라이언트 (axios)
    │   ├── pages/      # 페이지 컴포넌트 (로그인, 대시보드 등)
    │   └── App.jsx     # 메인 라우팅 설정
    └── package.json
