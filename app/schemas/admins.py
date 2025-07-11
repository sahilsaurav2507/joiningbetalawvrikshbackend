from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminBase(BaseModel):
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminOut(AdminBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 