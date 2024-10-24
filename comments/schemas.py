from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    is_banned: bool


class CommentCreate(CommentBase):
    post_id: int
    user_id: int


class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
