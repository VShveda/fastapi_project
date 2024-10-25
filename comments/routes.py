from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from comments.analyzer_comments import get_comments_daily_breakdown
from comments.crud import create_comment, get_comments_by_post
from db.database import get_db
from comments.schemas import CommentCreate, CommentResponse
from services.moderation import is_toxic_content
from user.models import User
from user.services import get_current_user

router = APIRouter()


@router.post("/api/comments/", response_model=CommentResponse)
def create_comment_endpoint(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CommentResponse:
    print(comment)
    is_banned = is_toxic_content(comment.content)
    if is_banned:
        create_comment(
            db=db,
            comment=comment,
            post_id=comment.post_id,
            user_id=current_user.id,
            is_banned=is_banned,
        )
        raise HTTPException(
            status_code=400, detail="Comment contains prohibited content"
        )
    return create_comment(
        db=db,
        comment=comment,
        post_id=comment.post_id,
        user_id=current_user.id,
        is_banned=False,
    )


@router.get(
    "/api/comments/{post_id}", response_model=list[CommentResponse]
)
def get_comments_by_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
) -> list[CommentResponse]:
    comments = get_comments_by_post(db, post_id)
    if not comments:
        raise HTTPException(
            status_code=404, detail="No comments found for this post"
        )
    return comments


@router.get("/api/comments-daily-breakdown/")
def comments_daily_breakdown(
    date_from: str,
    date_to: str,
    db: Session = Depends(get_db),
) -> list[dict]:
    analytics = get_comments_daily_breakdown(db, date_from, date_to)

    return [
        {
            "date": result.date,
            "total_comments": result.total_comments,
            "banned_comments": result.banned_comments,
        }
        for result in analytics
    ]
