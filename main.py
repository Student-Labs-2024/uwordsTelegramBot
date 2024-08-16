import sys
import asyncio
import logging
import aiohttp
import requests

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_config import async_session_maker
from database.models import User
from instance import BOT_TOKEN, SECRET, NODE

dp = Dispatcher()
users = {}


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    try:
        code = message.text.split(" ")[1]
    except:
        await message.reply("You are not authorized")
        return
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{NODE}/api/users/telegram/check_code", json={"code": code}
        ) as response:
            res_text = await response.text()
    if res_text != "false":
        async with async_session_maker() as session:
            session: AsyncSession
            stmt = insert(User).values(
                {"tg_user_id": message.from_user.id, "main_api_user_id": int(res_text)}
            )
            await session.execute(stmt)
            await session.commit()
    else:
        print(False)


@dp.message()
async def message(message: Message):
    async with async_session_maker() as session:
        session: AsyncSession

        stmt = select(User).filter(User.tg_user_id == message.from_user.id)
        user: User = await session.execute(stmt)
        if not user:
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NODE}/api/v1/user/bot_word",
                    json={
                        "secret": SECRET,
                        "user_id": users[message.from_user.id],
                        "text": message.text,
                    },
                ) as response:
                    if user.notice:
                        user.notice = False
                        await session.commit()
                    if response.status_code == 400:
                        if not user.notice:
                            user_id = message.from_user.id
                            await bot.send_message(
                                user_id, f"You need to subscribe to use this bot"
                            )
                            user.notice = True
                            await session.commit()
        except:
            return


async def main() -> None:
    global bot
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
