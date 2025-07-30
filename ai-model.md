# AI 모델 백엔드 통합 가이드

## 개요
학습된 ResNet18 모델 (best_food_model.pth)을 백엔드 서비스에 통합하기 위한 수정 사항을 정리합니다.

## 1. back-end/services/ai_service.py 수정

### 1.1 import 추가
```python
import json
from torchvision import models
```

### 1.2 클래스 매핑 로드 (line 15 이후)
```python
# 클래스 매핑 로드
def load_class_mapping():
    mapping_path = Path(__file__).parent.parent.parent / "class_mapping.json"
    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    return mapping['idx_to_class'], list(mapping['class_to_idx'].keys())

idx_to_class, FOOD_CLASSES = load_class_mapping()
```

### 1.3 FOOD_CLASSES 리스트 제거 (line 17-22)
기존의 하드코딩된 FOOD_CLASSES 리스트를 제거하고 위의 load_class_mapping()으로 대체

### 1.4 FoodClassifier 클래스 교체 (line 25-48)
```python
# 모델 로드 함수
def load_resnet_model(num_classes):
    model = models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    return model
```

기존 FoodClassifier 클래스를 제거하고 위 함수로 대체

### 1.5 load_model() 함수 수정 (line 54-91)
```python
def load_model():
    """모델을 로드합니다."""
    global model, transform
    
    if model is not None:
        return
    
    try:
        # 모델 경로
        model_path = Path(__file__).parent.parent.parent / AI_MODEL_PATH
        
        # 모델 초기화
        model = load_resnet_model(num_classes=len(FOOD_CLASSES))
        
        # CPU에서 실행
        device = torch.device("cpu")
        
        # 모델 가중치 로드
        if model_path.exists():
            model.load_state_dict(torch.load(model_path, map_location=device))
            logger.info(f"모델을 성공적으로 로드했습니다: {model_path}")
        else:
            logger.error(f"모델 파일을 찾을 수 없습니다: {model_path}")
            raise FileNotFoundError(f"모델 파일이 없습니다: {model_path}")
        
        model.to(device)
        model.eval()
        
        # 이미지 전처리 transform 정의 (predict.py와 동일하게)
        transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
    except Exception as e:
        logger.error(f"모델 로드 중 오류 발생: {str(e)}")
        raise
```

### 1.6 recognize_food() 함수 수정 (line 115-117)
```python
# 예측된 음식 클래스 (인덱스를 문자열로 변환)
predicted_class_name = idx_to_class[str(predicted_idx.item())]
confidence_score = confidence.item()

# 음식명 정규화 (언더스코어를 공백으로, 첫 글자 대문자)
predicted_food = predicted_class_name.replace('_', ' ').title()
```

## 2. 데이터베이스 음식명 매핑

현재 데이터베이스의 음식명과 모델의 클래스명이 다를 수 있습니다:
- 모델: "apple_pie", "baked_potato", "crispy_chicken"
- DB: "apple_pie", "Baked Potato", "Crispy Chicken"

### 2.1 매핑 딕셔너리 추가 (ai_service.py에 추가)
```python
# 모델 클래스명을 DB 음식명으로 매핑
MODEL_TO_DB_MAPPING = {
    "apple_pie": "apple_pie",
    "baked_potato": "Baked Potato",
    "burger": "burger",
    "butter_naan": "butter_naan",
    "chai": "chai",
    "chapati": "chapati",
    "cheesecake": "cheesecake",
    "chicken_curry": "chicken_curry",
    "chole_bhature": "chole_bhature",
    "crispy_chicken": "Crispy Chicken",
    "dal_makhani": "dal_makhani",
    "dhokla": "dhokla",
    "donut": "Donut",
    "fried_rice": "fried_rice",
    "fries": "Fries",
    "hot_dog": "Hot Dog",
    "ice_cream": "ice_cream",
    "idli": "idli",
    "jalebi": "jalebi",
    # 새로운 클래스들 추가
    "kaathi_rolls": "kaathi_rolls",
    "kadai_paneer": "kadai_paneer",
    "kulfi": "kulfi",
    "masala_dosa": "masala_dosa",
    "momos": "momos",
    "omelette": "omelette",
    "paani_puri": "paani_puri",
    "pakode": "pakode",
    "pav_bhaji": "pav_bhaji",
    "pizza": "pizza",
    "samosa": "samosa",
    "sandwich": "sandwich",
    "sushi": "sushi",
    "taco": "taco",
    "taquito": "taquito"
}
```

### 2.2 recognize_food() 함수에서 매핑 사용
```python
# 예측된 음식 클래스
predicted_class_name = idx_to_class[str(predicted_idx.item())]
confidence_score = confidence.item()

# DB 음식명으로 매핑
predicted_food = MODEL_TO_DB_MAPPING.get(predicted_class_name, predicted_class_name)
```

## 3. 필요한 파일 확인

다음 파일들이 루트 디렉토리에 있어야 합니다:
- `best_food_model.pth` - 학습된 모델 파일
- `class_mapping.json` - 클래스 인덱스 매핑 파일

## 4. 테스트 방법

1. 백엔드 서버 실행
```bash
cd back-end
python main.py
```

2. API 테스트 (curl 또는 Postman 사용)
```bash
curl -X POST "http://localhost:8000/api/v1/food/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

## 5. 주의사항

1. 새로운 음식 클래스(kaathi_rolls, kadai_paneer 등)가 데이터베이스에 없을 수 있습니다. 이 경우:
   - 데이터베이스에 해당 음식 정보를 추가하거나
   - recognize_food() 함수의 에러 처리 로직이 작동하여 기본값을 반환합니다

2. 이미지 전처리가 학습 시와 동일해야 정확한 예측이 가능합니다.

3. 모델 파일 크기가 클 수 있으므로 초기 로딩 시간이 필요합니다.