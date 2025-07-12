"""
Not Interested User model for users who decline to join.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class NotInterestedUser(Base):
    """Not Interested User model for users who decline to join."""
    
    __tablename__ = "not_interested_users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    not_interested_reason = Column(String(100), nullable=True)
    improvement_suggestions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<NotInterestedUser(id={self.id}, name='{self.name}', email='{self.email}')>" 