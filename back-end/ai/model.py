import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
from typing import Tuple, Dict
from config import get_settings

settings = get_settings()

class FoodClassifier:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.class_mapping = {}
        self.num_classes = 27
        
    def load_model(self):
        try:
            self.model = models.resnet18(pretrained=False)
            num_features = self.model.fc.in_features
            self.model.fc = nn.Linear(num_features, self.num_classes)
            
            checkpoint = torch.load(settings.model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint)
            self.model.to(self.device)
            self.model.eval()
            
            with open(settings.class_mapping_path, 'r', encoding='utf-8') as f:
                self.class_mapping = json.load(f)
                
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, image_path: str) -> Tuple[str, float]:
        if self.model is None:
            if not self.load_model():
                return "Unknown", 0.0
        
        try:
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
            class_idx = predicted.item()
            food_name = self.class_mapping.get(str(class_idx), "Unknown")
            confidence_score = confidence.item()
            
            return food_name, confidence_score
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return "Unknown", 0.0

food_classifier = FoodClassifier()