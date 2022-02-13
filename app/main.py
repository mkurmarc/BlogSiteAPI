
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

#Create the database tables; In a very simplistic way create the database tables:
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# lines below import the router objects from the post and user files in the router folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# do not need
@app.get("/")
def root():
    return {"message": "Hello World!!!"}
