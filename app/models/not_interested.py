from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class NotInterested(Base):
    __tablename__ = "not_interested"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 