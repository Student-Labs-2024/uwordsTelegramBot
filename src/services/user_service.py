import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.database.db_config import async_session_maker


logger = logging.getLogger("[SERVICES USER]")
logging.basicConfig(level=logging.INFO)


async def create_user(telegram_id: int, app_id: int) -> bool:
    try:
        async with async_session_maker() as session:
            session: AsyncSession
            stmt = insert(User).values(
                {"tg_user_id": telegram_id, "main_api_user_id": app_id}
            )
            await session.execute(stmt)
            await session.commit()
            return True
    except Exception as e:
        logger.info(f"[CREATE] Error: {e}")
        return False


async def get_user(telegram_id: int) -> User:
    try:
        async with async_session_maker() as session:
            session: AsyncSession

            stmt = select(User).filter(User.tg_user_id == telegram_id)
            user = await session.execute(stmt)

            return user

    except Exception as e:
        logger.info(f"[GET] Error: {e}")
        return None
