"""
User service for business logic operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserList
from app.utils.validators import validate_email, validate_phone_number, validate_name
from app.utils.helpers import sanitize_input


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """
        Register a new user for the waiting list.
        
        Args:
            user_data: User registration data
            
        Returns:
            UserResponse: Created user data if successful, None otherwise
        """
        # Validate input data
        validation_result = self._validate_user_data(user_data)
        if not validation_result["valid"]:
            raise ValueError(validation_result["error"])
        
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Sanitize input data
        sanitized_data = self._sanitize_user_data(user_data)
        
        try:
            # Create user
            db_user = self.user_repo.create(sanitized_data)
            return UserResponse.from_orm(db_user)
        except Exception as e:
            # Log the error (in production, use proper logging)
            raise ValueError(f"Failed to create user: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            UserResponse: User data if found, None otherwise
        """
        db_user = self.user_repo.get_by_id(user_id)
        if not db_user:
            return None
        
        return UserResponse.from_orm(db_user)
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            UserResponse: User data if found, None otherwise
        """
        db_user = self.user_repo.get_by_email(email)
        if not db_user:
            return None
        
        return UserResponse.from_orm(db_user)
    
    def get_users_paginated(self, page: int = 1, size: int = 10) -> UserList:
        """
        Get paginated users.
        
        Args:
            page: Page number
            size: Page size
            
        Returns:
            UserList: Paginated users with metadata
        """
        result = self.user_repo.get_paginated(page, size)
        
        users = [UserResponse.from_orm(user) for user in result["users"]]
        pagination = result["pagination"]
        
        return UserList(
            users=users,
            total=pagination["total"],
            page=pagination["page"],
            size=pagination["size"],
            pages=pagination["pages"]
        )
    
    def search_users_by_name(self, name: str, page: int = 1, size: int = 10) -> UserList:
        """
        Search users by name.
        
        Args:
            name: Name to search for
            page: Page number
            size: Page size
            
        Returns:
            UserList: Search results with metadata
        """
        skip = (page - 1) * size
        users = self.user_repo.search_by_name(name, skip, size)
        
        user_responses = [UserResponse.from_orm(user) for user in users]
        total = len(users)  # This is a simplified approach
        
        return UserList(
            users=user_responses,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    def get_users_by_profession(self, profession: str, page: int = 1, size: int = 10) -> UserList:
        """
        Get users by profession.
        
        Args:
            profession: Profession to filter by
            page: Page number
            size: Page size
            
        Returns:
            UserList: Filtered users with metadata
        """
        skip = (page - 1) * size
        users = self.user_repo.get_by_profession(profession, skip, size)
        
        user_responses = [UserResponse.from_orm(user) for user in users]
        total = len(users)  # This is a simplified approach
        
        return UserList(
            users=user_responses,
            total=total,
            page=page,
            size=size,
            pages=(total + size - 1) // size
        )
    
    def get_recent_registrations(self, days: int = 7) -> List[UserResponse]:
        """
        Get recent user registrations.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[UserResponse]: Recent registrations
        """
        users = self.user_repo.get_recent_registrations(days)
        return [UserResponse.from_orm(user) for user in users]
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """
        Get user statistics.
        
        Returns:
            dict: User statistics
        """
        total_users = self.user_repo.count_total()
        recent_users = len(self.user_repo.get_recent_registrations(7))
        
        return {
            "total_users": total_users,
            "recent_registrations": recent_users,
            "registration_rate": {
                "daily": len(self.user_repo.get_recent_registrations(1)),
                "weekly": recent_users,
                "monthly": len(self.user_repo.get_recent_registrations(30))
            }
        }
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[UserResponse]:
        """
        Update user data.
        
        Args:
            user_id: User ID
            user_data: Updated user data
            
        Returns:
            UserResponse: Updated user data if successful, None otherwise
        """
        # Validate input data
        if "email" in user_data:
            is_valid, error = validate_email(user_data["email"])
            if not is_valid:
                raise ValueError(f"Invalid email: {error}")
        
        if "phone_number" in user_data:
            is_valid, error = validate_phone_number(user_data["phone_number"])
            if not is_valid:
                raise ValueError(f"Invalid phone number: {error}")
        
        if "name" in user_data:
            is_valid, error = validate_name(user_data["name"])
            if not is_valid:
                raise ValueError(f"Invalid name: {error}")
        
        # Sanitize input data
        sanitized_data = {}
        for key, value in user_data.items():
            if isinstance(value, str):
                sanitized_data[key] = sanitize_input(value)
            else:
                sanitized_data[key] = value
        
        # Update user
        db_user = self.user_repo.update(user_id, sanitized_data)
        if not db_user:
            return None
        
        return UserResponse.from_orm(db_user)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            bool: True if deleted, False if not found
        """
        return self.user_repo.delete(user_id)
    
    def _validate_user_data(self, user_data: UserCreate) -> Dict[str, Any]:
        """
        Validate user data.
        
        Args:
            user_data: User data to validate
            
        Returns:
            dict: Validation result
        """
        # Validate email
        is_valid, error = validate_email(user_data.email)
        if not is_valid:
            return {"valid": False, "error": f"Invalid email: {error}"}
        
        # Validate phone number
        is_valid, error = validate_phone_number(user_data.phone_number)
        if not is_valid:
            return {"valid": False, "error": f"Invalid phone number: {error}"}
        
        # Validate name
        is_valid, error = validate_name(user_data.name)
        if not is_valid:
            return {"valid": False, "error": f"Invalid name: {error}"}
        
        return {"valid": True, "error": None}
    
    def _sanitize_user_data(self, user_data: UserCreate) -> UserCreate:
        """
        Sanitize user data.
        
        Args:
            user_data: User data to sanitize
            
        Returns:
            UserCreate: Sanitized user data
        """
        # Create a copy of the data
        sanitized_data = user_data.dict()
        
        # Sanitize string fields
        sanitized_data["name"] = sanitize_input(user_data.name)
        sanitized_data["email"] = user_data.email.lower().strip()
        sanitized_data["phone_number"] = user_data.phone_number.strip()
        
        if user_data.profession:
            sanitized_data["profession"] = sanitize_input(user_data.profession)
        
        if user_data.interest_reason:
            sanitized_data["interest_reason"] = sanitize_input(user_data.interest_reason)
        
        return UserCreate(**sanitized_data) 