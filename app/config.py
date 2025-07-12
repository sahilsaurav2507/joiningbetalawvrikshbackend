"""
Configuration settings for LawVriksh Backend API
"""
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Database Configuration
    DATABASE_URL: str = Field(..., description="Database connection URL")
    DATABASE_POOL_SIZE: int = Field(default=10, description="Database connection pool size")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Database max overflow connections")
    DATABASE_HOST: str = Field(default="localhost", description="Database host")
    DATABASE_PORT: int = Field(default=3306, description="Database port")
    DATABASE_NAME: str = Field(..., description="Database name")
    DATABASE_USER: str = Field(..., description="Database username")
    DATABASE_PASSWORD: str = Field(..., description="Database password")
    
    # Security Configuration
    SECRET_KEY: str = Field(..., description="Secret key for JWT tokens")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Access token expiration in minutes")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Refresh token expiration in days")
    
    # CORS Configuration - Fixed parsing
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000;http://127.0.0.1:3000", 
        description="CORS origins separated by semicolon"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Allow CORS credentials")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Rate limit per minute")
    ADMIN_RATE_LIMIT_PER_MINUTE: int = Field(default=100, description="Admin rate limit per minute")
    
    # Environment
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Admin Default Credentials
    DEFAULT_ADMIN_USERNAME: str = Field(default="admin", description="Default admin username")
    DEFAULT_ADMIN_EMAIL: str = Field(default="admin@lawvriksh.com", description="Default admin email")
    DEFAULT_ADMIN_PASSWORD: str = Field(default="change-this-password", description="Default admin password")
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    @validator('CORS_ORIGINS')
    def parse_cors_origins(cls, v):
        """Parse CORS origins from semicolon-separated string"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(';') if origin.strip()]
        return v
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        """Validate database URL format"""
        if not v.startswith(('mysql+pymysql://', 'mysql://', 'postgresql://', 'sqlite:///')):
            raise ValueError('DATABASE_URL must start with a valid database scheme')
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [origin.strip() for origin in self.CORS_ORIGINS.split(';') if origin.strip()]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Global settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Get application settings (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

# For backward compatibility
settings = get_settings()
