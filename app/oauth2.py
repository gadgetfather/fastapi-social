from fastapi import Depends, HTTPException,status
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.database import get_db
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Secret key to sign the JWT token
#Algorithm used to sign the JWT token
#Expiration time of the JWT token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY = "d1e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict):
    to_encode = data.copy()
    # Add expiration time to the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str ,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        print("00000",type(user_id))
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(user_id))

    except JWTError:
        raise credentials_exception
    return token_data
 

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token,credentials_exception)