"""
Creator schemas for request and response validation.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from app.models.user import GenderEnum


class CreatorCreate(BaseModel):
    """Schema for creating a new creator."""
    
    name: str = Field(..., min_length=1, max_length=255, description="Creator's full name")
    email: EmailStr = Field(..., description="Creator's email address")
    phone_number: str = Field(..., min_length=10, max_length=20, description="Creator's phone number")
    gender: Optional[GenderEnum] = Field(None, description="Creator's gender")
    profession: Optional[str] = Field(None, max_length=100, description="Creator's profession")
    interest_reason: Optional[str] = Field(None, description="Reason for interest in LawVriksh")
    
    @validator('phone_number')
    def validate_phone_number(cls, v):
        """Validate phone number format."""
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, v))
        if len(digits_only) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name format."""
        if not v.strip():
            raise ValueError('Name cannot be empty or contain only whitespace')
        return v.strip()
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone_number": "9876543210",
                "gender": "Female",
                "profession": "Lawyer",
                "interest_reason": "Interested in creating legal content"
            }
        }


class CreatorResponse(BaseModel):
    """Schema for creator response."""
    
    id: int
    name: str
    email: str
    phone_number: str
    gender: Optional[GenderEnum]
    profession: Optional[str]
    interest_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone_number": "9876543210",
                "gender": "Female",
                "profession": "Lawyer",
                "interest_reason": "Interested in creating legal content",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }


class CreatorList(BaseModel):
    """Schema for paginated creator list response."""
    
    creators: list[CreatorResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "creators": [
                    {
                        "id": 1,
                        "name": "Jane Smith",
                        "email": "jane.smith@example.com",
                        "phone_number": "9876543210",
                        "gender": "Female",
                        "profession": "Lawyer",
                        "interest_reason": "Interested in creating legal content",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        } 