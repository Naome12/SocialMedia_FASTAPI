# app/schemas/Post.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.User import UserResponse

class PostBase(BaseModel):
    content: str
    image_url: Optional[str] = None

# Schema for creating a post
class PostCreate(PostBase):
    pass  # Inherits content and image_url fields

# Schema for response (when sending post data back to client)
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: Optional[UserResponse] = None  # To include user details if needed

    class Config:
        orm_mode = True

# Schema for post with comments (optional)
class PostWithComments(PostResponse):
    comments: List["CommentResponse"] = []
