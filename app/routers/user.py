from sys import prefix
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from .. database import get_db

# prefix = adds the string to the beginning of each path op
# tags = is for the docs website for this api, it groups these path ops under 'Users' in the docs
router = APIRouter(
    prefix="/users", 
    tags=['Users'] 
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user) # add to database
    db.commit() # then commit it
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id}")

    return user