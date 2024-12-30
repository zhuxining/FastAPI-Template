import uuid
from typing import Optional

from sqlmodel import SQLModel

from .base_model import BaseModel


class PostBase(SQLModel):
    title: str
    content: str
    published: bool = True
    author_id: uuid.UUID


# database model
class Post(PostBase, BaseModel, table=True):
    __tablename__ = "posts"
    __table_args__ = dict(comment="Posts table")


# pydantic models
class PostCreate(PostBase):
    pass


class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class PostRead(PostBase):
    id: uuid.UUID
