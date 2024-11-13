# app/routes/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.user_service import update_user
from app.schemas.User import UserUpdate, UserResponse
from app.database import get_db

router = APIRouter()

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_profile(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
