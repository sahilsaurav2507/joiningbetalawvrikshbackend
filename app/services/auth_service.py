"""
Authentication service for admin login and token management.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories.admin_repository import AdminRepository
from app.schemas.admin import AdminLogin, TokenResponse
from app.utils.security import verify_password, create_access_token, create_refresh_token, verify_token
from app.config import settings


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.admin_repo = AdminRepository(db)
    
    def authenticate_admin(self, login_data: AdminLogin) -> Optional[Dict[str, Any]]:
        """
        Authenticate admin user.
        
        Args:
            login_data: Admin login credentials
            
        Returns:
            dict: Admin user data if authenticated, None otherwise
        """
        # Get admin by username
        admin = self.admin_repo.get_by_username(login_data.username)
        if not admin:
            return None
        
        # Check if admin is active
        if not admin.is_active:
            return None
        
        # Verify password
        if not verify_password(login_data.password, admin.hashed_password):
            return None
        
        # Update last login
        self.admin_repo.update_last_login(admin.id)
        
        return {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "is_active": admin.is_active
        }
    
    def create_tokens(self, admin_data: Dict[str, Any]) -> TokenResponse:
        """
        Create access and refresh tokens for admin.
        
        Args:
            admin_data: Admin user data
            
        Returns:
            TokenResponse: Access and refresh tokens
        """
        # Create token data
        token_data = {
            "sub": str(admin_data["id"]),
            "username": admin_data["username"],
            "email": admin_data["email"]
        }
        
        # Create access token
        access_token = create_access_token(token_data)
        
        # Create refresh token
        refresh_token = create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
            refresh_token=refresh_token
        )
    
    def login_admin(self, login_data: AdminLogin) -> Optional[TokenResponse]:
        """
        Login admin user and return tokens.
        
        Args:
            login_data: Admin login credentials
            
        Returns:
            TokenResponse: Access and refresh tokens if successful, None otherwise
        """
        # Authenticate admin
        admin_data = self.authenticate_admin(login_data)
        if not admin_data:
            return None
        
        # Create tokens
        return self.create_tokens(admin_data)
    
    def refresh_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """
        Refresh access token using refresh token.
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            TokenResponse: New access token if valid, None otherwise
        """
        # Verify refresh token
        payload = verify_token(refresh_token)
        if not payload:
            return None
        
        # Check if it's a refresh token
        if payload.get("type") != "refresh":
            return None
        
        # Get admin data
        admin_id = payload.get("sub")
        if not admin_id:
            return None
        
        admin = self.admin_repo.get_by_id(int(admin_id))
        if not admin or not admin.is_active:
            return None
        
        # Create new tokens
        admin_data = {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "is_active": admin.is_active
        }
        
        return self.create_tokens(admin_data)
    
    def get_current_admin(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get current admin from token.
        
        Args:
            token: Access token
            
        Returns:
            dict: Admin data if valid, None otherwise
        """
        # Verify token
        payload = verify_token(token)
        if not payload:
            return None
        
        # Get admin data
        admin_id = payload.get("sub")
        if not admin_id:
            return None
        
        admin = self.admin_repo.get_by_id(int(admin_id))
        if not admin or not admin.is_active:
            return None
        
        return {
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "is_active": admin.is_active,
            "created_at": admin.created_at,
            "last_login": admin.last_login
        }
    
    def validate_token(self, token: str) -> bool:
        """
        Validate access token.
        
        Args:
            token: Access token to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        payload = verify_token(token)
        if not payload:
            return False
        
        # Check if admin exists and is active
        admin_id = payload.get("sub")
        if not admin_id:
            return False
        
        admin = self.admin_repo.get_by_id(int(admin_id))
        return admin is not None and admin.is_active
    
    def logout_admin(self, token: str) -> bool:
        """
        Logout admin user (invalidate token).
        
        Args:
            token: Access token to invalidate
            
        Returns:
            bool: True if successful, False otherwise
        """
        # In a more sophisticated implementation, you might want to:
        # 1. Add token to a blacklist
        # 2. Store blacklisted tokens in Redis
        # 3. Check blacklist on token validation
        
        # For now, we'll just return True as JWT tokens are stateless
        # The client should remove the token from storage
        return True 