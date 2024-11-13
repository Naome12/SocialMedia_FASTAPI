from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.models.Users import Base  # Ensure this is the same Base as used in Users.py

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String, nullable=False)
    image_url = Column(String, nullable=True)  # Link to post image
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
