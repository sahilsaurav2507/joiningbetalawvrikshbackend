"""
Creator model for creator waiting list registrations.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
from .user import GenderEnum


class Creator(Base):
    """Creator model for creator waiting list registrations."""
    
    __tablename__ = "creators"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=True)
    profession = Column(String(100), nullable=True)
    interest_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Creator(id={self.id}, name='{self.name}', email='{self.email}')>" 