from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.users import UserCreate, UserOut
from app.repository.users import create_user, is_duplicate_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/userdata", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if is_duplicate_user(db, user.email, user.phone):
        raise HTTPException(status_code=400, detail="Email or phone already exists")
    return create_user(db, user) 