from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.not_interested import NotInterestedCreate, NotInterestedOut
from app.repository.not_interested import create_not_interested

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notinteresteddata", response_model=NotInterestedOut)
def submit_not_interested(data: NotInterestedCreate, db: Session = Depends(get_db)):
    return create_not_interested(db, data) 