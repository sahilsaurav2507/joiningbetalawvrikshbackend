from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.feedbacks import FeedbackCreate, FeedbackOut
from app.repository.feedbacks import create_feedback, is_duplicate_feedback

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/feedback", response_model=FeedbackOut)
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    if is_duplicate_feedback(db, feedback.contact_email):
        raise HTTPException(status_code=400, detail="Feedback already submitted for this email")
    return create_feedback(db, feedback) 