from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_markup_for_managing(name):
    markup_for_managing = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Удалить", callback_data=f'del {name}'),\
                                                                         InlineKeyboardButton("Отправить повторно", callback_data=f'resend {name}'))
    return markup_for_managing
