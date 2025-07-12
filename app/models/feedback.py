"""
Feedback models for the multi-step feedback system.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid


class Feedback(Base):
    """Main feedback model that holds the session information."""
    
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ui_rating = relationship("UIRating", back_populates="feedback", uselist=False, cascade="all, delete-orphan")
    ux_rating = relationship("UXRating", back_populates="feedback", uselist=False, cascade="all, delete-orphan")
    suggestion = relationship("Suggestion", back_populates="feedback", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, session_id='{self.session_id}')>"


class UIRating(Base):
    """User Interface ratings model."""
    
    __tablename__ = "ui_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    
    # Visual Design Ratings
    visual_design_rating = Column(Integer, nullable=False)
    visual_design_comments = Column(Text, nullable=True)
    
    # Ease of Navigation Ratings
    ease_of_navigation_rating = Column(Integer, nullable=False)
    ease_of_navigation_comments = Column(Text, nullable=True)
    
    # Mobile Responsiveness Ratings
    mobile_responsiveness_rating = Column(Integer, nullable=False)
    mobile_responsiveness_comments = Column(Text, nullable=True)
    
    # Relationships
    feedback = relationship("Feedback", back_populates="ui_rating")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('visual_design_rating >= 1 AND visual_design_rating <= 5', name='check_visual_design_rating'),
        CheckConstraint('ease_of_navigation_rating >= 1 AND ease_of_navigation_rating <= 5', name='check_navigation_rating'),
        CheckConstraint('mobile_responsiveness_rating >= 1 AND mobile_responsiveness_rating <= 5', name='check_mobile_rating'),
    )
    
    def __repr__(self):
        return f"<UIRating(id={self.id}, feedback_id={self.feedback_id})>"


class UXRating(Base):
    """User Experience ratings model."""
    
    __tablename__ = "ux_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    
    # Overall Satisfaction Ratings
    overall_satisfaction_rating = Column(Integer, nullable=False)
    overall_satisfaction_comments = Column(Text, nullable=True)
    
    # Task Completion Ratings
    task_completion_rating = Column(Integer, nullable=False)
    task_completion_comments = Column(Text, nullable=True)
    
    # Service Quality Ratings
    service_quality_rating = Column(Integer, nullable=False)
    service_quality_comments = Column(Text, nullable=True)
    
    # Relationships
    feedback = relationship("Feedback", back_populates="ux_rating")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('overall_satisfaction_rating >= 1 AND overall_satisfaction_rating <= 5', name='check_satisfaction_rating'),
        CheckConstraint('task_completion_rating >= 1 AND task_completion_rating <= 5', name='check_task_rating'),
        CheckConstraint('service_quality_rating >= 1 AND service_quality_rating <= 5', name='check_quality_rating'),
    )
    
    def __repr__(self):
        return f"<UXRating(id={self.id}, feedback_id={self.feedback_id})>"


class Suggestion(Base):
    """Suggestions and additional feedback model."""
    
    __tablename__ = "suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    
    # Suggestions and Needs
    liked_features = Column(Text, nullable=True)
    improvement_suggestions = Column(Text, nullable=True)
    desired_features = Column(Text, nullable=True)
    legal_challenges = Column(Text, nullable=True)
    
    # Additional Comments
    additional_comments = Column(Text, nullable=True)
    
    # Follow-up Information
    follow_up_consent = Column(Boolean, default=False)
    follow_up_email = Column(String(255), nullable=True)
    
    # Relationships
    feedback = relationship("Feedback", back_populates="suggestion")
    
    def __repr__(self):
        return f"<Suggestion(id={self.id}, feedback_id={self.feedback_id})>" 