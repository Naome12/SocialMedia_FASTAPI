from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.User import UsernameResponse
from app.schemas.Posts import PostResponse

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass 

class CommentUpdate(BaseModel):
    updated_content: str

class CommentResponse(CommentBase):
    id: int
    timestamp: datetime
    user_id: int
    post_id: int
    user: Optional[UsernameResponse] = None
    post: Optional[PostResponse] = None

    class Config:
        orm_mode = True
