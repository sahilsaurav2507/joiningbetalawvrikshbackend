"""
Admin repository for data access operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime
from app.models.admin import AdminUser
from app.schemas.admin import AdminCreate
from app.utils.security import get_password_hash
from app.utils.helpers import calculate_pagination


class AdminRepository:
    """Repository for admin user data access operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, admin_data: AdminCreate) -> AdminUser:
        """
        Create a new admin user.
        
        Args:
            admin_data: Admin creation data
            
        Returns:
            AdminUser: The created admin user
        """
        hashed_password = get_password_hash(admin_data.password)
        db_admin = AdminUser(
            username=admin_data.username,
            email=admin_data.email,
            hashed_password=hashed_password
        )
        self.db.add(db_admin)
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin
    
    def get_by_id(self, admin_id: int) -> Optional[AdminUser]:
        """
        Get admin user by ID.
        
        Args:
            admin_id: Admin ID
            
        Returns:
            AdminUser: The admin user if found, None otherwise
        """
        return self.db.query(AdminUser).filter(AdminUser.id == admin_id).first()
    
    def get_by_username(self, username: str) -> Optional[AdminUser]:
        """
        Get admin user by username.
        
        Args:
            username: Admin username
            
        Returns:
            AdminUser: The admin user if found, None otherwise
        """
        return self.db.query(AdminUser).filter(AdminUser.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[AdminUser]:
        """
        Get admin user by email.
        
        Args:
            email: Admin email
            
        Returns:
            AdminUser: The admin user if found, None otherwise
        """
        return self.db.query(AdminUser).filter(AdminUser.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[AdminUser]:
        """
        Get all admin users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[AdminUser]: List of admin users
        """
        return self.db.query(AdminUser).offset(skip).limit(limit).all()
    
    def get_paginated(self, page: int = 1, size: int = 10) -> dict:
        """
        Get paginated admin users.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            dict: Paginated admin users with metadata
        """
        total = self.db.query(func.count(AdminUser.id)).scalar()
        pagination = calculate_pagination(total, page, size)
        
        admins = self.db.query(AdminUser)\
            .order_by(desc(AdminUser.created_at))\
            .offset(pagination["offset"])\
            .limit(size)\
            .all()
        
        return {
            "admins": admins,
            "pagination": pagination
        }
    
    def update(self, admin_id: int, admin_data: dict) -> Optional[AdminUser]:
        """
        Update admin user data.
        
        Args:
            admin_id: Admin ID
            admin_data: Updated admin data
            
        Returns:
            AdminUser: The updated admin user if found, None otherwise
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return None
        
        for key, value in admin_data.items():
            if hasattr(db_admin, key):
                setattr(db_admin, key, value)
        
        self.db.commit()
        self.db.refresh(db_admin)
        return db_admin
    
    def update_password(self, admin_id: int, new_password: str) -> bool:
        """
        Update admin user password.
        
        Args:
            admin_id: Admin ID
            new_password: New password
            
        Returns:
            bool: True if updated, False if not found
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        db_admin.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True
    
    def update_last_login(self, admin_id: int) -> bool:
        """
        Update admin user last login timestamp.
        
        Args:
            admin_id: Admin ID
            
        Returns:
            bool: True if updated, False if not found
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        db_admin.last_login = datetime.utcnow()
        self.db.commit()
        return True
    
    def delete(self, admin_id: int) -> bool:
        """
        Delete admin user by ID.
        
        Args:
            admin_id: Admin ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        self.db.delete(db_admin)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        """
        Get total number of admin users.
        
        Returns:
            int: Total number of admin users
        """
        return self.db.query(func.count(AdminUser.id)).scalar()
    
    def search_by_username(self, username: str, skip: int = 0, limit: int = 100) -> List[AdminUser]:
        """
        Search admin users by username.
        
        Args:
            username: Username to search for
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[AdminUser]: List of matching admin users
        """
        return self.db.query(AdminUser)\
            .filter(AdminUser.username.ilike(f"%{username}%"))\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def get_active_admins(self) -> List[AdminUser]:
        """
        Get all active admin users.
        
        Returns:
            List[AdminUser]: List of active admin users
        """
        return self.db.query(AdminUser).filter(AdminUser.is_active == True).all()
    
    def deactivate_admin(self, admin_id: int) -> bool:
        """
        Deactivate an admin user.
        
        Args:
            admin_id: Admin ID
            
        Returns:
            bool: True if deactivated, False if not found
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        db_admin.is_active = False
        self.db.commit()
        return True
    
    def activate_admin(self, admin_id: int) -> bool:
        """
        Activate an admin user.
        
        Args:
            admin_id: Admin ID
            
        Returns:
            bool: True if activated, False if not found
        """
        db_admin = self.get_by_id(admin_id)
        if not db_admin:
            return False
        
        db_admin.is_active = True
        self.db.commit()
        return True
    
    def get_recent_logins(self, days: int = 7) -> List[AdminUser]:
        """
        Get admin users with recent logins.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[AdminUser]: List of admin users with recent logins
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(AdminUser)\
            .filter(AdminUser.last_login >= cutoff_date)\
            .order_by(desc(AdminUser.last_login))\
            .all()
    
    def create_default_admin(self, username: str, email: str, password: str) -> AdminUser:
        """
        Create a default admin user.
        
        Args:
            username: Admin username
            email: Admin email
            password: Admin password
            
        Returns:
            AdminUser: The created admin user
        """
        # Check if admin already exists
        existing_admin = self.get_by_username(username)
        if existing_admin:
            return existing_admin
        
        admin_data = AdminCreate(
            username=username,
            email=email,
            password=password
        )
        
        return self.create(admin_data) 