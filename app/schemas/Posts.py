from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.schemas.User import UsernameResponse

class PostBase(BaseModel):
    content: str
    image_url: Optional[str] = None

class PostCreate(PostBase):
    pass 

class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: Optional[UsernameResponse] = None 

    class Config:
        orm_mode = True

class PostWithComments(PostResponse):
    comments: List["CommentResponse"] = []