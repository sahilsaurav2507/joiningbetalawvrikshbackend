-- Create database with proper character set and collation
CREATE DATABASE IF NOT EXISTS lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE lawvriksh_db;

-- Drop existing admin_users table if it exists with wrong structure
DROP TABLE IF EXISTS refresh_tokens;
DROP TABLE IF EXISTS admin_users;

-- Create admin users table with correct structure
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Create users table for waiting list
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    profession VARCHAR(100),
    organization VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    how_did_you_hear VARCHAR(255),
    specific_interests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_profession (profession),
    INDEX idx_city (city)
);

-- Create creators table for creator waiting list
CREATE TABLE IF NOT EXISTS creators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    content_type VARCHAR(100),
    experience_level VARCHAR(50),
    platform_experience TEXT,
    portfolio_url VARCHAR(500),
    social_media_handles JSON,
    content_focus TEXT,
    why_join TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_content_type (content_type),
    INDEX idx_experience_level (experience_level)
);

-- Create feedback sessions table
CREATE TABLE IF NOT EXISTS feedback_sessions (
    id VARCHAR(36) PRIMARY KEY,
    user_email VARCHAR(255),
    user_name VARCHAR(255),
    session_status ENUM('started', 'ui_completed', 'ux_completed', 'completed') DEFAULT 'started',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    INDEX idx_user_email (user_email),
    INDEX idx_session_status (session_status),
    INDEX idx_created_at (created_at)
);

-- Create UI ratings table
CREATE TABLE IF NOT EXISTS ui_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    overall_design INT CHECK (overall_design BETWEEN 1 AND 5),
    color_scheme INT CHECK (color_scheme BETWEEN 1 AND 5),
    typography INT CHECK (typography BETWEEN 1 AND 5),
    layout INT CHECK (layout BETWEEN 1 AND 5),
    visual_hierarchy INT CHECK (visual_hierarchy BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES feedback_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id)
);

-- Create UX ratings table
CREATE TABLE IF NOT EXISTS ux_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    ease_of_use INT CHECK (ease_of_use BETWEEN 1 AND 5),
    navigation INT CHECK (navigation BETWEEN 1 AND 5),
    information_clarity INT CHECK (information_clarity BETWEEN 1 AND 5),
    loading_speed INT CHECK (loading_speed BETWEEN 1 AND 5),
    mobile_responsiveness INT CHECK (mobile_responsiveness BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES feedback_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id)
);

-- Create suggestions table
CREATE TABLE IF NOT EXISTS suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    what_liked TEXT,
    what_improved TEXT,
    additional_features TEXT,
    overall_experience TEXT,
    recommend_rating INT CHECK (recommend_rating BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES feedback_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id)
);

-- Create not interested table
CREATE TABLE IF NOT EXISTS not_interested (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    reason VARCHAR(500),
    additional_feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);

-- Create refresh tokens table for JWT management
CREATE TABLE refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    admin_id INT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (admin_id) REFERENCES admin_users(id) ON DELETE CASCADE,
    INDEX idx_token_hash (token_hash),
    INDEX idx_admin_id (admin_id),
    INDEX idx_expires_at (expires_at)
);

-- Insert default admin user (password: change-this-password)
-- The password hash is generated using bcrypt with salt rounds = 12
INSERT INTO admin_users (username, email, password_hash, is_superuser, is_active) 
VALUES (
    'admin', 
    'admin@lawvriksh.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS',
    TRUE,
    TRUE
);

-- Verify the admin user was created
SELECT 'Admin user created successfully' as status, username, email, is_superuser 
FROM admin_users 
WHERE username = 'admin';