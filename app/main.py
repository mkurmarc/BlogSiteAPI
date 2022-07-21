
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#Create the database tables; In a very simplistic way create the database tables:
#models.Base.metadata.create_all(bind=engine) # do need any more because of Alembic

app = FastAPI()


origins = ["*"]
# allows other domains to talk to API https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware( # if API configured for specific webapp, then a strict origins list is best practice
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# lines below import the router objects from the post and user files in the router folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# do not need
@app.get("/")
def root():
    return {"message": "Hello World!!!"}
