"""
API routes for user waiting list operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the waiting list.

    This endpoint checks if a user with the given email already exists.
    If not, it creates a new user record.
    """
    user_repo = UserRepository(db)
    
    # Check if user with this email already exists
    db_user = user_repo.get_by_email(email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )
    
    # Create the new user
    new_user = user_repo.create(user)
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by their ID.
    """
    user_repo = UserRepository(db)
    db_user = user_repo.get_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user