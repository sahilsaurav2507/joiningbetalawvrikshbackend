-- Step 3: Insert default admin
INSERT INTO admin_users (username, email, password_hash, is_superuser, is_active) 
VALUES (
    'admin', 
    'admin@lawvriksh.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS',
    TRUE,
    TRUE
);