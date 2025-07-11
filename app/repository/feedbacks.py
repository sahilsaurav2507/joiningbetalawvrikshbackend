from sqlalchemy.orm import Session
from app.models.feedbacks import Feedback
from app.schemas.feedbacks import FeedbackCreate

def create_feedback(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(contact_email=feedback.contact_email, feedback=feedback.feedback)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def is_duplicate_feedback(db: Session, contact_email: str) -> bool:
    return db.query(Feedback).filter(Feedback.contact_email == contact_email).first() is not None 