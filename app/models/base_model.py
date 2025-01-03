import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, func


class BaseModel(SQLModel):
    __abstract__ = True

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"comment": "主键ID, UUID v4"},
    )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.current_timestamp(),
            comment="创建时间, timestamptz",
        )
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            onupdate=func.current_timestamp(),
            comment="更新时间, timestamptz",
        ),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column_kwargs={"comment": "是否软删除"},
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), comment="删除时间, timestamptz"),
    )
