from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value is true if no user provides value
    # rating: Optional[int] = None # fully optional field tht defaults to None

class PostCreate(PostBase):
    pass
