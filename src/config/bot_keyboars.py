from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from src.config.bot_callbacks import CancelCallback


def get_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Uwords"))
    builder.add(KeyboardButton(text="Промокод"))

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


def get_cancel_keyboard():
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="Отмена", callback_data=CancelCallback().pack())
    )

    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)
