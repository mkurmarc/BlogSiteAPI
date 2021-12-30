from pydantic import BaseModel
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
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config: # this class
        orm_mode = True
