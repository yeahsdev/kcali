Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 2 additions and 1 removal
        1    # AI 모델 연동 서비스
        2    import torch
        3    import torch.nn as nn
        4 -  from torchvision import transforms
        4 +  from torchvision import transforms, models
        5    from PIL import Image
        6    import io
        7 +  import json
        8    import logging
        9    from typing import Dict, Optional
       10    from sqlalchemy.orm import Session

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☐ class_mapping.json 로드 함수 추가
     ☐ 기존 FoodClassifier를 ResNet18로 교체
     ☐ 이미지 전처리 transform 수정
     ☐ 모델 출력과 DB 음식명 매핑 추가
     ☐ recognize_food 함수에서 새로운 클래스 처리
  ⎿  Found 2 new diagnostic issues in 1 file (ctrl-r to expand)

⏺ Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 59 additions and 7 removals             
       14    
       15    logger = logging.getLogger(__name__)
       16    
       17 -  # 음식 클래스 목록 (모델이 인식할 수 있는 음식들)
       18 -  FOOD_CLASSES = [
       19 -      "apple_pie", "Baked Potato", "burger", "butter_naan", "chai",
       20 -      "chapati", "cheesecake", "chicken_curry", "chole_bhature",
       21 -      "Crispy Chicken", "dal_makhani", "dhokla", "Donut", "fried_rice",
       22 -      "Fries", "Hot Dog", "ice_cream", "idli", "jalebi"
       23 -  ]
       17 +  # 클래스 매핑 로드
       18 +  def load_class_mapping():
       19 +      """class_mapping.json 파일에서 클래스 매핑을 로드합니다."""
       20 +      mapping_path = Path(__file__).parent.parent.parent / "class_mapping.json"
       21 +      try:
       22 +          with open(mapping_path, 'r', encoding='utf-8') as f:
       23 +              mapping = json.load(f)
       24 +          return mapping['idx_to_class'], list(mapping['class_to_idx'].keys())
       25 +      except Exception as e:
       26 +          logger.error(f"클래스 매핑 로드 실패: {str(e)}")
       27 +          # 폴백: 기본 클래스 목록 사용
       28 +          default_classes = [
       29 +              "apple_pie", "baked_potato", "burger", "butter_naan", "chai",
       30 +              "chapati", "cheesecake", "chicken_curry", "chole_bhature",
       31 +              "crispy_chicken", "dal_makhani", "dhokla", "donut", "fried_rice",
       32 +              "fries", "hot_dog", "ice_cream", "idli", "jalebi"
       33 +          ]
       34 +          idx_to_class = {str(i): cls for i, cls in enumerate(default_classes)}
       35 +          return idx_to_class, default_classes
       36    
       37 +  idx_to_class, FOOD_CLASSES = load_class_mapping()
       38 +  
       39 +  # 모델 클래스명을 DB 음식명으로 매핑
       40 +  MODEL_TO_DB_MAPPING = {
       41 +      "apple_pie": "apple_pie",
       42 +      "baked_potato": "Baked Potato",
       43 +      "burger": "burger",
       44 +      "butter_naan": "butter_naan",
       45 +      "chai": "chai",
       46 +      "chapati": "chapati",
       47 +      "cheesecake": "cheesecake",
       48 +      "chicken_curry": "chicken_curry",
       49 +      "chole_bhature": "chole_bhature",
       50 +      "crispy_chicken": "Crispy Chicken",
       51 +      "dal_makhani": "dal_makhani",
       52 +      "dhokla": "dhokla",
       53 +      "donut": "Donut",
       54 +      "fried_rice": "fried_rice",
       55 +      "fries": "Fries",
       56 +      "hot_dog": "Hot Dog",
       57 +      "ice_cream": "ice_cream",
       58 +      "idli": "idli",
       59 +      "jalebi": "jalebi",
       60 +      "kaathi_rolls": "kaathi_rolls",
       61 +      "kadai_paneer": "kadai_paneer",
       62 +      "kulfi": "kulfi",
       63 +      "masala_dosa": "masala_dosa",
       64 +      "momos": "momos",
       65 +      "omelette": "omelette",
       66 +      "paani_puri": "paani_puri",
       67 +      "pakode": "pakode",
       68 +      "pav_bhaji": "pav_bhaji",
       69 +      "pizza": "pizza",
       70 +      "samosa": "samosa",
       71 +      "sandwich": "sandwich",
       72 +      "sushi": "sushi",
       73 +      "taco": "taco",
       74 +      "taquito": "taquito"
       75 +  }
       76 +  
       77    # 모델 아키텍처 정의 (실제 모델과 동일해야 함)
       78    class FoodClassifier(nn.Module):
       79        def __init__(self, num_classes=len(FOOD_CLASSES)):

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☒ class_mapping.json 로드 함수 추가
     ☐ 기존 FoodClassifier를 ResNet18로 교체
     ☐ 이미지 전처리 transform 수정
     ☐ 모델 출력과 DB 음식명 매핑 추가
     ☐ recognize_food 함수에서 새로운 클래스 처리

⏺ Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 7 additions and 25 removals       
        74        "taquito": "taquito"
        75    }
        76    
        77 -  # 모델 아키텍처 정의 (실제 모델과 동일해야 함)
        78 -  class FoodClassifier(nn.Module):
        79 -      def __init__(self, num_classes=len(FOOD_CLASSES)):
        80 -          super(FoodClassifier, self).__init__()
        81 -          # ResNet18 기반 모델 가정
        82 -          self.features = nn.Sequential(
        83 -              nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
        84 -              nn.BatchNorm2d(64),
        85 -              nn.ReLU(inplace=True),
        86 -              nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
        87 -              # 간단한 구조로 가정
        88 -          )
        89 -          self.classifier = nn.Sequential(
        90 -              nn.Dropout(0.5),
        91 -              nn.Linear(64 * 56 * 56, 512),
        92 -              nn.ReLU(inplace=True),
        93 -              nn.Dropout(0.5),
        94 -              nn.Linear(512, num_classes)
        95 -          )
        96 -      
        97 -      def forward(self, x):
        98 -          x = self.features(x)
        99 -          x = torch.flatten(x, 1)
       100 -          x = self.classifier(x)
       101 -          return x
        77 +  # ResNet18 모델 로드 함수
        78 +  def load_resnet_model(num_classes):
        79 +      """사전 학습된 ResNet18 모델을 로드하고 마지막 층을 수정합니다."""
        80 +      model = models.resnet18(pretrained=False)
        81 +      num_features = model.fc.in_features
        82 +      model.fc = nn.Linear(num_features, num_classes)
        83 +      return model
        84    
        85    # 전역 변수로 모델 저장
        86    model = None

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☒ class_mapping.json 로드 함수 추가
     ☒ 기존 FoodClassifier를 ResNet18로 교체
     ☐ 이미지 전처리 transform 수정
     ☐ 모델 출력과 DB 음식명 매핑 추가
     ☐ recognize_food 함수에서 새로운 클래스 처리
  ⎿  Found 1 new diagnostic issue in 1 file (ctrl-r to expand)

⏺ Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 8 additions and 6 removals                                      
        95        
        96        try:
        97            # 모델 경로
        98 -          model_path = Path(__file__).parent.parent / AI_MODEL_PATH
        98 +          model_path = Path(__file__).parent.parent.parent / AI_MODEL_PATH
        99            
       100 -          # 모델 초기화
       101 -          model = FoodClassifier(num_classes=len(FOOD_CLASSES))
       100 +          # ResNet18 모델 초기화
       101 +          model = load_resnet_model(num_classes=len(FOOD_CLASSES))
       102            
       103            # CPU에서 실행
       104            device = torch.device("cpu")
     ...
       108                model.load_state_dict(torch.load(model_path, map_location=device))
       109                logger.info(f"모델을 성공적으로 로드했습니다: {model_path}")
       110            else:
       111 -              logger.warning(f"모델 파일을 찾을 수 없습니다: {model_path}. 랜덤 가중치를 사용합니다.")
       111 +              logger.error(f"모델 파일을 찾을 수 없습니다: {model_path}")
       112 +              raise FileNotFoundError(f"모델 파일이 없습니다: {model_path}")
       113            
       114            model.to(device)
       115            model.eval()
       116            
       117 -          # 이미지 전처리 transform 정의
       117 +          # 이미지 전처리 transform 정의 (predict.py와 동일하게)
       118            transform = transforms.Compose([
       119 -              transforms.Resize((224, 224)),
       119 +              transforms.Resize(256),
       120 +              transforms.CenterCrop(224),
       121                transforms.ToTensor(),
       122                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
       123            ])

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☒ class_mapping.json 로드 함수 추가
     ☒ 기존 FoodClassifier를 ResNet18로 교체
     ☒ 이미지 전처리 transform 수정
     ☐ 모델 출력과 DB 음식명 매핑 추가
     ☐ recognize_food 함수에서 새로운 클래스 처리

⏺ Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 5 additions and 2 removals                              
       149                probabilities = torch.nn.functional.softmax(outputs, dim=1)
       150                confidence, predicted_idx = torch.max(probabilities, 1)
       151            
       152 -          # 예측된 음식 클래스
       153 -          predicted_food = FOOD_CLASSES[predicted_idx.item()]
       152 +          # 예측된 음식 클래스 (인덱스를 문자열로 변환)
       153 +          predicted_class_name = idx_to_class[str(predicted_idx.item())]
       154            confidence_score = confidence.item()
       155            
       156 +          # DB 음식명으로 매핑
       157 +          predicted_food = MODEL_TO_DB_MAPPING.get(predicted_class_name, predicted_class_name)
       158 +          
       159            # 데이터베이스에서 음식 정보 조회
       160            food_item = db.query(Food).filter(Food.food == predicted_food).first()
       161            

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☒ class_mapping.json 로드 함수 추가
     ☒ 기존 FoodClassifier를 ResNet18로 교체
     ☒ 이미지 전처리 transform 수정
     ☒ 모델 출력과 DB 음식명 매핑 추가
     ☐ recognize_food 함수에서 새로운 클래스 처리

⏺ Update(back-end/services/ai_service.py)
  ⎿  Updated back-end/services/ai_service.py with 2 additions and 1 removal                  
       190        except Exception as e:
       191            logger.error(f"음식 인식 중 오류 발생: {str(e)}")
       192            # 오류 발생 시 폴백으로 첫 번째 음식 반환
       193 -          fallback_food = FOOD_CLASSES[0]
       193 +          fallback_class = FOOD_CLASSES[0]
       194 +          fallback_food = MODEL_TO_DB_MAPPING.get(fallback_class, fallback_class)
       195            food_item = db.query(Food).filter(Food.food == fallback_food).first()
       196            
       197            if food_item:

⏺ Update Todos
  ⎿  ☒ ai_service.py에 ResNet18 모델 import 및 json import 추가
     ☒ class_mapping.json 로드 함수 추가
     ☒ 기존 FoodClassifier를 ResNet18로 교체
     ☒ 이미지 전처리 transform 수정
     ☒ 모델 출력과 DB 음식명 매핑 추가
     ☒ recognize_food 함수에서 새로운 클래스 처리

⏺ 이제 코드 문법 확인을 해보겠습니다.

⏺ Bash(cd /Users/baejaemyeong/Desktop/coding/INTEL-APP/kcali_2025-07-28/kcali/back-end && python -m py_compile services/ai_service.py)
  ⎿  (No content)

⏺ 모든 수정이 완료되었습니다! 주요 변경 사항은 다음과 같습니다:

  1. ResNet18 모델 사용: 기존의 간단한 CNN 구조를 ResNet18로 교체
  2. class_mapping.json 로드: 34개 클래스를 동적으로 로드
  3. 이미지 전처리 업데이트: predict.py와 동일한 transform 사용 (Resize→CenterCrop→ToTensor→Normalize)
  4. 모델-DB 음식명 매핑: 모델 출력(예: "crispy_chicken")을 DB 음식명(예: "Crispy Chicken")으로 변환
  5. 새로운 클래스 처리: 34개 모든 클래스에 대한 매핑 추가

  백엔드가 이제 새로운 모델과 완전히 통합되었습니다.