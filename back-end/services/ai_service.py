# AI 모델 연동 서비스
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import logging
from typing import Dict, Optional
from sqlalchemy.orm import Session
from models.food import Food
from pathlib import Path
from config.settings import AI_MODEL_PATH

logger = logging.getLogger(__name__)

# 음식 클래스 목록 (모델이 인식할 수 있는 음식들)
FOOD_CLASSES = [
    "apple_pie", "Baked Potato", "burger", "butter_naan", "chai",
    "chapati", "cheesecake", "chicken_curry", "chole_bhature",
    "Crispy Chicken", "dal_makhani", "dhokla", "Donut", "fried_rice",
    "Fries", "Hot Dog", "ice_cream", "idli", "jalebi"
]

# 모델 아키텍처 정의 (실제 모델과 동일해야 함)
class FoodClassifier(nn.Module):
    def __init__(self, num_classes=len(FOOD_CLASSES)):
        super(FoodClassifier, self).__init__()
        # ResNet18 기반 모델 가정
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            # 간단한 구조로 가정
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(64 * 56 * 56, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

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
        model_path = Path(__file__).parent.parent / AI_MODEL_PATH
        
        # 모델 초기화
        model = FoodClassifier(num_classes=len(FOOD_CLASSES))
        
        # CPU에서 실행
        device = torch.device("cpu")
        
        # 모델 가중치 로드
        if model_path.exists():
            model.load_state_dict(torch.load(model_path, map_location=device))
            logger.info(f"모델을 성공적으로 로드했습니다: {model_path}")
        else:
            logger.warning(f"모델 파일을 찾을 수 없습니다: {model_path}. 랜덤 가중치를 사용합니다.")
        
        model.to(device)
        model.eval()
        
        # 이미지 전처리 transform 정의
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
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
        
        # 예측된 음식 클래스
        predicted_food = FOOD_CLASSES[predicted_idx.item()]
        confidence_score = confidence.item()
        
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
        fallback_food = FOOD_CLASSES[0]
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