from sqlalchemy.orm import Session
from app.models.not_interested import NotInterested
from app.schemas.not_interested import NotInterestedCreate

def create_not_interested(db: Session, data: NotInterestedCreate):
    db_entry = NotInterested(email=data.email, reason=data.reason)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry 