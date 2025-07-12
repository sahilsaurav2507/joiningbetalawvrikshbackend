"""
Not Interested repository for data access operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.not_interested import NotInterestedUser
from app.schemas.not_interested import NotInterestedCreate
from app.utils.helpers import calculate_pagination


class NotInterestedRepository:
    """Repository for not interested user data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, not_interested_data: NotInterestedCreate) -> NotInterestedUser:
        """
        Create a new not interested user record.
        
        Args:
            not_interested_data: Not interested user creation data
            
        Returns:
            NotInterestedUser: The created record
        """
        db_not_interested = NotInterestedUser(**not_interested_data.dict())
        self.db.add(db_not_interested)
        self.db.commit()
        self.db.refresh(db_not_interested)
        return db_not_interested
    
    def get_by_id(self, record_id: int) -> Optional[NotInterestedUser]:
        """
        Get not interested user by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            NotInterestedUser: The record if found, None otherwise
        """
        return self.db.query(NotInterestedUser).filter(NotInterestedUser.id == record_id).first()
    
    def get_by_email(self, email: str) -> Optional[NotInterestedUser]:
        """
        Get not interested user by email.
        
        Args:
            email: User email
            
        Returns:
            NotInterestedUser: The record if found, None otherwise
        """
        return self.db.query(NotInterestedUser).filter(NotInterestedUser.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[NotInterestedUser]:
        """
        Get all not interested users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[NotInterestedUser]: List of records
        """
        return self.db.query(NotInterestedUser).offset(skip).limit(limit).all()
    
    def get_paginated(self, page: int = 1, size: int = 10) -> dict:
        """
        Get paginated not interested users.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            dict: Paginated records with metadata
        """
        total = self.db.query(func.count(NotInterestedUser.id)).scalar()
        pagination = calculate_pagination(total, page, size)
        
        records = self.db.query(NotInterestedUser)\
            .order_by(desc(NotInterestedUser.created_at))\
            .offset(pagination["offset"])\
            .limit(size)\
            .all()
        
        return {
            "not_interested_users": records,
            "pagination": pagination
        }
    
    def update(self, record_id: int, record_data: dict) -> Optional[NotInterestedUser]:
        """
        Update not interested user data.
        
        Args:
            record_id: Record ID
            record_data: Updated record data
            
        Returns:
            NotInterestedUser: The updated record if found, None otherwise
        """
        db_record = self.get_by_id(record_id)
        if not db_record:
            return None
        
        for key, value in record_data.items():
            if hasattr(db_record, key):
                setattr(db_record, key, value)
        
        self.db.commit()
        self.db.refresh(db_record)
        return db_record
    
    def delete(self, record_id: int) -> bool:
        """
        Delete not interested user by ID.
        
        Args:
            record_id: Record ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_record = self.get_by_id(record_id)
        if not db_record:
            return False
        
        self.db.delete(db_record)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """
        Get total number of not interested users.
        
        Returns:
            int: Total number of records
        """
        return self.db.query(func.count(NotInterestedUser.id)).scalar()
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[NotInterestedUser]:
        """
        Search not interested users by name.
        
        Args:
            name: Name to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[NotInterestedUser]: List of matching records
        """
        return self.db.query(NotInterestedUser)\
            .filter(NotInterestedUser.name.ilike(f"%{name}%"))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_reason(self, reason: str, skip: int = 0, limit: int = 100) -> List[NotInterestedUser]:
        """
        Get not interested users by reason.
        
        Args:
            reason: Reason to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[NotInterestedUser]: List of records with matching reason
        """
        return self.db.query(NotInterestedUser)\
            .filter(NotInterestedUser.not_interested_reason == reason)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_recent_submissions(self, days: int = 7) -> List[NotInterestedUser]:
        """
        Get recent not interested submissions.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[NotInterestedUser]: List of recent submissions
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(NotInterestedUser)\
            .filter(NotInterestedUser.created_at >= cutoff_date)\
            .order_by(desc(NotInterestedUser.created_at))\
            .all()
    
    def get_reason_statistics(self) -> dict:
        """
        Get statistics by reason.
        
        Returns:
            dict: Statistics grouped by reason
        """
        from sqlalchemy import case
        
        # Count by reason
        reason_counts = self.db.query(
            NotInterestedUser.not_interested_reason,
            func.count(NotInterestedUser.id).label('count')
        ).group_by(NotInterestedUser.not_interested_reason).all()
        
        # Count total
        total = self.count_total()
        
        # Calculate percentages
        statistics = {}
        for reason, count in reason_counts:
            percentage = (count / total * 100) if total > 0 else 0
            statistics[reason or "No reason provided"] = {
                "count": count,
                "percentage": round(percentage, 2)
            }
        
        return {
            "total": total,
            "by_reason": statistics
        } 