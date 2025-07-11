from sqlalchemy.orm import Session
from app.models.users import User
from app.models.creators import Creator
from app.models.feedbacks import Feedback

def is_duplicate_user(db: Session, email: str, phone: str) -> bool:
    return db.query(User).filter((User.email == email) | (User.phone == phone)).first() is not None

def is_duplicate_creator(db: Session, email: str, phone: str) -> bool:
    return db.query(Creator).filter((Creator.email == email) | (Creator.phone == phone)).first() is not None

def is_duplicate_feedback(db: Session, contact_email: str) -> bool:
    return db.query(Feedback).filter(Feedback.contact_email == contact_email).first() is not None 