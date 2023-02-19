from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int]
    email: str
    password: str
    name: str
    is_provider: bool
    is_client = bool
    is_admin = bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "johndoe@gmail.com",
                "password": "password",
                "name": "johndoe",
                "is_provider": False,
                "is_client": False,
                "is_admin": False,
            }
        }


class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "johndoe@gmail.com", "password": "password"}
        }
