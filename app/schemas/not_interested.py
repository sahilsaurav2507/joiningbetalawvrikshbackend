"""
Not Interested User schemas for request and response validation.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime


class NotInterestedCreate(BaseModel):
    """Schema for creating a not interested user record."""
    
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    not_interested_reason: Optional[str] = Field(None, max_length=100, description="Reason for not being interested")
    improvement_suggestions: Optional[str] = Field(None, description="Suggestions for improvement")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name format."""
        if not v.strip():
            raise ValueError('Name cannot be empty or contain only whitespace')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "not_interested_reason": "Too complex",
                "improvement_suggestions": "Make it simpler to understand"
            }
        }


class NotInterestedResponse(BaseModel):
    """Schema for not interested user response."""
    
    id: int
    name: str
    email: str
    not_interested_reason: Optional[str]
    improvement_suggestions: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "not_interested_reason": "Too complex",
                "improvement_suggestions": "Make it simpler to understand",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }


class NotInterestedList(BaseModel):
    """Schema for paginated not interested user list response."""
    
    not_interested_users: list[NotInterestedResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "not_interested_users": [
                    {
                        "id": 1,
                        "name": "Bob Johnson",
                        "email": "bob.johnson@example.com",
                        "not_interested_reason": "Too complex",
                        "improvement_suggestions": "Make it simpler to understand",
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        } 