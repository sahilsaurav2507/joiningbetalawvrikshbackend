-- =====================================================
-- LawVriksh Database System - Complete Implementation
-- =====================================================

-- 1. Database and Table Creation
DROP DATABASE IF EXISTS lawvriksh_db;
CREATE DATABASE lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE lawvriksh_db;

-- Core Tables
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession VARCHAR(100) NULL,
    interest_reason TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE creators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NULL,
    profession VARCHAR(100) NULL,
    interest_reason TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE not_interested_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    not_interested_reason VARCHAR(100) NULL,
    improvement_suggestions TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
);

CREATE TABLE ui_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT NOT NULL,
    visual_design_rating INT NOT NULL CHECK (visual_design_rating BETWEEN 1 AND 5),
    visual_design_comments TEXT NULL,
    ease_of_navigation_rating INT NOT NULL CHECK (ease_of_navigation_rating BETWEEN 1 AND 5),
    ease_of_navigation_comments TEXT NULL,
    mobile_responsiveness_rating INT NOT NULL CHECK (mobile_responsiveness_rating BETWEEN 1 AND 5),
    mobile_responsiveness_comments TEXT NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE
);

CREATE TABLE ux_ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT NOT NULL,
    overall_satisfaction_rating INT NOT NULL CHECK (overall_satisfaction_rating BETWEEN 1 AND 5),
    overall_satisfaction_comments TEXT NULL,
    task_completion_rating INT NOT NULL CHECK (task_completion_rating BETWEEN 1 AND 5),
    task_completion_comments TEXT NULL,
    service_quality_rating INT NOT NULL CHECK (service_quality_rating BETWEEN 1 AND 5),
    service_quality_comments TEXT NULL,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE
);

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
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE
);

CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Index Optimization
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_creators_profession ON creators(profession);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);
CREATE INDEX idx_ui_ratings_feedback ON ui_ratings(feedback_id);
CREATE INDEX idx_suggestions_followup ON suggestions(follow_up_consent, follow_up_email);

-- Views for Analytics
CREATE VIEW user_statistics AS
SELECT 
    COUNT(*) AS total_users,
    COUNT(CASE WHEN created_at >= CURDATE() - INTERVAL 7 DAY THEN 1 END) AS new_users_7d,
    COUNT(CASE WHEN created_at >= CURDATE() - INTERVAL 30 DAY THEN 1 END) AS new_users_30d,
    COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS male_count,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS female_count,
    AVG(
        (SELECT AVG(overall_satisfaction_rating) 
         FROM feedback f
         JOIN ux_ratings ux ON f.id = ux.feedback_id
         WHERE f.session_id = users.email)
    ) AS avg_satisfaction
FROM users;

CREATE VIEW feedback_analysis AS
SELECT
    f.id,
    f.session_id,
    ui.mobile_responsiveness_rating,
    LEFT(ui.mobile_responsiveness_comments, 100) AS mobile_comments,
    ux.task_completion_rating,
    s.desired_features
FROM feedback f
JOIN ui_ratings ui ON f.id = ui.feedback_id
JOIN ux_ratings ux ON f.id = ux.feedback_id
JOIN suggestions s ON f.id = s.feedback_id
WHERE ui.mobile_responsiveness_rating < 4;

-- =====================================================
-- 2. Sample Data Insertion
-- =====================================================

-- Users
INSERT INTO users (name, email, phone_number, gender, profession, interest_reason) VALUES
('John Doe', 'john@example.com', '1234567890', 'Male', 'Student', 'Legal research for studies'),
('Jane Smith', 'jane@example.com', '9876543210', 'Female', 'Lawyer', 'Document templates'),
('Alex Brown', 'alex@example.com', '5551234567', 'Other', 'Business Owner', 'Startup legal advice');

-- Creators
INSERT INTO creators (name, email, phone_number, gender, profession, interest_reason) VALUES
('Sarah Lee', 'sarah@example.com', '1112223333', 'Female', 'Attorney', 'Create legal content'),
('Mike Chen', 'mike@example.com', '4445556666', 'Male', 'Legal Scholar', 'Share expertise');

-- Feedback Sessions
INSERT INTO feedback (session_id) VALUES
('FB20230712001'), ('FB20230712002'), ('FB20230712003');

-- UI Ratings
INSERT INTO ui_ratings (feedback_id, visual_design_rating, ease_of_navigation_rating, mobile_responsiveness_rating, mobile_responsiveness_comments) VALUES
(1, 4, 5, 3, 'Mobile menu difficult to use'),
(2, 5, 4, 5, NULL),
(3, 3, 3, 2, 'Text too small on mobile devices');

-- UX Ratings
INSERT INTO ux_ratings (feedback_id, overall_satisfaction_rating, task_completion_rating, service_quality_rating) VALUES
(1, 4, 5, 4),
(2, 5, 4, 5),
(3, 3, 2, 3);

-- Suggestions
INSERT INTO suggestions (feedback_id, improvement_suggestions, desired_features, legal_challenges, follow_up_consent, follow_up_email) VALUES
(1, 'Improve mobile navigation', 'Video consultations', 'Contract disputes', TRUE, 'john@example.com'),
(2, 'Add more examples', 'Document builder', NULL, FALSE, NULL),
(3, 'Simplify language', 'Legal glossary', 'Understanding regulations', TRUE, 'alex@example.com');

-- Admin Users
INSERT INTO admin_users (username, email, hashed_password) VALUES
('admin', 'admin@lawvriksh.com', '$2a$12$MTExMTExMTExMTExMTEud2Jwcm0uN1F6d2FBRjFqRmJ2d0EudGFq'),
('support', 'support@lawvriksh.com', '$2a$12$MTExMTExMTExMTExMTEud2Jwcm0uN1F6d2FBRjFqRmJ2d0EudGFq');

-- =====================================================
-- 3. Analytical Queries
-- =====================================================

-- 1. User Statistics Summary
SELECT 
    total_users,
    new_users_7d,
    new_users_30d,
    ROUND(avg_satisfaction, 2) AS avg_user_satisfaction
FROM user_statistics;

-- 2. Mobile Experience Issues
SELECT 
    session_id,
    mobile_responsiveness_rating AS mobile_rating,
    mobile_comments,
    task_completion_rating AS task_rating
FROM feedback_analysis
WHERE mobile_responsiveness_rating < 3;

-- 3. Service Quality Correlation
SELECT
    ux.service_quality_rating,
    AVG(ux.overall_satisfaction_rating) AS satisfaction_correlation,
    COUNT(s.id) AS suggestion_count
FROM ux_ratings ux
JOIN suggestions s ON ux.feedback_id = s.feedback_id
GROUP BY ux.service_quality_rating
ORDER BY ux.service_quality_rating DESC;

-- 4. Profession-Based Feedback
SELECT
    u.profession,
    AVG(ui.visual_design_rating) AS avg_design,
    AVG(ux.task_completion_rating) AS avg_task_completion,
    COUNT(DISTINCT f.id) AS feedback_count
FROM users u
JOIN feedback f ON u.email = f.session_id
JOIN ui_ratings ui ON f.id = ui.feedback_id
JOIN ux_ratings ux ON f.id = ux.feedback_id
GROUP BY u.profession;

-- 5. Follow-up Consent Tracking
SELECT
    DATE(created_at) AS feedback_date,
    COUNT(*) AS total_feedback,
    SUM(follow_up_consent) AS consent_count,
    GROUP_CONCAT(follow_up_email) AS consent_emails
FROM suggestions
GROUP BY feedback_date
ORDER BY feedback_date DESC;

-- 6. Navigation Experience Report
SELECT
    ui.ease_of_navigation_rating AS nav_rating,
    COUNT(*) AS response_count,
    AVG(ux.overall_satisfaction_rating) AS avg_satisfaction,
    GROUP_CONCAT(ui.ease_of_navigation_comments SEPARATOR ' | ') AS comments
FROM ui_ratings ui
JOIN ux_ratings ux ON ui.feedback_id = ux.feedback_id
WHERE ui.ease_of_navigation_rating <= 3
GROUP BY nav_rating;

-- 7. Legal Challenges Analysis
SELECT
    TRIM(SUBSTRING_INDEX(legal_challenges, ' ', 3)) AS challenge_keywords,
    COUNT(*) AS frequency,
    AVG(ux.service_quality_rating) AS avg_service_rating
FROM suggestions s
JOIN ux_ratings ux ON s.feedback_id = ux.feedback_id
WHERE legal_challenges IS NOT NULL
GROUP BY challenge_keywords
ORDER BY frequency DESC
LIMIT 5;

-- 8. Admin Dashboard Summary
SELECT
    (SELECT COUNT(*) FROM users) AS total_users,
    (SELECT COUNT(*) FROM creators) AS total_creators,
    (SELECT COUNT(*) FROM feedback) AS total_feedback,
    (SELECT AVG(overall_satisfaction_rating) FROM ux_ratings) AS avg_satisfaction,
    (SELECT COUNT(*) FROM suggestions WHERE follow_up_consent = TRUE) AS follow_up_requests;

-- 9. Detailed Feedback Session Report
SELECT
    f.session_id,
    DATE_FORMAT(f.created_at, '%Y-%m-%d %H:%i') AS feedback_time,
    u.name,
    u.profession,
    ui.visual_design_rating AS design_rating,
    ui.ease_of_navigation_rating AS nav_rating,
    ux.overall_satisfaction_rating AS satisfaction,
    s.desired_features
FROM feedback f
LEFT JOIN users u ON f.session_id = u.email
JOIN ui_ratings ui ON f.id = ui.feedback_id
JOIN ux_ratings ux ON f.id = ux.feedback_id
JOIN suggestions s ON f.id = s.feedback_id
ORDER BY f.created_at DESC
LIMIT 10;

-- 10. Improvement Suggestions Analysis
SELECT
    TRIM(SUBSTRING_INDEX(improvement_suggestions, ' ', 3)) AS suggestion_key,
    COUNT(*) AS frequency,
    AVG(ux.overall_satisfaction_rating) AS avg_satisfaction
FROM suggestions s
JOIN ux_ratings ux ON s.feedback_id = ux.feedback_id
WHERE improvement_suggestions IS NOT NULL
GROUP BY suggestion_key
HAVING frequency > 0
ORDER BY frequency DESC;

-- =====================================================
-- System Verification
-- =====================================================
SELECT 'Database initialized successfully!' AS status;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS feedback_count FROM feedback;