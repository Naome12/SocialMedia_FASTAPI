# app/schemas/Comment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.User import UserResponse
from app.schemas.Posts import PostResponse

class CommentBase(BaseModel):
    content: str

# Schema for creating a comment
class CommentCreate(CommentBase):
    pass  # Inherits content field for comment creation

# Schema for response (when sending comment data back to client)
class CommentResponse(CommentBase):
    id: int
    timestamp: datetime
    user_id: int
    post_id: int
    user: Optional[UserResponse] = None
    post: Optional[PostResponse] = None

    class Config:
        orm_mode = True
