# app/models/Users.py
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from app.database import Base
from app.models.followers import Followers  # Correct import

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

    # Relationships
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    # Followers relationship
    followers = relationship(
        "User",
        secondary=Followers,  # Reference the followers table
        primaryjoin=id == Followers.c.following_id,
        secondaryjoin=id == Followers.c.follower_id,
        backref="following",  # Enables querying "following"
    )
