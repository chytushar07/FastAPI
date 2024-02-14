
from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Defining data schema: -pydantic model -Defines the structure of a request and response
# class Post(BaseModel): #This will ensure front-end send data type we want. 
#     title:str
#     content:str
#     published: bool =True

class PostBase(BaseModel):
    title:str
    content:str
    published: bool =True
    

class PostCreate(PostBase):
    pass #Same as PostBase

# Response Pydantic Model

# Response model
class UserOut(BaseModel):
    id:int
    email:EmailStr  # Validates email
    created_at:datetime

    class Config:
       from_attributes=True

class Post(PostBase):
    id:int
    created_at:datetime
    owner_id: int
    owner : UserOut #Refers Pydantic model 

    class Config:
       from_attributes=True

# We can create several classes request/Response structure as Creating post might require all fields while updating post won't
class CreatePost(BaseModel):
    title:str
    content:str
    published: bool =True

class UpdatePost(BaseModel):
    # title:str
    # content:str
    published: bool =True    

class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]=None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)
