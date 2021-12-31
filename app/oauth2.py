from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # the path api for login

# SECRET_KEY
# Algorithm
# Expiration time of the token, aka how long the user can be logged in
SECRET_KEY = "***REMOVED***"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # decodes the token from user
        id: str = payload.get("user_id")
        # if no 'id' in token, then throw an error
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # validates the schema
    except JWTError: 
        raise credentials_exception
    
    return token_data # in this case just the 'id' but extra fields may be added to the payload

# initializes credentials_exception and calls the verify token method with the users token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user