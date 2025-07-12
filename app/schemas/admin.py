"""
Admin schemas for authentication and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class AdminLogin(BaseModel):
    """Schema for admin login."""
    
    username: str = Field(..., description="Admin username")
    password: str = Field(..., description="Admin password")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "secure_password"
            }
        }


class AdminResponse(BaseModel):
    """Schema for admin response."""
    
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "admin",
                "email": "admin@lawvriksh.com",
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "last_login": "2024-01-01T12:00:00Z"
            }
        }


class TokenResponse(BaseModel):
    """Schema for token response."""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class AdminCreate(BaseModel):
    """Schema for creating a new admin user."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Admin username")
    email: EmailStr = Field(..., description="Admin email address")
    password: str = Field(..., min_length=8, description="Admin password")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "newadmin",
                "email": "newadmin@lawvriksh.com",
                "password": "secure_password123"
            }
        } 