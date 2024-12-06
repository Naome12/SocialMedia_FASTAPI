from app.models import followers
from sqlalchemy.orm import Session
from app.models.Users import User
from app.schemas.User import UserCreate, UserUpdate
from typing import Optional
from passlib.context import CryptContext
from app.models.followers import Followers as followers
from sqlalchemy import select
from fastapi import HTTPException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)  
    db_user = User(
        username=user.username,
        email=user.email,
        Dob=user.Dob,
        hashed_password=hashed_password, 
        bio=user.bio,
        profile_picture=user.profile_picture,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
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

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def follow_user(db: Session, current_user_id: int, user_to_follow_id: int):
    if current_user_id == user_to_follow_id:
        return {"message": "You can't follow yourself."}
    stmt = select(followers).filter(
        followers.c.follower_id == current_user_id,
        followers.c.following_id == user_to_follow_id
    )
    existing_follow = db.execute(stmt).first()
    if existing_follow:
        return {"message": "You are already following this user."}
    user_to_follow = db.query(User).filter(User.id == user_to_follow_id).first()
    if not user_to_follow:
        return {"message": "The user you are trying to follow does not exist."}
    insert_stmt = followers.insert().values(follower_id=current_user_id, following_id=user_to_follow_id)
    db.execute(insert_stmt)
    db.commit()

    return {"message": f"You are now following {user_to_follow.username}."}

def unfollow_user(db: Session, current_user_id: int, user_to_unfollow_id: int) -> str:
    user_to_unfollow = db.query(User).filter(User.id == user_to_unfollow_id).first()
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found.")
    existing_follow = db.query(followers).filter(followers.c.follower_id == current_user_id,followers.c.following_id == user_to_unfollow_id).first()

    if not existing_follow:
        raise HTTPException(status_code=400, detail="You are not following this user.")
    
    db.execute(followers.delete().where(
        followers.c.follower_id == current_user_id,
        followers.c.following_id == user_to_unfollow_id
    ))
    db.commit()

    return f"You have unfollowed {user_to_unfollow.username}."
