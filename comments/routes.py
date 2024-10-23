from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from comments.schemas import CommentCreate, CommentResponse
from comments.models import Comment
from user.models import User
from user.services import get_current_user


router = APIRouter()


@router.post("/api/comments/", response_model=CommentResponse)
def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Comment:
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get(
    "/api/comments/{post_id}", response_model=list[CommentResponse]
)
def get_comments_by_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Comment]:
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    if not comments:
        raise HTTPException(
            status_code=404, detail="No comments found for this post"
        )
    return comments
