from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_markup_for_submition():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Откликнуться", callback_data='submit'))

def get_markup_for_acception():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Подтвердить", callback_data='confirm'))
    