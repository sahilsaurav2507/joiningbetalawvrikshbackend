from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreatorBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class CreatorCreate(CreatorBase):
    pass

class CreatorOut(CreatorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 