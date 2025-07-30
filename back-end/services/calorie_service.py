def calculate_bmr(gender: str, age: int, height: float, weight: float) -> float:
    """
    BMR(기초대사율) 계산 - Mifflin-St Jeor 공식
    gender: 'M' or 'F'
    age: 나이
    height: 키 (cm)
    weight: 몸무게 (kg)
    """
    if gender == 'M':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    return bmr

def calculate_daily_calories(bmr: float, activity_level: float = 1.55) -> float:
    """
    일일 권장 칼로리 계산
    activity_level: 활동 수준 (기본값 1.55 = 보통 활동량)
    """
    return round(bmr * activity_level, 0)