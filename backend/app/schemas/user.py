from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    Name: str
    Phone: str
    Address: str
    DOB: date
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True  # replaces orm_mode
    }
