from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.user import User


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    content: str
    published: bool = Field(default=True)
    author_id: int = Field(foreign_key="user.id")

    author: Optional[User] = Relationship(back_populates="posts")
