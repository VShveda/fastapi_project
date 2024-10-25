from sqlalchemy import func, cast, Integer
from sqlalchemy.orm import Session

from comments.models import Comment


def get_comments_daily_breakdown(
    db: Session, date_from: str, date_to: str
) -> list:
    query = (
        db.query(
            func.date(Comment.created_at).label("date"),
            func.count(Comment.id).label("total_comments"),
            func.sum(cast(Comment.is_banned, Integer)).label(
                "banned_comments"
            ),
        )
        .filter(
            func.date(Comment.created_at) >= date_from,
            func.date(Comment.created_at) <= date_to,
        )
        .group_by(func.date(Comment.created_at))
        .order_by(func.date(Comment.created_at))
    )

    results = query.all()
    return results
