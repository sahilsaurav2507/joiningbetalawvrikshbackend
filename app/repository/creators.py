from sqlalchemy.orm import Session
from app.models.creators import Creator
from app.schemas.creators import CreatorCreate

def create_creator(db: Session, creator: CreatorCreate):
    db_creator = Creator(name=creator.name, email=creator.email, phone=creator.phone)
    db.add(db_creator)
    db.commit()
    db.refresh(db_creator)
    return db_creator

def get_all_creators(db: Session):
    return [c.__dict__ for c in db.query(Creator).all()]

def is_duplicate_creator(db: Session, email: str, phone: str) -> bool:
    return db.query(Creator).filter((Creator.email == email) | (Creator.phone == phone)).first() is not None 