"""
Feedback repository for data access operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from app.models.feedback import Feedback, UIRating, UXRating, Suggestion
from app.schemas.feedback import UIRatingCreate, UXRatingCreate, SuggestionCreate
from app.utils.helpers import calculate_pagination


class FeedbackRepository:
    """Repository for feedback data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_feedback_session(self) -> Feedback:
        """
        Create a new feedback session.
        
        Returns:
            Feedback: The created feedback session
        """
        db_feedback = Feedback()
        self.db.add(db_feedback)
        self.db.commit()
        self.db.refresh(db_feedback)
        return db_feedback
    
    def get_by_session_id(self, session_id: str) -> Optional[Feedback]:
        """
        Get feedback by session ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Feedback: The feedback if found, None otherwise
        """
        return self.db.query(Feedback)\
            .options(
                joinedload(Feedback.ui_rating),
                joinedload(Feedback.ux_rating),
                joinedload(Feedback.suggestion)
            )\
            .filter(Feedback.session_id == session_id)\
            .first()
    
    def get_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """
        Get feedback by ID.
        
        Args:
            feedback_id: Feedback ID
            
        Returns:
            Feedback: The feedback if found, None otherwise
        """
        return self.db.query(Feedback)\
            .options(
                joinedload(Feedback.ui_rating),
                joinedload(Feedback.ux_rating),
                joinedload(Feedback.suggestion)
            )\
            .filter(Feedback.id == feedback_id)\
            .first()
    
    def create_ui_rating(self, feedback_id: int, ui_data: UIRatingCreate) -> UIRating:
        """
        Create UI rating for a feedback session.
        
        Args:
            feedback_id: Feedback ID
            ui_data: UI rating data
            
        Returns:
            UIRating: The created UI rating
        """
        db_ui_rating = UIRating(
            feedback_id=feedback_id,
            **ui_data.dict()
        )
        self.db.add(db_ui_rating)
        self.db.commit()
        self.db.refresh(db_ui_rating)
        return db_ui_rating
    
    def create_ux_rating(self, feedback_id: int, ux_data: UXRatingCreate) -> UXRating:
        """
        Create UX rating for a feedback session.
        
        Args:
            feedback_id: Feedback ID
            ux_data: UX rating data
            
        Returns:
            UXRating: The created UX rating
        """
        db_ux_rating = UXRating(
            feedback_id=feedback_id,
            **ux_data.dict()
        )
        self.db.add(db_ux_rating)
        self.db.commit()
        self.db.refresh(db_ux_rating)
        return db_ux_rating
    
    def create_suggestion(self, feedback_id: int, suggestion_data: SuggestionCreate) -> Suggestion:
        """
        Create suggestion for a feedback session.
        
        Args:
            feedback_id: Feedback ID
            suggestion_data: Suggestion data
            
        Returns:
            Suggestion: The created suggestion
        """
        db_suggestion = Suggestion(
            feedback_id=feedback_id,
            **suggestion_data.dict()
        )
        self.db.add(db_suggestion)
        self.db.commit()
        self.db.refresh(db_suggestion)
        return db_suggestion
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Feedback]:
        """
        Get all feedback with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Feedback]: List of feedback
        """
        return self.db.query(Feedback)\
            .options(
                joinedload(Feedback.ui_rating),
                joinedload(Feedback.ux_rating),
                joinedload(Feedback.suggestion)
            )\
            .order_by(desc(Feedback.created_at))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_paginated(self, page: int = 1, size: int = 10) -> dict:
        """
        Get paginated feedback.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            dict: Paginated feedback with metadata
        """
        total = self.db.query(func.count(Feedback.id)).scalar()
        pagination = calculate_pagination(total, page, size)
        
        feedback = self.db.query(Feedback)\
            .options(
                joinedload(Feedback.ui_rating),
                joinedload(Feedback.ux_rating),
                joinedload(Feedback.suggestion)
            )\
            .order_by(desc(Feedback.created_at))\
            .offset(pagination["offset"])\
            .limit(size)\
            .all()
        
        return {
            "feedback": feedback,
            "pagination": pagination
        }
    
    def delete(self, feedback_id: int) -> bool:
        """
        Delete feedback by ID.
        
        Args:
            feedback_id: Feedback ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_feedback = self.get_by_id(feedback_id)
        if not db_feedback:
            return False
        
        self.db.delete(db_feedback)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """
        Get total number of feedback.
        
        Returns:
            int: Total number of feedback
        """
        return self.db.query(func.count(Feedback.id)).scalar()
    
    def get_recent_feedback(self, days: int = 7) -> List[Feedback]:
        """
        Get recent feedback.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[Feedback]: List of recent feedback
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(Feedback)\
            .options(
                joinedload(Feedback.ui_rating),
                joinedload(Feedback.ux_rating),
                joinedload(Feedback.suggestion)
            )\
            .filter(Feedback.created_at >= cutoff_date)\
            .order_by(desc(Feedback.created_at))\
            .all()
    
    def get_feedback_statistics(self) -> Dict[str, Any]:
        """
        Get feedback statistics.
        
        Returns:
            dict: Feedback statistics
        """
        # Total feedback count
        total_feedback = self.count_total()
        
        # Average ratings
        ui_stats = self.db.query(
            func.avg(UIRating.visual_design_rating).label('avg_visual_design'),
            func.avg(UIRating.ease_of_navigation_rating).label('avg_navigation'),
            func.avg(UIRating.mobile_responsiveness_rating).label('avg_mobile')
        ).join(Feedback).scalar()
        
        ux_stats = self.db.query(
            func.avg(UXRating.overall_satisfaction_rating).label('avg_satisfaction'),
            func.avg(UXRating.task_completion_rating).label('avg_task_completion'),
            func.avg(UXRating.service_quality_rating).label('avg_service_quality')
        ).join(Feedback).scalar()
        
        # Follow-up consent count
        follow_up_count = self.db.query(func.count(Suggestion.id))\
            .filter(Suggestion.follow_up_consent == True)\
            .scalar()
        
        # Recent feedback (last 7 days)
        recent_feedback = len(self.get_recent_feedback(7))
        
        return {
            "total_feedback": total_feedback,
            "recent_feedback": recent_feedback,
            "follow_up_consent_count": follow_up_count,
            "average_ratings": {
                "ui": {
                    "visual_design": round(ui_stats.avg_visual_design or 0, 2),
                    "ease_of_navigation": round(ui_stats.avg_navigation or 0, 2),
                    "mobile_responsiveness": round(ui_stats.avg_mobile or 0, 2)
                },
                "ux": {
                    "overall_satisfaction": round(ux_stats.avg_satisfaction or 0, 2),
                    "task_completion": round(ux_stats.avg_task_completion or 0, 2),
                    "service_quality": round(ux_stats.avg_service_quality or 0, 2)
                }
            }
        }
    
    def get_complete_feedback(self, feedback_id: int) -> Optional[Dict[str, Any]]:
        """
        Get complete feedback with all related data.
        
        Args:
            feedback_id: Feedback ID
            
        Returns:
            dict: Complete feedback data or None
        """
        feedback = self.get_by_id(feedback_id)
        if not feedback:
            return None
        
        return {
            "feedback": feedback,
            "ui_rating": feedback.ui_rating,
            "ux_rating": feedback.ux_rating,
            "suggestion": feedback.suggestion
        } 