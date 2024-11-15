from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.Comments import Comment
from app.schemas.Comments import CommentCreate
import logging

logger = logging.getLogger(__name__)

def create_comment(db: Session, comment_create: CommentCreate, post_id: int, user_id: int) -> Comment:
    try:
        comment = Comment( content=comment_create.content, post_id=post_id, user_id=user_id)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        logger.info(f"Comment created successfully by user {user_id} on post {post_id}")
        return comment
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating comment by user {user_id} on post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Error creating comment")

def get_comments(db: Session, post_id: int) -> list[Comment]:
    try:
        comments = db.query(Comment).filter(Comment.post_id == post_id).all()
        logger.info(f"Retrieved {len(comments)} comments for post {post_id}")
        return comments
    except Exception as e:
        logger.error(f"Error fetching comments for post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving comments")

def update_comment(db: Session, comment_id: int, user_id: int, updated_content: str) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if not comment:
        logger.warning(f"User {user_id} attempted to update a non-existent or unauthorized comment (Comment ID: {comment_id})")
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to update it")

    try:
        comment.content = updated_content
        db.commit()
        db.refresh(comment)
        logger.info(f"Comment ID {comment_id} updated successfully by user {user_id}")
        return comment
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating comment {comment_id} by user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating comment")

def delete_comment(db: Session, comment_id: int, user_id: int) -> bool:
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if not comment:
        logger.warning(f"User {user_id} attempted to delete a non-existent or unauthorized comment (Comment ID: {comment_id})")
        raise HTTPException(status_code=404, detail="Comment not found or you don't have permission to delete it")
    try:
        db.delete(comment)
        db.commit()
        logger.info(f"Comment ID {comment_id} deleted successfully by user {user_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting comment {comment_id} by user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting comment")
