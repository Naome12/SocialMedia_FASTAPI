# app/schemas/User.py
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List

# Base schema for shared fields
class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    Dob: date


# Schema for creating a new user
class UserCreate(UserBase):
    password: str  # Only needed for user creation

# Schema for response (when sending user data back to client)
class UserResponse(UserBase):
    username:str
    id: int
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Schema for user with posts and comments (optional)
class UserWithPostsAndComments(UserResponse):
    posts: List["PostResponse"] = []
    comments: List["CommentResponse"] = []

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
