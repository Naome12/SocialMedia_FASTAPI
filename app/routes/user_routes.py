# app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.User import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (create_user, get_user, get_all_users, update_user, delete_user, follow_user, unfollow_user)
from app.database import get_db 
from app.models.Users import User
from app.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/createuser", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db=db)

@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_data(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/delete/{user_id}", response_model=bool)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@router.post("/follow/{user_id}")
def follow(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return follow_user(db=db, current_user_id=current_user.id, user_to_follow_id=user_id)

@router.post("/unfollow/{user_id}")
def unfollow(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return unfollow_user(db=db, current_user_id=current_user.id, user_to_unfollow_id=user_id)
