from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.database import Base


class Post(BaseModel):       #using pydantic
    title: str
    content: str
    published: bool = True 
       
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass 

class PostResponse(PostBase):
    id : int
    create_at : datetime
    
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email : EmailStr
    password : str
    
class UserResponse(BaseModel):
    email : EmailStr
    id : int
    create_at :  datetime
    
    class Config:
        orm_mode = True
        
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None