#!/usr/bin/env python3
"""
Complete database setup script for LawVriksh Backend
This script will create the database, tables, and initial data
"""
import os
import sys
import mysql.connector
from mysql.connector import Error
import bcrypt
import getpass
from pathlib import Path
from typing import Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_setup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = None
        self.database_name = "lawvriksh_db"
        self.connection = None
        
    def get_database_credentials(self):
        """Get database credentials from user"""
        print("🔐 Database Setup - Enter MySQL credentials")
        
        # Get host (default: localhost)
        host_input = input(f"MySQL Host (default: {self.host}): ").strip()
        if host_input:
            self.host = host_input
            
        # Get port (default: 3306)
        port_input = input(f"MySQL Port (default: {self.port}): ").strip()
        if port_input:
            try:
                self.port = int(port_input)
            except ValueError:
                logger.warning("Invalid port, using default 3306")
                
        # Get username (default: root)
        user_input = input(f"MySQL Username (default: {self.user}): ").strip()
        if user_input:
            self.user = user_input
            
        # Get password
        self.password = getpass.getpass("MySQL Password: ")
        
        # Get database name
        db_input = input(f"Database Name (default: {self.database_name}): ").strip()
        if db_input:
            self.database_name = db_input
    
    def connect_to_mysql(self, use_database: bool = False):
        """Connect to MySQL server"""
        try:
            config = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_unicode_ci'
            }
            
            if use_database:
                config['database'] = self.database_name
                
            self.connection = mysql.connector.connect(**config)
            
            if self.connection.is_connected():
                logger.info(f"✅ Connected to MySQL server at {self.host}:{self.port}")
                return True
                
        except Error as e:
            logger.error(f"❌ Error connecting to MySQL: {e}")
            return False
    
    def execute_sql_file(self, file_path: str):
        """Execute SQL commands from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Split SQL commands by semicolon
            commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
            
            cursor = self.connection.cursor()
            
            for command in commands:
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        self.connection.commit()
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            logger.warning(f"Warning executing command: {e}")
            
            cursor.close()
            logger.info(f"✅ Successfully executed SQL file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error executing SQL file {file_path}: {e}")
            return False
    
    def execute_sql_command(self, command: str):
        """Execute a single SQL command"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(command)
            self.connection.commit()
            
            # Fetch results if it's a SELECT query
            if command.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            
            cursor.close()
            return True
            
        except Error as e:
            logger.error(f"❌ Error executing SQL command: {e}")
            return False
    
    def create_database(self):
        """Create the main database"""
        logger.info(f"🏗️ Creating database: {self.database_name}")
        
        sql_command = f"""
        CREATE DATABASE IF NOT EXISTS {self.database_name} 
        CHARACTER SET utf8mb4 
        COLLATE utf8mb4_unicode_ci
        """
        
        return self.execute_sql_command(sql_command)
    
    def generate_password_hash(self, password: str) -> str:
        """Generate bcrypt hash for password"""
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def create_admin_user(self):
        """Create default admin user"""
        logger.info("👤 Creating default admin user")
        
        # Get admin password
        print("\n🔐 Set up admin user credentials:")
        admin_username = input("Admin Username (default: admin): ").strip() or "admin"
        admin_email = input("Admin Email (default: admin@lawvriksh.com): ").strip() or "admin@lawvriksh.com"
        admin_password = getpass.getpass("Admin Password (default: change-this-password): ") or "change-this-password"
        
        # Generate password hash
        password_hash = self.generate_password_hash(admin_password)
        
        # Insert admin user
        sql_command = f"""
        INSERT INTO admin_users (username, email, password_hash, is_superuser, is_active) 
        VALUES ('{admin_username}', '{admin_email}', '{password_hash}', TRUE, TRUE)
        ON DUPLICATE KEY UPDATE 
        password_hash = '{password_hash}',
        is_active = TRUE
        """
        
        if self.execute_sql_command(sql_command):
            logger.info(f"✅ Admin user created: {admin_username} ({admin_email})")
            return True
        return False
    
    def verify_setup(self):
        """Verify database setup"""
        logger.info("🔍 Verifying database setup...")
        
        # Check tables
        tables_query = "SHOW TABLES"
        tables = self.execute_sql_command(tables_query)
        
        if tables:
            logger.info(f"✅ Found {len(tables)} tables:")
            for table in tables:
                logger.info(f"   - {table[0]}")
        
        # Check admin user
        admin_query = "SELECT username, email, is_superuser FROM admin_users WHERE username = 'admin'"
        admin_result = self.execute_sql_command(admin_query)
        
        if admin_result:
            admin_data = admin_result[0]
            logger.info(f"✅ Admin user verified: {admin_data[0]} ({admin_data[1]})")
        
        return True
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("🔌 Database connection closed")

def create_sql_files():
    """Create all necessary SQL files"""
    
    # Main database schema
    schema_sql = """-- LawVriksh Database Schema
-- Create database with proper character set and collation
CREATE DATABASE IF NOT EXISTS lawvriksh_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE lawvriksh_db;

-- Create admin users table
CREATE TABLE IF NOT EXISTS admin_users (
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
CREATE TABLE IF NOT EXISTS refresh_tokens (
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
"""

    # Write schema file
    with open('sql/01_schema.sql', 'w', encoding='utf-8') as f:
        f.write(schema_sql)
    
    # Sample data file
    sample_data_sql = """-- Sample data for testing
USE lawvriksh_db;

-- Insert sample users (for testing)
INSERT IGNORE INTO users (full_name, email, phone, profession, city, state) VALUES
('John Doe', 'john.doe@example.com', '+91-9876543210', 'Lawyer', 'Mumbai', 'Maharashtra'),
('Jane Smith', 'jane.smith@example.com', '+91-9876543211', 'Law Student', 'Delhi', 'Delhi'),
('Mike Johnson', 'mike.johnson@example.com', '+91-9876543212', 'Legal Consultant', 'Bangalore', 'Karnataka');

-- Insert sample creators (for testing)
INSERT IGNORE INTO creators (full_name, email, phone, content_type, experience_level) VALUES
('Alice Brown', 'alice.brown@example.com', '+91-9876543213', 'Video Content', 'Intermediate'),
('Bob Wilson', 'bob.wilson@example.com', '+91-9876543214', 'Written Content', 'Expert'),
('Carol Davis', 'carol.davis@example.com', '+91-9876543215', 'Podcast', 'Beginner');
"""

    # Write sample data file
    with open('sql/02_sample_data.sql', 'w', encoding='utf-8') as f:
        f.write(sample_data_sql)

def main():
    """Main setup function"""
    print("🚀 LawVriksh Database Setup Script")
    print("=" * 50)
    
    # Create SQL directory if it doesn't exist
    os.makedirs('sql', exist_ok=True)
    
    # Create SQL files
    logger.info("📝 Creating SQL files...")
    create_sql_files()
    
    # Initialize database setup
    db_setup = DatabaseSetup()
    
    try:
        # Get database credentials
        db_setup.get_database_credentials()
        
        # Connect to MySQL (without database)
        if not db_setup.connect_to_mysql(use_database=False):
            logger.error("❌ Failed to connect to MySQL server")
            return False
        
        # Create database
        if not db_setup.create_database():
            logger.error("❌ Failed to create database")
            return False
        
        # Close connection and reconnect with database
        db_setup.close_connection()
        
        if not db_setup.connect_to_mysql(use_database=True):
            logger.error("❌ Failed to connect to database")
            return False
        
        # Execute schema file
        logger.info("🏗️ Creating database schema...")
        if not db_setup.execute_sql_file('sql/01_schema.sql'):
            logger.error("❌ Failed to create schema")
            return False
        
        # Create admin user
        if not db_setup.create_admin_user():
            logger.error("❌ Failed to create admin user")
            return False
        
        # Ask if user wants sample data
        add_sample = input("\n📊 Add sample data for testing? (y/N): ").strip().lower()
        if add_sample in ['y', 'yes']:
            logger.info("📊 Adding sample data...")
            db_setup.execute_sql_file('sql/02_sample_data.sql')
        
        # Verify setup
        db_setup.verify_setup()
        
        # Update .env file
        update_env_file(db_setup)
        
        logger.info("\n🎉 Database setup completed successfully!")
        logger.info("📋 Next steps:")
        logger.info("   1. Update your .env file with the database credentials")
        logger.info("   2. Run: python -c \"from app.database import init_db; init_db()\"")
        logger.info("   3. Start your FastAPI application")
        
        return True
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Setup interrupted by user")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False
    finally:
        db_setup.close_connection()

def update_env_file(db_setup):
    """Update .env file with database configuration"""
    logger.info("📝 Updating .env file...")
    
    env_content = f"""# Database Configuration
DATABASE_URL=mysql+pymysql://{db_setup.user}:{db_setup.password}@{db_setup.host}:{db_setup.port}/{db_setup.database_name}
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_HOST={db_setup.host}
DATABASE_PORT={db_setup.port}
DATABASE_NAME={db_setup.database_name}
DATABASE_USER={db_setup.user}
DATABASE_PASSWORD={db_setup.password}

# Security Configuration
SECRET_KEY=lawvrikshjksndfjsdsjkfcsdmlcmskdnjdsjnsdkc3874hbefsyf89j894397
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,https://lawvriksh.com,https://www.lawvriksh.com
CORS_ALLOW_CREDENTIALS=true

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
ADMIN_RATE_LIMIT_PER_MINUTE=100

# Environment
ENVIRONMENT=development
DEBUG=true

# Admin Default Credentials
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_EMAIL=admin@lawvriksh.com
DEFAULT_ADMIN_PASSWORD=change-this-password

# Server Configuration
HOST=0.0.0.0
PORT=8000
"""
    
    # Backup existing .env file
    if os.path.exists('.env'):
        os.rename('.env', '.env.backup')
        logger.info("📋 Existing .env file backed up as .env.backup")
    
    # Write new .env file
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    logger.info("✅ .env file updated successfully")

if __name__ == "__main__":
    main()
