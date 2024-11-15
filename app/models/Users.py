from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from app.database import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    Dob = Column(Date, nullable=False) 
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  
    bio = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)

    posts = relationship("Post", back_populates="user") 
    comments = relationship("Comment", back_populates="user")  

    # def __repr__(self):
    #     return f"User(id={self.id}, username={self.username})"
