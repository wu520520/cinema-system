-- 创建数据库
CREATE DATABASE IF NOT EXISTS cinema_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cinema_system;

-- 创建地区表
CREATE TABLE IF NOT EXISTS movie_region (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL UNIQUE,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建分类表
CREATE TABLE IF NOT EXISTS movie_category (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL UNIQUE,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建影片表
CREATE TABLE IF NOT EXISTS movie_film (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(64) NOT NULL,
    synopsis VARCHAR(1024),
    pic VARCHAR(80),
    region INT,
    director VARCHAR(30),
    release_date DATE,
    times INT NOT NULL,
    score FLOAT,
    grade VARCHAR(5) NOT NULL,
    category INT NOT NULL,
    profit INT,
    organization VARCHAR(128),
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (region) REFERENCES movie_region(id) ON DELETE SET NULL,
    FOREIGN KEY (category) REFERENCES movie_category(id) ON DELETE RESTRICT,
    INDEX idx_title (title),
    INDEX idx_region (region),
    INDEX idx_category (category),
    INDEX idx_grade (grade),
    INDEX idx_created (created)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始化地区数据
INSERT INTO movie_region (name) VALUES 
('内地'),
('港台'),
('欧美'),
('亚洲'),
('其它')
ON DUPLICATE KEY UPDATE name=name;

-- 初始化分类数据
INSERT INTO movie_category (name) VALUES 
('动作'),
('喜剧'),
('爱情'),
('动画'),
('剧情'),
('惊悚'),
('犯罪'),
('科幻'),
('战争'),
('纪录'),
('电视剧'),
('其他')
ON DUPLICATE KEY UPDATE name=name;
