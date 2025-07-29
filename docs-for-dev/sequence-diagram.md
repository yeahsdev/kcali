@@시퀀스 다이어그램 (Sequence Diagram) - 1. 신규 회원가입
sequenceDiagram
    participant User as 사용자
    participant FE as FrontEnd_App
    participant BE as BackEnd_Server
    participant DB as Database
    User->>FE: 1. 회원가입 정보 입력 (이메일, PW, 신체정보)
    activate FE
    FE->>BE: 2. 회원가입 API 호출
    activate BE
    loop 내부 로직
        BE->>BE: 3. 일일 권장 섭취량 계산
    end
    Note right of BE: 계산된 칼로리 정보를 포함하여
    BE->>DB: 4. 사용자 정보 저장 요청
    activate DB
    DB-->>BE: 5. 저장 성공 응답
    deactivate DB
    BE-->>FE: 6. 회원가입 성공 응답
    deactivate BE
    FE->>User: 7. 회원가입 완료 화면 안내
    deactivate FE
흐름 설명:
사용자가 앱(Front-End)에 정보를 입력합니다.
Front-End는 이 정보를 Back-End 서버로 전송합니다.
Back-End는 전달받은 신체 정보로 내부에서 권장 칼로리를 계산합니다.
Back-End는 모든 정보를 DB에 저장하도록 요청합니다.
DB가 저장 성공을 알립니다.
Back-End가 Front-End로 최종 성공 응답을 보냅니다.
Front-End가 사용자에게 가입 완료 화면을 보여줍니다.
@@시퀀스 다이어그램 (Sequence Diagram) - 2.식단 기록 및 섭취현황 조회
sequenceDiagram
    participant User as 사용자
    participant FE as FrontEnd_App
    participant BE as BackEnd_Server
    participant AI as AI_Model_Server
    participant DB as Database
    User->>FE: 1. 음식 사진 업로드 요청
    activate FE
    FE->>BE: 2. 이미지 업로드 API 호출
    activate BE
    BE->>AI: 3. AI 모델에 음식 인식 요청
    activate AI
    AI-->>BE: 4. 음식 판별 결과 반환 ("김치찌개")
    deactivate AI
    BE->>DB: 5. 음식 DB에서 정보 조회
    activate DB
    DB-->>BE: 6. 칼로리 등 상세 정보 반환
    deactivate DB
    BE->>DB: 7. 섭취 기록 생성 및 저장
    activate DB
    DB-->>BE: 8. 저장 성공 응답
    deactivate DB
    BE-->>FE: 9. 최종 결과(음식명, 칼로리) 반환
    deactivate BE
    FE->>User: 10. 기록 완료 화면 표시
    deactivate FE
다이어그램 흐름 설명
사진 업로드: 사용자가 앱(Front-End)에서 음식 사진을 업로드합니다.
API 호출: Front-End는 이미지를 Back-End 서버로 전송합니다.
AI 음식 인식: Back-End는 이미지를 AI 서버로 보내 분석을 요청합니다.
결과 반환: AI 서버가 음식 이름을 분석하여 Back-End로 전달합니다.
정보 조회: Back-End는 전달받은 음식 이름으로 DB에서 칼로리 정보를 검색합니다.
정보 반환: DB가 검색된 칼로리 정보를 Back-End로 전달합니다.
기록 생성: Back-End가 최종 정보를 DB의 사용자 식단 로그에 저장합니다.
저장 완료: DB가 저장 성공을 알립니다.
최종 결과 전송: Back-End가 모든 처리 결과를 Front-End로 보냅니다.
결과 확인: Front-End가 사용자에게 "김치찌개, 450kcal가 기록되었습니다"와 같은 최종 화면을 보여줍니다.
@@시퀀스 다이어그램 (Sequence Diagram) - 3.대쉬보드(섭취현황 표시)
sequenceDiagram
    participant User as 사용자
    participant FE as FrontEnd_App
    participant BE as BackEnd_Server
    participant DB as Database
    User->>FE: 1. 앱 실행 또는 대시보드 화면 진입
    activate FE
    FE->>BE: 2. 오늘의 대시보드 데이터 요청 API 호출
    activate BE
    BE->>DB: 3. 사용자의 목표 칼로리 조회
    activate DB
    DB-->>BE: 목표 칼로리(e.g., 2000kcal) 반환
    deactivate DB
    BE->>DB: 4. 오늘의 모든 식사 기록(칼로리) 조회
    activate DB
    DB-->>BE: 식사 기록 리스트 반환 (e.g., [450, 350, 500])
    deactivate DB
    loop 내부 로직
        BE->>BE: 5. 일일 섭취 칼로리 집계 (e.g., 1300kcal)
        BE->>BE: 6. 목표와 섭취량 비교
    end
    BE-->>FE: 7. 최종 분석 데이터 반환
    deactivate BE
    Note right of FE: 프로그레스 바, 그래프 등 시각화
    FE->>User: 8. 대시보드 화면 표시
    deactivate FE
▶︎ 다이어그램 흐름 설명:
사용자가 대시보드 화면에 접근합니다.
Front-End는 Back-End 서버에 오늘의 데이터를 요청합니다.
Back-End는 DB에서 해당 유저의 '일일 목표 칼로리'를 가져옵니다.
Back-End는 DB에서 오늘 날짜로 기록된 모든 '식사 기록'을 가져옵니다.
Back-End는 가져온 식사 기록의 칼로리를 모두 합산(집계)합니다.
Back-End는 합산된 값과 목표 칼로리를 비교하여 분석합니다.
Back-End는 분석된 최종 데이터(목표량, 섭취량, 남은 양 등)를 Front-End로 전달합니다.
Front-End는 이 데이터를 바탕으로 프로그레스 바나 그래프 등을 그려 사용자에게 보여줍니다.