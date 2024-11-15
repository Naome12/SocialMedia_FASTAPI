from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

# Define the followers table as a Table object
Followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('following_id', Integer, ForeignKey('users.id'), primary_key=True)
)
