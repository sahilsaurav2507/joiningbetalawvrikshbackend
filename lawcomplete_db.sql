-- =====================================================
-- LawVriksh Backend - Quick Database Setup (FIXED)
-- Simplified MySQL setup for development
-- =====================================================

-- Create database
CREATE DATABASE IF NOT EXISTS lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE lawvriksh_db;

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS suggestions;
DROP TABLE IF EXISTS ux_ratings;
DROP TABLE IF EXISTS ui_ratings;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS not_interested_users;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS admin_users;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession VARCHAR(100) NULL,
    interest_reason TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_gender (gender),
    INDEX idx_profession (profession)
);

-- Creators table
CREATE TABLE creators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession VARCHAR(100) NULL,
    interest_reason TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_gender (gender),
    INDEX idx_profession (profession)
);

-- Not interested users table
CREATE TABLE not_interested_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    not_interested_reason VARCHAR(100) NULL,
    improvement_suggestions TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    INDEX idx_reason (not_interested_reason)
);

-- Feedback table
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
);

-- UI ratings table
CREATE TABLE ui_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT NOT NULL,
    visual_design_rating INT NOT NULL CHECK (visual_design_rating BETWEEN 1 AND 5),
    visual_design_comments TEXT NULL,
    ease_of_navigation_rating INT NOT NULL CHECK (ease_of_navigation_rating BETWEEN 1 AND 5),
    ease_of_navigation_comments TEXT NULL,
    mobile_responsiveness_rating INT NOT NULL CHECK (mobile_responsiveness_rating BETWEEN 1 AND 5),
    mobile_responsiveness_comments TEXT NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE,
    INDEX idx_feedback_id (feedback_id),
    INDEX idx_visual_design (visual_design_rating),
    INDEX idx_navigation (ease_of_navigation_rating),
    INDEX idx_mobile (mobile_responsiveness_rating)
);

-- UX ratings table
CREATE TABLE ux_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT NOT NULL,
    overall_satisfaction_rating INT NOT NULL CHECK (overall_satisfaction_rating BETWEEN 1 AND 5),
    overall_satisfaction_comments TEXT NULL,
    task_completion_rating INT NOT NULL CHECK (task_completion_rating BETWEEN 1 AND 5),
    task_completion_comments TEXT NULL,
    service_quality_rating INT NOT NULL CHECK (service_quality_rating BETWEEN 1 AND 5),
    service_quality_comments TEXT NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE,
    INDEX idx_feedback_id (feedback_id),
    INDEX idx_satisfaction (overall_satisfaction_rating),
    INDEX idx_task_completion (task_completion_rating),
    INDEX idx_service_quality (service_quality_rating)
);

-- Suggestions table
CREATE TABLE suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT NOT NULL,
    liked_features TEXT NULL,
    improvement_suggestions TEXT NULL,
    desired_features TEXT NULL,
    legal_challenges TEXT NULL,
    additional_comments TEXT NULL,
    follow_up_consent BOOLEAN DEFAULT FALSE,
    follow_up_email VARCHAR(255) NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE,
    INDEX idx_feedback_id (feedback_id),
    INDEX idx_follow_up_consent (follow_up_consent),
    INDEX idx_follow_up_email (follow_up_email)
);

-- Admin users table
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);

-- Insert default admin user (password: admin123)
INSERT INTO admin_users (username, email, hashed_password, is_active) VALUES 
('admin', 'admin@lawvriksh.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G', TRUE);

-- Create Views for Analytics
-- View for user statistics
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_count,
    COUNT(CASE WHEN gender = 'Prefer not to say' THEN 1 END) as prefer_not_to_say_count
FROM users;

-- View for creator statistics
CREATE OR REPLACE VIEW creator_statistics AS
SELECT 
    COUNT(*) as total_creators,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_count,
    COUNT(CASE WHEN gender = 'Prefer not to say' THEN 1 END) as prefer_not_to_say_count
FROM creators;

-- View for feedback statistics
CREATE OR REPLACE VIEW feedback_statistics AS
SELECT 
    COUNT(f.id) as total_feedback,
    COUNT(CASE WHEN f.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    AVG(ui.visual_design_rating) as avg_visual_design,
    AVG(ui.ease_of_navigation_rating) as avg_navigation,
    AVG(ui.mobile_responsiveness_rating) as avg_mobile,
    AVG(ux.overall_satisfaction_rating) as avg_satisfaction,
    AVG(ux.task_completion_rating) as avg_task_completion,
    AVG(ux.service_quality_rating) as avg_service_quality,
    COUNT(CASE WHEN s.follow_up_consent = TRUE THEN 1 END) as follow_up_consent_count
FROM feedback f
LEFT JOIN ui_ratings ui ON f.id = ui.feedback_id
LEFT JOIN ux_ratings ux ON f.id = ux.feedback_id
LEFT JOIN suggestions s ON f.id = s.feedback_id;

-- View for not interested statistics
CREATE OR REPLACE VIEW not_interested_statistics AS
SELECT 
    COUNT(*) as total_not_interested,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    not_interested_reason,
    COUNT(*) as reason_count
FROM not_interested_users
GROUP BY not_interested_reason;

-- Show tables
SHOW TABLES;

-- Show views
SHOW FULL TABLES WHERE Table_type = 'VIEW'; 

-- =====================================================
-- Simple Database Fix for LawVriksh
-- Run this to fix the gender column issue
-- =====================================================

USE lawvriksh_db;

-- Add gender column to users table if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL AFTER phone_number;

-- Add gender column to creators table if it doesn't exist
ALTER TABLE creators 
ADD COLUMN IF NOT EXISTS gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL AFTER phone_number;

-- Drop existing views
DROP VIEW IF EXISTS user_statistics;
DROP VIEW IF EXISTS creator_statistics;
DROP VIEW IF EXISTS feedback_statistics;
DROP VIEW IF EXISTS not_interested_statistics;

-- Recreate user_statistics view
CREATE VIEW user_statistics AS
SELECT 
    COUNT(*) as total_users,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_count,
    COUNT(CASE WHEN gender = 'Prefer not to say' THEN 1 END) as prefer_not_to_say_count
FROM users;

-- Recreate creator_statistics view
CREATE VIEW creator_statistics AS
SELECT 
    COUNT(*) as total_creators,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    COUNT(CASE WHEN gender = 'Other' THEN 1 END) as other_count,
    COUNT(CASE WHEN gender = 'Prefer not to say' THEN 1 END) as prefer_not_to_say_count
FROM creators;

-- Recreate feedback_statistics view
CREATE VIEW feedback_statistics AS
SELECT 
    COUNT(f.id) as total_feedback,
    COUNT(CASE WHEN f.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    AVG(ui.visual_design_rating) as avg_visual_design,
    AVG(ui.ease_of_navigation_rating) as avg_navigation,
    AVG(ui.mobile_responsiveness_rating) as avg_mobile,
    AVG(ux.overall_satisfaction_rating) as avg_satisfaction,
    AVG(ux.task_completion_rating) as avg_task_completion,
    AVG(ux.service_quality_rating) as avg_service_quality,
    COUNT(CASE WHEN s.follow_up_consent = TRUE THEN 1 END) as follow_up_consent_count
FROM feedback f
LEFT JOIN ui_ratings ui ON f.id = ui.feedback_id
LEFT JOIN ux_ratings ux ON f.id = ux.feedback_id
LEFT JOIN suggestions s ON f.id = s.feedback_id;

-- Recreate not_interested_statistics view
CREATE VIEW not_interested_statistics AS
SELECT 
    COUNT(*) as total_not_interested,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as recent_7_days,
    COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as recent_30_days,
    not_interested_reason,
    COUNT(*) as reason_count
FROM not_interested_users
GROUP BY not_interested_reason;

-- Test the fix
SELECT 'Database fix completed!' as status;
SELECT * FROM user_statistics; 
-- =====================================================
-- LawVriksh Backend - Sample Data
-- Insert sample data for development and testing
-- =====================================================

USE lawvriksh_db;

-- =====================================================
-- Sample Users Data
-- =====================================================
INSERT INTO users (name, email, phone_number, gender, profession, interest_reason) VALUES
('John Doe', 'john.doe@example.com', '1234567890', 'Male', 'Student', 'Interested in legal services for my studies'),
('Jane Smith', 'jane.smith@example.com', '9876543210', 'Female', 'Lawyer', 'Looking for legal document templates'),
('Bob Johnson', 'bob.johnson@example.com', '5551234567', 'Male', 'Business Owner', 'Need legal advice for my startup'),
('Alice Brown', 'alice.brown@example.com', '4449876543', 'Female', 'Student', 'Researching legal topics'),
('Charlie Wilson', 'charlie.wilson@example.com', '3335557777', 'Other', 'Freelancer', 'Legal consultation for contracts'),
('Diana Davis', 'diana.davis@example.com', '2228889999', 'Female', 'Teacher', 'Personal legal matters'),
('Edward Miller', 'edward.miller@example.com', '1117773333', 'Male', 'Engineer', 'Property law questions'),
('Fiona Garcia', 'fiona.garcia@example.com', '6664442222', 'Female', 'Doctor', 'Medical law information'),
('George Taylor', 'george.taylor@example.com', '9991115555', 'Male', 'Student', 'Criminal law research'),
('Helen Anderson', 'helen.anderson@example.com', '8883337777', 'Female', 'Artist', 'Copyright law assistance');

-- =====================================================
-- Sample Creators Data
-- =====================================================
INSERT INTO creators (name, email, phone_number, gender, profession, interest_reason) VALUES
('Sarah Wilson', 'sarah.wilson@example.com', '1234567891', 'Female', 'Lawyer', 'Want to create legal content'),
('Michael Chen', 'michael.chen@example.com', '9876543211', 'Male', 'Legal Consultant', 'Share legal expertise'),
('Emily Rodriguez', 'emily.rodriguez@example.com', '5551234568', 'Female', 'Law Professor', 'Educational legal content'),
('David Thompson', 'david.thompson@example.com', '4449876544', 'Male', 'Paralegal', 'Legal document creation'),
('Lisa Martinez', 'lisa.martinez@example.com', '3335557778', 'Female', 'Legal Writer', 'Legal blog content'),
('Robert Lee', 'robert.lee@example.com', '2228889990', 'Male', 'Attorney', 'Legal advice videos'),
('Maria Gonzalez', 'maria.gonzalez@example.com', '1117773334', 'Female', 'Legal Researcher', 'Legal research content'),
('James White', 'james.white@example.com', '6664442223', 'Male', 'Law Student', 'Student legal content'),
('Jennifer Hall', 'jennifer.hall@example.com', '9991115556', 'Female', 'Legal Assistant', 'Legal procedure guides'),
('Christopher Allen', 'christopher.allen@example.com', '8883337778', 'Male', 'Legal Analyst', 'Legal market analysis');

-- =====================================================
-- Sample Not Interested Users Data
-- =====================================================
INSERT INTO not_interested_users (name, email, not_interested_reason, improvement_suggestions) VALUES
('Alex Turner', 'alex.turner@example.com', 'Too complex', 'Make the interface simpler'),
('Rachel Green', 'rachel.green@example.com', 'Not relevant', 'Focus on specific legal areas'),
('Tom Harris', 'tom.harris@example.com', 'Other', 'Add more free resources'),
('Sophie Clark', 'sophie.clark@example.com', 'Too expensive', 'Provide more affordable options'),
('Daniel Lewis', 'daniel.lewis@example.com', 'Not relevant', 'Include more business law content'),
('Emma Walker', 'emma.walker@example.com', 'Too complex', 'Simplify the language used'),
('Mark Hall', 'mark.hall@example.com', 'Other', 'Add video tutorials'),
('Olivia Young', 'olivia.young@example.com', 'Not relevant', 'Focus on family law'),
('Peter King', 'peter.king@example.com', 'Too expensive', 'Offer payment plans'),
('Natalie Scott', 'natalie.scott@example.com', 'Other', 'Include more real-world examples');

-- =====================================================
-- Sample Feedback Data
-- =====================================================
INSERT INTO feedback (session_id) VALUES
('fb-session-001'),
('fb-session-002'),
('fb-session-003'),
('fb-session-004'),
('fb-session-005');

-- =====================================================
-- Sample UI Ratings Data
-- =====================================================
INSERT INTO ui_ratings (feedback_id, visual_design_rating, visual_design_comments, ease_of_navigation_rating, ease_of_navigation_comments, mobile_responsiveness_rating, mobile_responsiveness_comments) VALUES
(1, 4, NULL, 5, NULL, 4, NULL),
(2, 3, 'Could be more modern', 4, NULL, 5, NULL),
(3, 5, NULL, 3, 'Navigation could be improved', 4, NULL),
(4, 4, NULL, 4, NULL, 3, 'Mobile layout needs work'),
(5, 5, NULL, 5, NULL, 5, NULL);

-- =====================================================
-- Sample UX Ratings Data
-- =====================================================
INSERT INTO ux_ratings (feedback_id, overall_satisfaction_rating, overall_satisfaction_comments, task_completion_rating, task_completion_comments, service_quality_rating, service_quality_comments) VALUES
(1, 4, NULL, 5, NULL, 4, NULL),
(2, 3, 'Overall experience was okay', 4, NULL, 3, 'Service could be faster'),
(3, 4, NULL, 3, 'Some tasks were confusing', 4, NULL),
(4, 5, NULL, 4, NULL, 5, NULL),
(5, 4, NULL, 5, NULL, 4, NULL);

-- =====================================================
-- Sample Suggestions Data
-- =====================================================
INSERT INTO suggestions (feedback_id, liked_features, improvement_suggestions, desired_features, legal_challenges, additional_comments, follow_up_consent, follow_up_email) VALUES
(1, 'Easy to use interface', 'Add more legal document templates', 'Video consultations', 'Understanding complex legal terms', 'Great platform overall', TRUE, 'john.doe@example.com'),
(2, 'Clean design', 'Improve mobile responsiveness', 'Live chat support', 'Finding relevant information', 'Good start but needs improvement', FALSE, NULL),
(3, 'Comprehensive content', 'Simplify navigation', 'Legal document builder', 'Legal jargon', 'Very helpful resource', TRUE, 'jane.smith@example.com'),
(4, 'Professional appearance', 'Add search functionality', 'Legal calculator tools', 'Cost of legal services', 'Would recommend to others', FALSE, NULL),
(5, 'User-friendly design', 'Include more examples', 'Legal form generator', 'Understanding legal processes', 'Excellent platform', TRUE, 'bob.johnson@example.com');

-- =====================================================
-- Sample Admin Users (Additional)
-- =====================================================
INSERT INTO admin_users (username, email, hashed_password, is_active) VALUES
('manager', 'manager@lawvriksh.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G', TRUE),
('support', 'support@lawvriksh.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO.G', TRUE);

-- =====================================================
-- Verification Queries
-- =====================================================

-- Count records in each table
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Creators', COUNT(*) FROM creators
UNION ALL
SELECT 'Not Interested Users', COUNT(*) FROM not_interested_users
UNION ALL
SELECT 'Feedback', COUNT(*) FROM feedback
UNION ALL
SELECT 'UI Ratings', COUNT(*) FROM ui_ratings
UNION ALL
SELECT 'UX Ratings', COUNT(*) FROM ux_ratings
UNION ALL
SELECT 'Suggestions', COUNT(*) FROM suggestions
UNION ALL
SELECT 'Admin Users', COUNT(*) FROM admin_users;

-- Show sample data
SELECT 'Sample Users:' as info;
SELECT id, name, email, profession FROM users LIMIT 5;

SELECT 'Sample Creators:' as info;
SELECT id, name, email, profession FROM creators LIMIT 5;

SELECT 'Sample Feedback Statistics:' as info;
SELECT 
    f.id,
    f.session_id,
    ui.visual_design_rating,
    ux.overall_satisfaction_rating,
    s.follow_up_consent
FROM feedback f
LEFT JOIN ui_ratings ui ON f.id = ui.feedback_id
LEFT JOIN ux_ratings ux ON f.id = ux.feedback_id
LEFT JOIN suggestions s ON f.id = s.feedback_id
LIMIT 5;
