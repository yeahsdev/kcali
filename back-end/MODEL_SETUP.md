# AI 모델 설정 가이드

## 모델 파일 위치

AI 음식 인식 기능을 사용하려면 `best_food_model.pth` 파일이 필요합니다.

### 모델 파일 설치

1. `best_food_model.pth` 파일을 다음 위치에 배치하세요:
   ```
   back-end/best_food_model.pth
   ```

2. 모델 파일이 없는 경우:
   - 서비스는 정상적으로 시작되지만 경고 메시지가 표시됩니다
   - 음식 인식 시 랜덤 가중치를 사용하므로 정확도가 매우 낮습니다

### 모델 아키텍처

현재 코드는 다음과 같은 모델 구조를 가정합니다:
- 입력: 224x224 RGB 이미지
- 출력: 19개 음식 클래스에 대한 확률
- 아키텍처: 간단한 CNN (ResNet 스타일)

### 지원되는 음식 클래스

모델이 인식할 수 있는 음식 목록:
- apple_pie
- Baked Potato
- burger
- butter_naan
- chai
- chapati
- cheesecake
- chicken_curry
- chole_bhature
- Crispy Chicken
- dal_makhani
- dhokla
- Donut
- fried_rice
- Fries
- Hot Dog
- ice_cream
- idli
- jalebi

### 모델 경로 변경

모델 파일 경로를 변경하려면 `config/settings.py`에서 수정하세요:
```python
AI_MODEL_PATH = "your_model_path.pth"
```

### 문제 해결

1. **모델 파일을 찾을 수 없음**
   - 파일 경로가 올바른지 확인
   - 파일 권한 확인

2. **모델 로드 오류**
   - PyTorch 버전 확인
   - 모델 파일이 손상되지 않았는지 확인

3. **메모리 부족**
   - 더 작은 모델 사용 고려
   - 배치 크기 조정