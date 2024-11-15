from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.User import UserCreate, UserResponse, UserUpdate
from app.services.user_service import (
    create_user, get_user, get_all_users, update_user, delete_user
)
from app.database import get_db  # Database session dependency

router = APIRouter(
    prefix="/users",  # Prefix for all routes in this file
    tags=["Users"]
)

# Route to create a new user
@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)  # Call the service function directly

# Route to get a user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Route to get all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return get_all_users(db=db)

# Route to update user information
@router.put("/update/{user_id}", response_model=UserResponse)
def update_user_data(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Route to delete a user by ID
@router.delete("/delete/{user_id}", response_model=bool)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

