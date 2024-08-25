from aiogram.filters.callback_data import CallbackData


class CancelCallback(CallbackData, prefix="cancel_action"):
    pass
