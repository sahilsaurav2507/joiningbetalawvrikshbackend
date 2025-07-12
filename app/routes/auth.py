"""
Authentication routes for admin login and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.auth_service import AuthService
from app.schemas.admin import AdminLogin, TokenResponse, AdminResponse
from app.schemas.common import BaseResponse, ErrorResponse

router = APIRouter()
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login_admin(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """
    Login admin user and return access token.
    
    Args:
        login_data: Admin login credentials
        db: Database session
        
    Returns:
        TokenResponse: Access and refresh tokens
        
    Raises:
        HTTPException: If authentication fails
    """
    auth_service = AuthService(db)
    
    try:
        token_response = auth_service.login_admin(login_data)
        if not token_response:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        return token_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Args:
        refresh_token: Refresh token
        db: Database session
        
    Returns:
        TokenResponse: New access and refresh tokens
        
    Raises:
        HTTPException: If refresh token is invalid
    """
    auth_service = AuthService(db)
    
    try:
        token_response = auth_service.refresh_token(refresh_token)
        if not token_response:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        return token_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token refresh failed: {str(e)}"
        )


@router.get("/me", response_model=AdminResponse, status_code=status.HTTP_200_OK)
async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current admin user information.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        AdminResponse: Current admin user data
        
    Raises:
        HTTPException: If token is invalid
    """
    auth_service = AuthService(db)
    
    try:
        admin_data = auth_service.get_current_admin(credentials.credentials)
        if not admin_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        
        return AdminResponse(**admin_data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get admin data: {str(e)}"
        )


@router.post("/logout", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def logout_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Logout admin user.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        BaseResponse: Success message
        
    Raises:
        HTTPException: If logout fails
    """
    auth_service = AuthService(db)
    
    try:
        success = auth_service.logout_admin(credentials.credentials)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Logout failed"
            )
        
        return BaseResponse(
            success=True,
            message="Successfully logged out"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


@router.post("/validate", response_model=BaseResponse, status_code=status.HTTP_200_OK)
async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Validate access token.
    
    Args:
        credentials: HTTP authorization credentials
        db: Database session
        
    Returns:
        BaseResponse: Validation result
        
    Raises:
        HTTPException: If token is invalid
    """
    auth_service = AuthService(db)
    
    try:
        is_valid = auth_service.validate_token(credentials.credentials)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        
        return BaseResponse(
            success=True,
            message="Token is valid"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token validation failed: {str(e)}"
        ) 