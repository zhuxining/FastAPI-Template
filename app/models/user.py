from typing import List

from fastapi_users.db import SQLModelBaseUserTableUUID
from sqlmodel import Relationship, SQLModel

from app.models.post import Post


class User(SQLModelBaseUserTableUUID, SQLModel, table=True):
    posts: List["Post"] = Relationship(back_populates="author")

    class Config:
        orm_mode = True
