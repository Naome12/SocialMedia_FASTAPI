# app/services/post_services.py

from sqlalchemy.orm import Session, joinedload
from app.models.Post import Post
from app.schemas.Post import PostCreate
from typing import List, Optional

def get_post(db: Session, post_id: int) -> Optional[Post]:
    """
    Retrieve a single post by ID, including the user details.
    """
    # Use joinedload to load the related user along with the post
    return db.query(Post).options(joinedload(Post.user)).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10, user_id: Optional[int] = None) -> List[Post]:
    """
    Retrieve multiple posts, optionally filtering by user_id, and include user details.
    """
    query = db.query(Post).options(joinedload(Post.user))
    if user_id is not None:
        query = query.filter(Post.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_post(db: Session, post_create: PostCreate, user_id: int) -> Post:
    """
    Create a new post for a specific user.
    """
    post = Post(
        content=post_create.content,
        image_url=post_create.image_url,
        user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post_id: int, user_id: int) -> bool:
    """
    Delete a post by ID if it belongs to the given user_id.
    """
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

def update_post(db: Session, post_id: int, user_id: int, post_update: PostCreate) -> Optional[Post]:
    """
    Update a post's content or image URL if it belongs to the given user_id.
    """
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        return None

    if post_update.content is not None:
        post.content = post_update.content
    if post_update.image_url is not None:
        post.image_url = post_update.image_url

    db.commit()
    db.refresh(post)
    return post
