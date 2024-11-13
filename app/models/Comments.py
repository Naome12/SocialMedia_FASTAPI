# app/models/comments.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign key to the User model (user who made the comment)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Foreign key to the Post model (post to which this comment belongs)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)

    # Relationships (assuming User and Post models are in `users.py` and `posts.py` respectively)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    comments = relationship("Comment", back_populates="user")
