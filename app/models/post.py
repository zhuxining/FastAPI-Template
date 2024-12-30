import uuid
from datetime import datetime

from sqlmodel import SQLModel

from .base_model import BaseModel


class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True


# database model
class Post(PostBase, BaseModel, table=True):
    __tablename__ = "posts"
    __table_args__ = dict(comment="Posts table")

    author_id: uuid.UUID


# pydantic models
class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None


class PostUpdate(PostBase):
    pass
