from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from posts.crud import (
    create_post,
    get_post,
    get_posts,
    update_post,
    delete_post,
)
from posts.schemas import PostCreate, PostResponse
from posts.models import Post
from db.database import get_db
from services.moderation import is_toxic_content
from user.models import User
from user.services import get_current_user

router = APIRouter()


@router.post("/posts/", response_model=PostResponse)
def create(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:
    print(post)
    if is_toxic_content(post.content):
        create_post(
            db=db, post=post, user_id=current_user.id, is_banned=True
        )
        raise HTTPException(
            status_code=400, detail="Post contains toxic content"
        )
    return create_post(
        db=db, post=post, user_id=current_user.id, is_banned=False
    )


@router.get("/posts/", response_model=list[PostResponse])
def read_posts(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[Type[Post]]:
    posts = get_posts(db=db, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)) -> Post:
    db_post = get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=PostResponse)
def update(
    post_id: int,
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:
    db_post = update_post(
        db=db, post_id=post_id, post=post, user_id=current_user.id
    )
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}", response_model=PostResponse)
def delete(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:
    db_post = delete_post(db=db, post_id=post_id, user_id=current_user.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}/auto-reply", response_model=PostResponse)
def update_auto_reply_settings(
    post_id: int,
    post: PostResponse,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PostResponse:
    db_post = (
        db.query(Post)
        .filter(Post.id == post_id, Post.user_id == current_user.id)
        .first()
    )
    if db_post is None:
        raise HTTPException(
            status_code=404, detail="Post not found or access denied"
        )

    db_post.auto_reply_enabled = post.auto_reply_enabled
    db_post.reply_delay = post.reply_delay
    db.commit()
    db.refresh(db_post)

    return post
