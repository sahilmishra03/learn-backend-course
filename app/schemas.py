import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr,conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class CreatePost(PostBase):
    pass

class Post(PostBase):
    id:int
    created_at: datetime.datetime
    owner_id: int
    owner: "User"
    
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        from_attributes=True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class User(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime.datetime

    class Config:
        from_attributes=True
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    # user IDs in tokens are integers, so allow either int or str for flexibility
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)