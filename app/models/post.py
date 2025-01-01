import uuid

# from typing import Optional
from sqlmodel import Field, SQLModel

from .base_model import BaseModel


class PostBase(SQLModel):
    title: str = Field(sa_column_kwargs={"comment": "标题"})
    content: str | None = Field(default=None, nullable=True, sa_column_kwargs={"comment": "内容"})
    is_published: bool = Field(default=True, sa_column_kwargs={"comment": "是否发表"})


# database model
class Post(PostBase, BaseModel, table=True):
    __tablename__ = "posts"
    __table_args__ = dict(comment="Posts table")

    author_id: uuid.UUID = Field(sa_column_kwargs={"comment": "作者ID, UUID v4"})


# pydantic models
class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostRead(PostBase, BaseModel):
    pass
