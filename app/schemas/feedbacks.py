from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Any

class FeedbackBase(BaseModel):
    contact_email: EmailStr
    feedback: Any

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackOut(FeedbackBase):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True 