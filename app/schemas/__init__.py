"""
Pydantic schemas for LawVriksh Backend API.
"""

from .user import UserCreate, UserResponse, UserList
from .creator import CreatorCreate, CreatorResponse, CreatorList
from .not_interested import NotInterestedCreate, NotInterestedResponse, NotInterestedList
from .feedback import (
    FeedbackCreate, FeedbackResponse, FeedbackList,
    UIRatingCreate, UIRatingResponse,
    UXRatingCreate, UXRatingResponse,
    SuggestionCreate, SuggestionResponse
)
from .admin import AdminLogin, AdminResponse, TokenResponse
from .common import PaginationParams, PaginatedResponse

__all__ = [
    "UserCreate", "UserResponse", "UserList",
    "CreatorCreate", "CreatorResponse", "CreatorList",
    "NotInterestedCreate", "NotInterestedResponse", "NotInterestedList",
    "FeedbackCreate", "FeedbackResponse", "FeedbackList",
    "UIRatingCreate", "UIRatingResponse",
    "UXRatingCreate", "UXRatingResponse",
    "SuggestionCreate", "SuggestionResponse",
    "AdminLogin", "AdminResponse", "TokenResponse",
    "PaginationParams", "PaginatedResponse"
] 