from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # the path api for login

# SECRET_KEY
# Algorithm
# Expiration time of the token, aka how long the user can be logged in
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """
    Creates a JWT (JSON Web Token) that includes the provided user data. The token has a 
    preset expiration time (defined by ACCESS_TOKEN_EXPIRE_MINUTES). This function is typically 
    used during the authentication process, where it creates a token for a successfully 
    authenticated user, which the user can then use for authenticating subsequent requests.

    Args:
        data (dict): A dictionary that must include the user details. The 'user_id' is an example 
        of a detail that can be included. This data will be embedded in the JWT payload.

    Returns:
        str: A JWT as a string. This JWT includes the user details and an expiration time. 
        This token can be returned to the client during the login process or token refresh process.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    """
    Verifies and decodes a JWT token. If verification is successful, a TokenData 
    object is returned. If token verification fails, a credentials_exception is 
    raised.
    
    Args:
        token (str): The JWT token to verify and decode.
        credentials_exception: The exception to be raised if token verification fails.
    
    Returns:
        TokenData: A Pydantic model containing the decoded information from the JWT.
    """
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
    """
    Authenticates a user using a provided JWT token and retrieves the user's details 
    from a database. If token verification fails, a HTTP 401 Unauthorized error is 
    returned.

    Args:
        token (str): The JWT token to verify. This is provided using FastAPI's 
        dependency injection system, and would typically come from the 'Authorization' 
        header in the HTTP request.
        
        db (Session): The database session to use for querying the database. This is 
        provided using FastAPI's dependency injection system.

    Returns:
        models.User: The authenticated user's details retrieved from the database. 

    Raises:
        HTTPException: If token verification fails, an HTTP 401 Unauthorized 
        error is returned.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user