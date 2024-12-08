from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import async_session_maker
from app.users import current_active_user


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


get_current_active_user = current_active_user
