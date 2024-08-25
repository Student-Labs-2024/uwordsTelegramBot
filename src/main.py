import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import asyncio
import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from src.config import bot_messages
from src.config import bot_keyboars
from src.config.instance import BOT_TOKEN, UPLOAD_DIR
from src.config.bot_callbacks import CancelCallback

from src.services.user_service import get_user, create_user, change_state
from src.services.client_service import check_code, send_promo, send_text, send_audio


dp = Dispatcher()


logger = logging.getLogger("[BOT]")
logging.basicConfig(level=logging.INFO)


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    keyboard = bot_keyboars.get_menu_kb()

    user = await get_user(telegram_id=message.from_user.id)

    try:
        code = message.text.split(" ")[1]
    except:
        if not user:
            return await message.reply(
                bot_messages.NOT_AUTHORIZED, reply_markup=keyboard
            )

    try:
        if user:
            return await message.reply(
                text=bot_messages.GREETING_MESSAGE, reply_markup=keyboard
            )

        uwords_uid = await check_code(code=code)

        if not uwords_uid:
            return await message.reply(
                text=bot_messages.NOT_AUTHORIZED, reply_markup=keyboard
            )

        await create_user(telegram_id=message.from_user.id, uwords_uid=uwords_uid)

        await message.reply(text=bot_messages.SUCCESSFULLY_REG, reply_markup=keyboard)

        return await message.reply(
            text=bot_messages.GREETING_MESSAGE, reply_markup=keyboard
        )

    except Exception as e:
        logger.info(f"[START] Error: {e}")
        return await message.reply(
            text=bot_messages.ERROR_MESSAGE, reply_markup=keyboard
        )


@dp.message(lambda message: message.text == "Uwords")
async def info_message(message: Message):
    return await message.answer(
        text=bot_messages.INFO_MESSAGE.format(name=message.from_user.first_name)
    )


@dp.message(lambda message: message.text == "Промокод")
async def promo_message(message: Message):
    user = await get_user(telegram_id=message.from_user.id)
    if not user:
        return await message.reply(bot_messages.NOT_AUTHORIZED)

    await change_state(telegram_id=user.tg_user_id, state="promocode")

    keyboard = bot_keyboars.get_cancel_keyboard()

    return await message.reply(text=bot_messages.PROMO_MESSAGE, reply_markup=keyboard)


@dp.callback_query(CancelCallback.filter())
async def get_mail_cancel(query: CallbackQuery, callback_data: CancelCallback):

    try:
        await bot.delete_message(
            chat_id=query.message.chat.id, message_id=query.message.message_id
        )
    except:
        pass

    return await change_state(telegram_id=query.message.chat.id, state="default")


@dp.message(lambda message: message.content_type == ContentType.TEXT)
async def text_message(message: Message):
    user = await get_user(telegram_id=message.from_user.id)
    if not user:
        return await message.reply(bot_messages.NOT_AUTHORIZED)

    if user.state == "promocode":
        is_promo = await send_promo(uwords_uid=user.uwords_uid, promo=message.text)

        if is_promo:
            await change_state(telegram_id=user.tg_user_id, state="default")
            return await message.reply(text=bot_messages.PROMO_SUCCESS)

        return await message.reply(text=bot_messages.PROMO_FAIL)

    try:
        is_send = await send_text(uwords_uid=user.uwords_uid, text=message.text)

        if not is_send:
            return await message.reply(text=bot_messages.NOT_SUBSCRIBE)

        return await message.reply(text=bot_messages.SEND_TEXT)

    except Exception as e:
        logger.info(f"[MESSAGE] Error: {e}")
        return await message.reply(bot_messages.ERROR_MESSAGE)


@dp.message(lambda message: message.content_type == ContentType.VOICE)
async def audio_message(message: Message):
    try:
        user = await get_user(telegram_id=message.from_user.id)
        if not user:
            return await message.reply(bot_messages.NOT_AUTHORIZED)

        file_id = str(message.voice.file_id)
        file = await bot.get_file(file_id)
        file_path = file.file_path

        filename = f"{file_id}.ogg"

        download_path = UPLOAD_DIR / filename

        await bot.download_file(file_path=file_path, destination=download_path)

        is_send = await send_audio(
            uwords_uid=user.uwords_uid,
            file_path=download_path,
            filename=filename,
            content_type="audio/ogg",
        )

        if not is_send:
            return await message.reply(text=bot_messages.NOT_SUBSCRIBE)
        return await message.reply(text=bot_messages.SEND_AUDIO)

    except Exception as e:
        logger.info(f"[MESSAGE] Error: {e}")
        return await message.reply(bot_messages.ERROR_MESSAGE)

    finally:
        try:
            os.remove(download_path)
        except:
            pass


async def main() -> None:
    global bot
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
