from pydantic import BaseModel, EmailStr
from datetime import date

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
    name: str
    phone: str | None
    address: str | None
    dob: date | None

    model_config = {
        "from_attributes": True
    }

