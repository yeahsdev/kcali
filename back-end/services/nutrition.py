def calculate_daily_calories(gender: str, age: int, height: float, weight: float, activity_level: float = 1.55) -> float:
    if gender == 'M':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    return round(bmr * activity_level, 0)