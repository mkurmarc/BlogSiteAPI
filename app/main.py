
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# from .config import settings
from pydantic import BaseSettings
import time
from . import models, schemas, utils 
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

#Create the database tables; In a very simplistic way create the database tables:
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# lines below import the router objects from the post and user files in the router folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



@app.get("/")
def root():
    return {"message": "Hello World!!!"}
