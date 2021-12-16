
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default value is true if no user provides value
    rating: Optional[int] = None # fully optional field tht defaults to None

@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return{"data":"This is your posts"}

'''
# another example of using the Body
@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # saves body content to a dict named payload
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
'''

@app.post("/createposts")
def create_posts(new_post: Post): # FastAPI automatically checks frontend payload if data fits the 
    print(new_post.published)     # schema model, Post. If true, then it validates and data is 
    return {"NEW POST"}           # available via 'new_post'. If false, then error is sent back to
                                  # user stating where the error is. AUTOMATIC VALIDATION

