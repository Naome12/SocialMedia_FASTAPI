from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    Dob: date

class UserCreate(UserBase):
    password: str  

class UsernameResponse(BaseModel):
    username: str
    class Config:
        orm_mode = True

class UserResponse(UserBase):
    username:str
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserWithPostsAndComments(UserResponse):
    posts: List["PostResponse"] = []
    comments: List["CommentResponse"] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str