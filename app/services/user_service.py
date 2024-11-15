# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.Users import User
from app.schemas.User import UserCreate, UserUpdate
from typing import Optional
from passlib.context import CryptContext

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
