import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
import logging

from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from src.config import bot_messages
from src.config.instance import BOT_TOKEN

from src.services.user_service import get_user, create_user
from src.services.client_service import check_code, send_text


dp = Dispatcher()


logger = logging.getLogger("[BOT]")
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    try:
        code = message.text.split(" ")[1]
    except:
        return await message.reply(bot_messages.NOT_AUTHORIZED)

    try:
        uwords_uid = await check_code(code=code)

        if not uwords_uid:
            return await message.answer(text=bot_messages.NOT_AUTHORIZED)

        await create_user(telegram_id=message.from_user.id, uwords_uid=uwords_uid)

        await message.answer(text=bot_messages.SUCCESSFULLY_REG)

        return await message.answer(text=bot_messages.GREETING_MESSAGE)

    except Exception as e:
        logger.info(f"[START] Error: {e}")
        return await message.answer(text=bot_messages.ERROR_MESSAGE)


@dp.message()
async def message(message: Message):
    try:
        user = await get_user(telegram_id=message.from_user.id)
        if not user:
            return await message.answer(bot_messages.NOT_AUTHORIZED)

        is_send = await send_text(uwords_uid=user.uwords_uid, text=message.text)

        if not is_send:
            return await message.answer(text=bot_messages.NOT_SUBSCRIBE)

        return await message.answer(text=bot_messages.SEND_TEXT)

    except Exception as e:
        logger.info(f"[MESSAGE] Error: {e}")
        return await message.answer(bot_messages.ERROR_MESSAGE)


async def main() -> None:
    global bot
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
