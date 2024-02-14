from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Annotated
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . config import settings


oauth2_schema=OAuth2PasswordBearer(tokenUrl= 'login' )

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

class Token(BaseModel):
    access_token: str
    token_type: str

# Copied from documentation
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# cred/ 
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str =payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id) 
        # token_data schema will ensure all data is present
    except JWTError:
        raise credentials_exception
    
    return token_data

# This will fetch token when logged in using URL
    # Ṭhis will ensure when we call a function on a URL and it has get_current_user it will check login status and credentials of login.

# So this way we can keep URL protected which needs login
    
def get_current_user(token: str=Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Couldn't validate credentials", 
                                        headers={"WWW-Authenticate": "Bearer"})
    token=verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    

    return user