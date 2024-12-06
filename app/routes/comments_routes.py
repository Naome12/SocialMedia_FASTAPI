from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.Comments import CommentCreate, CommentResponse, CommentUpdate
from app.services.comments_services import create_comment, get_comments, delete_comment, update_comment
from app.auth import get_current_user
from app.database import get_db
from app.models.Users import User

router = APIRouter(prefix="/comments",tags=["comments"])

@router.post("/posts/{post_id}", response_model=CommentResponse)
def add_comment(post_id: int, comment_create: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment = create_comment(db, comment_create, post_id, current_user.id)
    return comment

@router.get("/posts/{post_id}", response_model=list[CommentResponse])
def get_all_comments(post_id: int, db: Session = Depends(get_db)):
    comments = get_comments(db, post_id)
    return comments

@router.put("/edit/{comment_id}/", response_model=CommentResponse)
def update_comment_route(comment_id: int, comment_update: CommentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated_comment = update_comment(db, comment_id, current_user.id, comment_update.updated_content)
    return updated_comment

@router.delete("/{comment_id}/", status_code=204)
def delete_comment_route(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = delete_comment(db, comment_id, current_user.id)
    if success:
        return {"message": "Comment deleted successfully"}
