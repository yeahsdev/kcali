def predict_image(model, image_path, idx_to_class, transform=None):
    """
    단일 이미지 예측
    
    Args:
        model: 학습된 모델
        image_path: 예측할 이미지 경로
        idx_to_class: 인덱스-클래스 매핑
        transform: 이미지 변환
    
    Returns:
        예측된 클래스, 신뢰도
    """
    if transform is None:
        transform = test_transform
    
    # 이미지 로드 및 전처리
    try:
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0).to(device)
        
        # 예측
        model.eval()
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # 결과 반환
        predicted_class = idx_to_class[predicted.item()]
        confidence_score = confidence.item() * 100
        
        return predicted_class, confidence_score
        
    except Exception as e:
        print(f"예측 오류: {str(e)}")
        return None, 0.0