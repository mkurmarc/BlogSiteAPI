from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# from .config import settings
from pydantic import BaseSettings
import time
from . import models, schemas 
from .database import engine, get_db
from sqlalchemy.orm import Session


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


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)): # pass in Session as parameter saved as 'db' when using sqlalchemy and fastapi
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts # If I pass in an array like this, FastAPI 
                          # serializes 'my_posts' converting it into JSON

'''
# another example of using the Body
@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # saves body content to a dict named payload
    print(payload)
    return {"new_post": f"title {payload['title']} content: {payload['content']}"}
'''
'''
#2:
FastAPI automatically checks frontend payload if data fits the schema model, 'Post'. If true,
then it validates and data is available via 'new_post'. If false, then error is sent back to
user stating where the error is. AUTOMATIC VALIDATION.
#2
Use this style of string witht he % symbols because it protects against SQL injection attackspp 
'''
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) 
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 
    # cursor.execute( #2 ALSO code block below uses SQL instead of sqlalchemy          
    #     """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #     (post.title, post.content, post.published) 
    # ) 
    # new_post = cursor.fetchone()
    # conn.commit() # pushes the changes out to the database
    new_post = models.Post(**post.dict()) # this line does same thing as next 2 lines of comments
    # new_post = models.Post(
    # title=post.title, content=post.content, published=post.published)
    db.add(new_post) # add to database
    db.commit() # then commit it
    db.refresh(new_post) # retrieve the new post that was created and store it back under the variable 'new_post'

    return new_post          

'''
'id: int' Validates that path parameter can be turned into int and does
so if true. Now throws error if the parameter is not the selcted type of
int. Also, now the frontend has a good way of understanding what they did wrong
'''                                  
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):       
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),)) # converts int to string AND this comma may fix a current bug
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()   

    if not post:          
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found") 

    return post           
                                    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)                                   


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)): # 'post: Post' makes sures the request comes in with the right schema
    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    #     RETURNING * """,
    #     (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None: # if index doesnt exist, this sends an error code to the user stating the reason
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()