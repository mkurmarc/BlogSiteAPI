from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value is true if no user provides value
    # rating: Optional[int] = None # fully optional field tht defaults to None


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    created_at: datetime

    class Config: # this class
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr # using this type ensures email is a valid one, uses "email-validator" library
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: # this class
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    