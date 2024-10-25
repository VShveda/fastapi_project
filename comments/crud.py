from sqlalchemy.orm import Session

from comments.models import Comment
from comments.schemas import CommentCreate


def create_comment(
    db: Session,
    comment: CommentCreate,
    user_id: int,
    is_banned: bool,
    post_id: int,
) -> Comment:
    db_comment = Comment(
        **comment.dict(),
        user_id=user_id,
        is_banned=is_banned,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.post_id == post_id).all()
