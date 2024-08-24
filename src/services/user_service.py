import logging

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.database.db_config import async_session_maker


logger = logging.getLogger("[SERVICES USER]")
logging.basicConfig(level=logging.INFO)


async def create_user(telegram_id: int, uwords_uid: str) -> bool:
    try:
        async with async_session_maker() as session:
            session: AsyncSession
            stmt = insert(User).values(
                {"tg_user_id": telegram_id, "uwords_uid": uwords_uid}
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
            res = await session.execute(stmt)

            return res.scalar_one_or_none()

    except Exception as e:
        logger.info(f"[GET] Error: {e}")
        return None
