from sqlalchemy.orm import Session
from app.models.admins import Admin

def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first() 