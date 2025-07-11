from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class NotInterestedBase(BaseModel):
    email: EmailStr
    reason: Optional[str] = None

class NotInterestedCreate(NotInterestedBase):
    pass

class NotInterestedOut(NotInterestedBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 