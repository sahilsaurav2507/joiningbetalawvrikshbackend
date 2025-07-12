"""
Creator repository for data access operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.creator import Creator
from app.schemas.creator import CreatorCreate
from app.utils.helpers import calculate_pagination


class CreatorRepository:
    """Repository for creator data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, creator_data: CreatorCreate) -> Creator:
        """
        Create a new creator.
        
        Args:
            creator_data: Creator creation data
            
        Returns:
            Creator: The created creator
        """
        db_creator = Creator(**creator_data.dict())
        self.db.add(db_creator)
        self.db.commit()
        self.db.refresh(db_creator)
        return db_creator
    
    def get_by_id(self, creator_id: int) -> Optional[Creator]:
        """
        Get creator by ID.
        
        Args:
            creator_id: Creator ID
            
        Returns:
            Creator: The creator if found, None otherwise
        """
        return self.db.query(Creator).filter(Creator.id == creator_id).first()
    
    def get_by_email(self, email: str) -> Optional[Creator]:
        """
        Get creator by email.
        
        Args:
            email: Creator email
            
        Returns:
            Creator: The creator if found, None otherwise
        """
        return self.db.query(Creator).filter(Creator.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Creator]:
        """
        Get all creators with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Creator]: List of creators
        """
        return self.db.query(Creator).offset(skip).limit(limit).all()
    
    def get_paginated(self, page: int = 1, size: int = 10) -> dict:
        """
        Get paginated creators.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            dict: Paginated creators with metadata
        """
        total = self.db.query(func.count(Creator.id)).scalar()
        pagination = calculate_pagination(total, page, size)
        
        creators = self.db.query(Creator)\
            .order_by(desc(Creator.created_at))\
            .offset(pagination["offset"])\
            .limit(size)\
            .all()
        
        return {
            "creators": creators,
            "pagination": pagination
        }
    
    def update(self, creator_id: int, creator_data: dict) -> Optional[Creator]:
        """
        Update creator data.
        
        Args:
            creator_id: Creator ID
            creator_data: Updated creator data
            
        Returns:
            Creator: The updated creator if found, None otherwise
        """
        db_creator = self.get_by_id(creator_id)
        if not db_creator:
            return None
        
        for key, value in creator_data.items():
            if hasattr(db_creator, key):
                setattr(db_creator, key, value)
        
        self.db.commit()
        self.db.refresh(db_creator)
        return db_creator
    
    def delete(self, creator_id: int) -> bool:
        """
        Delete creator by ID.
        
        Args:
            creator_id: Creator ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_creator = self.get_by_id(creator_id)
        if not db_creator:
            return False
        
        self.db.delete(db_creator)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """
        Get total number of creators.
        
        Returns:
            int: Total number of creators
        """
        return self.db.query(func.count(Creator.id)).scalar()
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Creator]:
        """
        Search creators by name.
        
        Args:
            name: Name to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Creator]: List of matching creators
        """
        return self.db.query(Creator)\
            .filter(Creator.name.ilike(f"%{name}%"))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_profession(self, profession: str, skip: int = 0, limit: int = 100) -> List[Creator]:
        """
        Get creators by profession.
        
        Args:
            profession: Profession to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Creator]: List of creators with matching profession
        """
        return self.db.query(Creator)\
            .filter(Creator.profession == profession)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_recent_registrations(self, days: int = 7) -> List[Creator]:
        """
        Get recent creator registrations.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[Creator]: List of recent registrations
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(Creator)\
            .filter(Creator.created_at >= cutoff_date)\
            .order_by(desc(Creator.created_at))\
            .all() 