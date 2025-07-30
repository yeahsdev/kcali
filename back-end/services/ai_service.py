# AI 모델 연동 서비스
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io
import json
import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session
from models.food import Food
from pathlib import Path
from config.settings import AI_MODEL_PATH

logger = logging.getLogger(__name__)

# 클래스 매핑 로드
def load_class_mapping():
    """class_mapping.json 파일에서 클래스 매핑을 로드합니다."""
    mapping_path = Path(__file__).parent.parent.parent / "class_mapping.json"
    try:
        with open(mapping_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        return mapping['idx_to_class'], list(mapping['class_to_idx'].keys())
    except Exception as e:
        logger.error(f"클래스 매핑 로드 실패: {str(e)}")
        # 폴백: 기본 클래스 목록 사용
        default_classes = [
            "apple_pie", "baked_potato", "burger", "butter_naan", "chai",
            "chapati", "cheesecake", "chicken_curry", "chole_bhature",
            "crispy_chicken", "dal_makhani", "dhokla", "donut", "fried_rice",
            "fries", "hot_dog", "ice_cream", "idli", "jalebi"
        ]
        idx_to_class = {str(i): cls for i, cls in enumerate(default_classes)}
        return idx_to_class, default_classes

idx_to_class, FOOD_CLASSES = load_class_mapping()

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

# ResNet18 모델 로드 함수
def load_resnet_model(num_classes):
    """사전 학습된 ResNet18 모델을 로드하고 마지막 층을 수정합니다."""
    model = models.resnet18(pretrained=False)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, num_classes)
    return model

# 전역 변수로 모델 저장
model = None
transform = None

def load_model():
    """모델을 로드합니다."""
    global model, transform
    
    if model is not None:
        return
    
    try:
        # 모델 경로
        model_path = Path(__file__).parent.parent.parent / AI_MODEL_PATH
        
        # ResNet18 모델 초기화
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

# 모델은 첫 요청 시 로드됨 (지연 로딩)

async def recognize_food(image_data: bytes, db: Session) -> Optional[Dict]:
    """
    AI 모델로 음식을 인식합니다.
    """
    # 모델이 로드되지 않았다면 로드
    if model is None:
        load_model()
    
    try:
        # 이미지 데이터를 PIL Image로 변환
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # 이미지 전처리
        input_tensor = transform(image).unsqueeze(0)
        
        # 모델 추론
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        # 예측된 음식 클래스 (인덱스를 문자열로 변환)
        predicted_class_name = idx_to_class[str(predicted_idx.item())]
        confidence_score = confidence.item()
        
        # DB 음식명으로 매핑
        predicted_food = MODEL_TO_DB_MAPPING.get(predicted_class_name, predicted_class_name)
        
        # 데이터베이스에서 음식 정보 조회
        food_item = db.query(Food).filter(Food.food == predicted_food).first()
        
        if not food_item:
            # 음식을 찾을 수 없는 경우 기본값 반환
            logger.warning(f"데이터베이스에서 음식을 찾을 수 없습니다: {predicted_food}")
            return {
                "food_name": predicted_food,
                "confidence": confidence_score,
                "calories": 200.0,
                "serving_size": "1 serving",
                "nutrition": {
                    "protein_g": 10.0,
                    "fat_g": 5.0,
                    "carbs_g": 30.0
                }
            }
        
        # 음식 정보가 있는 경우
        return {
            "food_name": food_item.food,
            "confidence": confidence_score,
            "calories": food_item.calories_kcal,
            "serving_size": food_item.serving_size,
            "nutrition": {
                "protein_g": food_item.protein_g,
                "fat_g": food_item.fat_g,
                "carbs_g": food_item.carbs_g
            }
        }
        
    except Exception as e:
        logger.error(f"음식 인식 중 오류 발생: {str(e)}")
        # 오류 발생 시 폴백으로 첫 번째 음식 반환
        fallback_class = FOOD_CLASSES[0]
        fallback_food = MODEL_TO_DB_MAPPING.get(fallback_class, fallback_class)
        food_item = db.query(Food).filter(Food.food == fallback_food).first()
        
        if food_item:
            return {
                "food_name": food_item.food,
                "confidence": 0.5,  # 낮은 신뢰도
                "calories": food_item.calories_kcal,
                "serving_size": food_item.serving_size,
                "nutrition": {
                    "protein_g": food_item.protein_g,
                    "fat_g": food_item.fat_g,
                    "carbs_g": food_item.carbs_g
                }
            }
        else:
            return None