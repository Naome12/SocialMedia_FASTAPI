from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.auth_services import login_for_access_token
from app.schemas.User import UserLogin, Token
from app.database import get_db

router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    return login_for_access_token(db=db, form_data=form_data)
