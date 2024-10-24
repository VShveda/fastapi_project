from datetime import timedelta

from sqlalchemy import Column, Integer, String, Boolean, Interval
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    auto_reply_enabled = Column(Boolean, default=False)
    reply_time = Column(Interval, default=timedelta(minutes=1))

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
