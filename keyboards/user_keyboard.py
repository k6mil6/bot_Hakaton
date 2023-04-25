from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def submit_task_markup():
    markup_for_task_submition = InlineKeyboardMarkup().add(InlineKeyboardButton("Отправить подтверждение", callback_data='submit'))
    return markup_for_task_submition