from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.Users import User
from app.schemas.Posts import PostCreate, PostResponse
from app.services.posts_services import get_post, get_posts, create_post, update_post, delete_post
from app.database import get_db
from app.auth import get_current_user
from typing import Optional, List
from app.utils.preprocessing import preprocess_posts

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/preprocessed")
def get_preprocessed_posts(limit: int = 100000, db: Session = Depends(get_db)):
    """
    Fetch preprocessed posts with feature engineering applied.
    """
    df = preprocess_posts(db, limit)
    return df.to_dict(orient="records")

@router.post("/createpost", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(post_create: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = create_post(db=db, post_create=post_create, user_id=current_user.id)
    return post

@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post(db=db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.get("/", response_model=List[PostResponse])
def read_posts( user_id: Optional[int] = None, db: Session = Depends(get_db)):
    posts = get_posts(db=db, user_id=user_id)
    return posts

@router.put("/edit/{post_id}", response_model=PostResponse)
def update_existing_post(post_id: int, post_update: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = update_post(db=db, post_id=post_id, user_id=current_user.id, post_update=post_update)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission to update it")
    return post

@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    success = delete_post(db=db, post_id=post_id, user_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found or you don't have permission to delete it")
    return {"detail": "Post deleted successfully"}
