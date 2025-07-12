"""
Pydantic schemas for User model.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import GenderEnum


# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address.")
    name: str = Field(..., min_length=2, max_length=255, description="User's full name.")
    phone_number: str = Field(..., max_length=20, description="User's phone number.")
    gender: Optional[GenderEnum] = Field(default=None, description="User's gender.")
    profession: Optional[str] = Field(default=None, max_length=100, description="User's profession.")
    interest_reason: Optional[str] = Field(default=None, description="Reason for user's interest.")


# Schema for creating a new user
class UserCreate(UserBase):
    pass


# Schema for updating a user (all fields optional)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    name: Optional[str] = Field(default=None, min_length=2, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=20)
    gender: Optional[GenderEnum] = Field(default=None)
    profession: Optional[str] = Field(default=None, max_length=100)
    interest_reason: Optional[str] = Field(default=None)


# Schema for returning a user in the API response
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }