"""
Feedback schemas for the multi-step feedback system.
"""

from typing import Optional
from pydantic import BaseModel, Field, validator, EmailStr
from datetime import datetime


class FeedbackCreate(BaseModel):
    """Schema for creating a new feedback session."""
    
    pass  # No fields needed, session_id is auto-generated


class FeedbackResponse(BaseModel):
    """Schema for feedback response."""
    
    id: int
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UIRatingCreate(BaseModel):
    """Schema for UI ratings submission."""
    
    visual_design_rating: int = Field(..., ge=1, le=5, description="Visual design rating (1-5)")
    visual_design_comments: Optional[str] = Field(None, description="Comments for visual design (required if rating ≤ 2)")
    ease_of_navigation_rating: int = Field(..., ge=1, le=5, description="Ease of navigation rating (1-5)")
    ease_of_navigation_comments: Optional[str] = Field(None, description="Comments for navigation (required if rating ≤ 2)")
    mobile_responsiveness_rating: int = Field(..., ge=1, le=5, description="Mobile responsiveness rating (1-5)")
    mobile_responsiveness_comments: Optional[str] = Field(None, description="Comments for mobile responsiveness (required if rating ≤ 2)")
    
    @validator('visual_design_comments')
    def validate_visual_design_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'visual_design_rating' in values and values['visual_design_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    @validator('ease_of_navigation_comments')
    def validate_navigation_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'ease_of_navigation_rating' in values and values['ease_of_navigation_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    @validator('mobile_responsiveness_comments')
    def validate_mobile_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'mobile_responsiveness_rating' in values and values['mobile_responsiveness_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "visual_design_rating": 4,
                "visual_design_comments": None,
                "ease_of_navigation_rating": 3,
                "ease_of_navigation_comments": "Could be more intuitive",
                "mobile_responsiveness_rating": 5,
                "mobile_responsiveness_comments": None
            }
        }


class UIRatingResponse(BaseModel):
    """Schema for UI ratings response."""
    
    id: int
    feedback_id: int
    visual_design_rating: int
    visual_design_comments: Optional[str]
    ease_of_navigation_rating: int
    ease_of_navigation_comments: Optional[str]
    mobile_responsiveness_rating: int
    mobile_responsiveness_comments: Optional[str]
    
    class Config:
        from_attributes = True


class UXRatingCreate(BaseModel):
    """Schema for UX ratings submission."""
    
    overall_satisfaction_rating: int = Field(..., ge=1, le=5, description="Overall satisfaction rating (1-5)")
    overall_satisfaction_comments: Optional[str] = Field(None, description="Comments for satisfaction (required if rating ≤ 2)")
    task_completion_rating: int = Field(..., ge=1, le=5, description="Task completion rating (1-5)")
    task_completion_comments: Optional[str] = Field(None, description="Comments for task completion (required if rating ≤ 2)")
    service_quality_rating: int = Field(..., ge=1, le=5, description="Service quality rating (1-5)")
    service_quality_comments: Optional[str] = Field(None, description="Comments for service quality (required if rating ≤ 2)")
    
    @validator('overall_satisfaction_comments')
    def validate_satisfaction_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'overall_satisfaction_rating' in values and values['overall_satisfaction_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    @validator('task_completion_comments')
    def validate_task_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'task_completion_rating' in values and values['task_completion_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    @validator('service_quality_comments')
    def validate_quality_comments(cls, v, values):
        """Validate that comments are provided for low ratings."""
        if 'service_quality_rating' in values and values['service_quality_rating'] <= 2 and not v:
            raise ValueError('Comments are required for ratings of 2 or below')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "overall_satisfaction_rating": 4,
                "overall_satisfaction_comments": None,
                "task_completion_rating": 3,
                "task_completion_comments": "Some tasks were confusing",
                "service_quality_rating": 5,
                "service_quality_comments": None
            }
        }


class UXRatingResponse(BaseModel):
    """Schema for UX ratings response."""
    
    id: int
    feedback_id: int
    overall_satisfaction_rating: int
    overall_satisfaction_comments: Optional[str]
    task_completion_rating: int
    task_completion_comments: Optional[str]
    service_quality_rating: int
    service_quality_comments: Optional[str]
    
    class Config:
        from_attributes = True


class SuggestionCreate(BaseModel):
    """Schema for suggestions submission."""
    
    liked_features: Optional[str] = Field(None, description="What do you like most?")
    improvement_suggestions: Optional[str] = Field(None, description="Suggestions for improvement")
    desired_features: Optional[str] = Field(None, description="Desired features")
    legal_challenges: Optional[str] = Field(None, description="Legal challenges you face")
    additional_comments: Optional[str] = Field(None, description="Any additional comments")
    follow_up_consent: bool = Field(False, description="Consent for follow-up")
    follow_up_email: Optional[EmailStr] = Field(None, description="Email for follow-up (required if consent is True)")
    
    @validator('follow_up_email')
    def validate_follow_up_email(cls, v, values):
        """Validate that email is provided if consent is given."""
        if values.get('follow_up_consent') and not v:
            raise ValueError('Email is required when follow-up consent is given')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "liked_features": "Easy to use interface",
                "improvement_suggestions": "Add more legal document templates",
                "desired_features": "Video consultations",
                "legal_challenges": "Understanding complex legal terms",
                "additional_comments": "Great platform overall",
                "follow_up_consent": True,
                "follow_up_email": "user@example.com"
            }
        }


class SuggestionResponse(BaseModel):
    """Schema for suggestions response."""
    
    id: int
    feedback_id: int
    liked_features: Optional[str]
    improvement_suggestions: Optional[str]
    desired_features: Optional[str]
    legal_challenges: Optional[str]
    additional_comments: Optional[str]
    follow_up_consent: bool
    follow_up_email: Optional[str]
    
    class Config:
        from_attributes = True


class FeedbackList(BaseModel):
    """Schema for paginated feedback list response."""
    
    feedback: list[FeedbackResponse]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        schema_extra = {
            "example": {
                "feedback": [
                    {
                        "id": 1,
                        "session_id": "uuid-string",
                        "created_at": "2024-01-01T00:00:00Z"
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        } 