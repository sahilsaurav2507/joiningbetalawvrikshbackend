from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.creators import CreatorCreate, CreatorOut
from app.repository.creators import create_creator, is_duplicate_creator

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/creatordata", response_model=CreatorOut)
def register_creator(creator: CreatorCreate, db: Session = Depends(get_db)):
    if is_duplicate_creator(db, creator.email, creator.phone):
        raise HTTPException(status_code=400, detail="Email or phone already exists")
    return create_creator(db, creator) 