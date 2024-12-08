from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from app.core.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="author")
