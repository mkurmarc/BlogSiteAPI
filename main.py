
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default value is true if no user provides value
    rating: Optional[int] = None # fully optional field tht defaults to None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "favorite foods", "content": "i like pizzas", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    return{"data": my_posts} # If I pass in an array like this, FastAPI 
                             # serializes 'my_posts' converting it into JSON

'''
# another example of using the Body
@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # saves body content to a dict named payload
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
'''

@app.post("/posts")
def create_posts(post: Post): # FastAPI automatically checks frontend payload if data fits the 
    post_dict = post.dict()   # schema model, Post. If true, then it validates and data is
    post_dict['id'] = randrange(0, 10000000) # available via 'new_post'. If false, then error is sent back to
    my_posts.append(post_dict)                        # user stating where the error is. AUTOMATIC VALIDATION
    return {"data": post_dict}           
                                  

@app.get("/posts/{id}")
def get_post(id: int):           # Validates that path parameter can be turned 
    post = find_post(id)         # into int and does so if true. Now throws error 
    return{"post_detail": post}  # if the parameter is not the selcted type of  
                                 # int. Also, now the frontend has a good way of 
                                 # understanding what they did wrong


