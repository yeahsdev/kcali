-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS food_calorie_tracker
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE food_calorie_tracker;

-- Users 테이블
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    age INT NOT NULL,
    height DECIMAL(5,2) NOT NULL,
    weight DECIMAL(5,2) NOT NULL,
    daily_target_calories DECIMAL(7,2) NOT NULL,
    
    INDEX idx_email (email)
);

-- Food 테이블
CREATE TABLE food (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food VARCHAR(100) NOT NULL UNIQUE,
    serving_size VARCHAR(50) NOT NULL,
    calories_kcal DECIMAL(7,2) NOT NULL,
    protein_g DECIMAL(5,2) DEFAULT 0,
    fat_g DECIMAL(5,2) DEFAULT 0,
    carbs_g DECIMAL(5,2) DEFAULT 0,
    
    INDEX idx_food_name (food)
);

-- Food_records 테이블
CREATE TABLE food_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    daily_target_calories DECIMAL(7,2) NOT NULL,
    daily_total_calories DECIMAL(7,2) DEFAULT 0,
    food_id INT NOT NULL,
    food_name VARCHAR(100) NOT NULL,
    calories_kcal DECIMAL(7,2) NOT NULL,
    protein_g DECIMAL(5,2) DEFAULT 0,
    fat_g DECIMAL(5,2) DEFAULT 0,
    carbs_g DECIMAL(5,2) DEFAULT 0,
    
    CONSTRAINT fk_food_records_user_id FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_food_records_food_id FOREIGN KEY (food_id) REFERENCES food(food_id) ON UPDATE CASCADE,
    
    INDEX idx_user_datetime (user_id, datetime),
    INDEX idx_food_id (food_id),
    INDEX idx_food_name (food_name)
);

-- 회원가입 프로시저
DELIMITER //

CREATE PROCEDURE register_user(
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(255),
    IN p_gender CHAR(1),
    IN p_age INT,
    IN p_height DECIMAL(5,2),
    IN p_weight DECIMAL(5,2)
)
BEGIN
    DECLARE v_bmr DECIMAL(7,2);
    DECLARE v_target_calories DECIMAL(7,2);
    
    -- BMR 계산 (Mifflin-St Jeor 공식)
    IF p_gender = 'M' THEN
        SET v_bmr = (10 * p_weight) + (6.25 * p_height) - (5 * p_age) + 5;
    ELSE
        SET v_bmr = (10 * p_weight) + (6.25 * p_height) - (5 * p_age) - 161;
    END IF;
    
    -- 보통 활동량 기준 (BMR * 1.55)으로 일일 목표 칼로리 계산
    SET v_target_calories = ROUND(v_bmr * 1.55, 0);
    
    -- 사용자 정보 저장
    INSERT INTO users (
        email, password, gender, age, height, weight, daily_target_calories
    ) VALUES (
        p_email, p_password, p_gender, p_age, p_height, p_weight, v_target_calories
    );
    
    SELECT LAST_INSERT_ID() as user_id, v_target_calories as daily_target_calories;
END//

DELIMITER ;

-- 음식 기록 삽입 트리거 (날짜별 총 칼로리 자동 계산)
DELIMITER //

CREATE TRIGGER before_food_record_insert 
BEFORE INSERT ON food_records
FOR EACH ROW
BEGIN
    DECLARE v_calories DECIMAL(7,2);
    DECLARE v_protein DECIMAL(5,2);
    DECLARE v_fat DECIMAL(5,2);
    DECLARE v_carbs DECIMAL(5,2);
    DECLARE v_food_name VARCHAR(100);
    DECLARE v_target_calories DECIMAL(7,2);
    DECLARE v_today_calories DECIMAL(7,2);
    
    -- users 테이블에서 목표 칼로리 가져오기
    SELECT daily_target_calories 
    INTO v_target_calories
    FROM users 
    WHERE user_id = NEW.user_id;
    
    -- food 테이블에서 영양 정보 가져오기 (food_id로 조회)
    SELECT calories_kcal, protein_g, fat_g, carbs_g, food
    INTO v_calories, v_protein, v_fat, v_carbs, v_food_name
    FROM food 
    WHERE food_id = NEW.food_id;
    
    -- NULL 체크
    IF v_calories IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Food not found in database';
    END IF;
    
    -- 값 설정
    SET NEW.daily_target_calories = v_target_calories;
    SET NEW.food_name = v_food_name;
    SET NEW.calories_kcal = v_calories;
    SET NEW.protein_g = v_protein;
    SET NEW.fat_g = v_fat;
    SET NEW.carbs_g = v_carbs;
    
    -- 해당 날짜의 총 칼로리 계산 (같은 날짜의 기록만)
    SELECT COALESCE(SUM(calories_kcal), 0)
    INTO v_today_calories
    FROM food_records
    WHERE user_id = NEW.user_id
        AND DATE(datetime) = DATE(NEW.datetime);
    
    -- 현재 기록의 칼로리를 더해서 총 칼로리 설정
    SET NEW.daily_total_calories = v_today_calories + v_calories;
END//

DELIMITER ;