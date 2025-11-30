from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name: str
    phone: str | None = None
    address: str | None = None
    dob: date | None = None
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    dob: Optional[date]

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dob: Optional[date] = None

    model_config = {
        "extra": "ignore"
    }