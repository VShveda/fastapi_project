from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    user_id: int
    is_banned: bool
    auto_reply_enabled: bool
    reply_delay: Optional[int] = None

    class Config:
        from_attributes = True
