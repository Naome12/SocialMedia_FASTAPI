from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base 

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)  

    user = relationship("User", back_populates="comments")  
    post = relationship("Post", back_populates="comments")  