from sqlalchemy.orm import Session, joinedload
from app.models.Posts import Post
from app.schemas.Posts import PostCreate
from fastapi import HTTPException
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

def get_post(db: Session, post_id: int) -> Optional[Post]:
    try:
        post = db.query(Post).options(joinedload(Post.user)).filter(Post.id == post_id).first()
        if post is None:
            logger.warning(f"Post with ID {post_id} not found.")
        return post
    except Exception as e:
        logger.error(f"Error retrieving post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_posts(db: Session, user_id: Optional[int] = None) -> List[Post]:
    try:
        query = db.query(Post).options(joinedload(Post.user))
        if user_id is not None:
            query = query.filter(Post.user_id == user_id)
        return query
    except Exception as e:
        logger.error(f"Error retrieving posts: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def create_post(db: Session, post_create: PostCreate, user_id: int) -> Post:
    try:
        post = Post(
            content=post_create.content,
            image_url=post_create.image_url,
            user_id=user_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        logger.info(f"Post created successfully by user {user_id}")
        return post
    except Exception as e:
        logger.error(f"Error creating post for user {user_id}: {e}")
        db.rollback() 
        raise HTTPException(status_code=500, detail="Internal server error")


def delete_post(db: Session, post_id: int, user_id: int) -> bool:
    try:
        post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if not post:
            logger.warning(f"User {user_id} attempted to delete a post they do not own (Post ID: {post_id})")
            raise HTTPException(status_code=404, detail="Post not found or you don't have permission to delete it")
        
        db.delete(post)
        db.commit()
        logger.info(f"Post with ID {post_id} deleted by user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error deleting post {post_id} by user {user_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")


def update_post(db: Session, post_id: int, user_id: int, post_update: PostCreate) -> Optional[Post]:
    try:
        post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
        if not post:
            logger.warning(f"User {user_id} attempted to update a post they do not own (Post ID: {post_id})")
            raise HTTPException(status_code=404, detail="Post not found or you don't have permission to update it")

        if post_update.content is not None:
            post.content = post_update.content
        if post_update.image_url is not None:
            post.image_url = post_update.image_url

        db.commit()
        db.refresh(post)
        logger.info(f"Post with ID {post_id} updated by user {user_id}")
        return post
    except Exception as e:
        logger.error(f"Error updating post {post_id} by user {user_id}: {e}")
        db.rollback()  
        raise HTTPException(status_code=500, detail="Internal server error")
