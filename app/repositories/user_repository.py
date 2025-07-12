"""
User repository for data access operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.helpers import calculate_pagination


class UserRepository:
    """Repository for user data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: UserCreate) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User creation data
            
        Returns:
            User: The created user
        """
        db_user = User(**user_data.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of users
        """
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_paginated(self, page: int = 1, size: int = 10) -> dict:
        """
        Get paginated users.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            dict: Paginated users with metadata
        """
        total = self.db.query(func.count(User.id)).scalar()
        pagination = calculate_pagination(total, page, size)
        
        users = self.db.query(User)\
            .order_by(desc(User.created_at))\
            .offset(pagination["offset"])\
            .limit(size)\
            .all()
        
        return {
            "users": users,
            "pagination": pagination
        }
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        """
        Update user data.
        
        Args:
            user_id: User ID
            user_data: Updated user data
            
        Returns:
            User: The updated user if found, None otherwise
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        
        for key, value in user_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        
        self.db.delete(db_user)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """
        Get total number of users.
        
        Returns:
            int: Total number of users
        """
        return self.db.query(func.count(User.id)).scalar()
    
    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Search users by name.
        
        Args:
            name: Name to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of matching users
        """
        return self.db.query(User)\
            .filter(User.name.ilike(f"%{name}%"))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_by_profession(self, profession: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get users by profession.
        
        Args:
            profession: Profession to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of users with matching profession
        """
        return self.db.query(User)\
            .filter(User.profession == profession)\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_recent_registrations(self, days: int = 7) -> List[User]:
        """
        Get recent user registrations.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[User]: List of recent registrations
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(User)\
            .filter(User.created_at >= cutoff_date)\
            .order_by(desc(User.created_at))\
            .all() 