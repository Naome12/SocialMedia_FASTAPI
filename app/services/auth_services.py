from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.Users import User
from app.schemas.User import UserLogin
from app.auth import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user


def login_for_access_token(db: Session, form_data:UserLogin):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

