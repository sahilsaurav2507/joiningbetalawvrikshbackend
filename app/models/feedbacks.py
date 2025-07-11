from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"
    id = Column(Integer, primary_key=True, index=True)
    contact_email = Column(String(255), unique=True, nullable=False, index=True)
    feedback = Column(JSON, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now()) 