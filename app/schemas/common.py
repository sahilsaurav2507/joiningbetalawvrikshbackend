"""
Common schemas used across the application.
"""

from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters for API endpoints."""
    
    page: int = Field(default=1, ge=1, description="Page number (starts from 1)")
    size: int = Field(default=10, ge=1, le=100, description="Number of items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""
    
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @property
    def has_next(self) -> bool:
        """Check if there's a next page."""
        return self.page < self.pages
    
    @property
    def has_prev(self) -> bool:
        """Check if there's a previous page."""
        return self.page > 1


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    
    success: bool = True
    message: str = "Operation completed successfully"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow) 