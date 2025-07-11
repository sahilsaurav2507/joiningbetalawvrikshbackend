from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate

def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session):
    return [u.__dict__ for u in db.query(User).all()]

def is_duplicate_user(db: Session, email: str, phone: str) -> bool:
    return db.query(User).filter((User.email == email) | (User.phone == phone)).first() is not None 