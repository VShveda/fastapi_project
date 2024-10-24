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
from posts.schemas import PostCreate, Post
from db.database import get_db
from services.moderation import is_toxic_content
from user.models import User
from user.services import get_current_user

router = APIRouter()


@router.post("/posts/", response_model=Post)
def create(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:

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


@router.get("/posts/", response_model=list[Post])
def read_posts(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[Type[Post]]:
    posts = get_posts(db=db, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)) -> Post:
    db_post = get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=Post)
def update(
    post_id: int,
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:
    db_post = update_post(db=db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}", response_model=Post)
def delete(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Post:
    db_post = delete_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
