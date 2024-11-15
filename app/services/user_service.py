# app/services/user_service.py
from app.models import followers
from sqlalchemy.orm import Session
from app.models.Users import User
from app.schemas.User import UserCreate, UserUpdate
from typing import Optional
from passlib.context import CryptContext
from app.models.followers import Followers as followers
from sqlalchemy import select

# Initialize Passlib's bcrypt context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Create a new user with hashed password
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)  # Hash the password
    db_user = User(
        username=user.username,
        email=user.email,
        Dob=user.Dob,
        hashed_password=hashed_password,  # Save hashed password
        bio=user.bio,
        profile_picture=user.profile_picture,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get a user by ID
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# Get all users
def get_all_users(db: Session):
    return db.query(User).all()

# Update a user
def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    # Update fields if new data is provided
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.bio is not None:
        user.bio = user_update.bio
    if user_update.profile_picture is not None:
        user.profile_picture = user_update.profile_picture  
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)  # Re-hash new password
    db.commit()
    db.refresh(user)
    return user

# Delete a user by ID
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def follow_user(db: Session, current_user_id: int, user_to_follow_id: int):
    # Check if the user is already following the target user
    stmt = select(followers).filter(
        followers.c.follower_id == current_user_id,
        followers.c.following_id == user_to_follow_id
    )
    existing_follow = db.execute(stmt).first()  # Executes the query and checks if already following
    if existing_follow:
        return {"message": "You are already following this user."}
    
    user_to_follow = db.query(User).filter(User.id == user_to_follow_id).first()
    if not user_to_follow:
        return {"message": "The user you are trying to follow does not exist."}


    # If not already following, insert the new follow relationship
    insert_stmt = followers.insert().values(follower_id=current_user_id, following_id=user_to_follow_id)
    db.execute(insert_stmt)
    db.commit()
    
    return {"message": f"You are now following {user_to_follow.username}."}

def unfollow_user(db: Session, current_user_id: int, user_to_unfollow_id: int) -> str:
    if current_user_id == user_to_unfollow_id:
        raise HTTPException(status_code=400, detail="You cannot unfollow yourself.")
    
    user_to_unfollow = db.query(User).filter(User.id == user_to_unfollow_id).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found.")

    db.execute(followers.delete().where(
        followers.c.follower_id == current_user_id,
        followers.c.following_id == user_to_unfollow_id
    ))
    db.commit()
    return f"You have unfollowed {user_to_unfollow.username}."