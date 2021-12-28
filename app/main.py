from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# from .config import settings
from pydantic import BaseSettings
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # default value is true if no user provides value
    # rating: Optional[int] = None # fully optional field tht defaults to None

# temp solution to connect to DB. Later add production ready solution
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='BlogSiteAPI', user='postgres', 
                                password='***REMOVED***', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successful!")
        break
    except Exception as error:
        print("Connecting to DB failed!")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
    {"title": "favorite foods", "content": "i like pizzas", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return{"data": posts} # If I pass in an array like this, FastAPI 
                          # serializes 'my_posts' converting it into JSON

'''
# another example of using the Body
@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # saves body content to a dict named payload
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
'''
'''
#1
FastAPI automatically checks frontend payload if data fits the schema model, 'Post'. If true,
then it validates and data is available via 'new_post'. If false, then error is sent back to
user stating where the error is. AUTOMATIC VALIDATION.
#2
Use this style of string witht he % symbols because it protects against SQL injection attacks
'''
  
@app.post("/posts", status_code=status.HTTP_201_CREATED) 
def create_posts(post: Post): #1 
    cursor.execute( #2          
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
        (post.title, post.content, post.published) 
    ) 
    new_post = cursor.fetchone()
    conn.commit() # pushes the changes out to the database
    return {"data": new_post}           
                                  
# 'id: int' Validates that path parameter can be turned into int and does
# so if true. Now throws error if the parameter is not the selcted type of
# int. Also, now the frontend has a good way of understanding what they did wrong
@app.get("/posts/{id}")
def get_post(id: int):               
    post = find_post(id)  
    if not post:          
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found") 
    return{"post_detail": post}            
                                    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)                                   


@app.put("/posts/{id}")
def update_post(id: int, post: Post): # 'post: Post' makes sures the request comes in with the right schema
    index = find_index_post(id)
    # if index doesnt exist, this sends an error code to the user stating the reason
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    
    post_dict = post.dict()
    post_dict['id'] = id 
    my_posts[index] = post_dict
    return {'data': post_dict}