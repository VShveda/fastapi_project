from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from posts.crud import (
    create_post,
    get_post,
    get_posts,
    update_post,
    delete_post
)
from posts.schemas import PostCreate, Post
from db.database import get_db


router = APIRouter()


@router.post("/posts/", response_model=Post)
def create(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    return create_post(db=db, post=post, user_id=user_id)


@router.get("/posts/", response_model=list[Post])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = get_posts(db=db, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/posts/{post_id}", response_model=Post)
def update(post_id: int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = update_post(db=db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}", response_model=Post)
def delete(post_id: int, db: Session = Depends(get_db)):
    db_post = delete_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
