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