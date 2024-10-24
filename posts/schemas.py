from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int
    is_banned: bool

    class Config:
        from_attributes = True
