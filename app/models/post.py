import uuid
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=True)
    author_id: uuid.UUID
