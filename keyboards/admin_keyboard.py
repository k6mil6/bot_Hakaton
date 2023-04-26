from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_markup_for_managing(name):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Удалить", callback_data=f'del {name}'),\
                                                 InlineKeyboardButton("Отправить повторно", callback_data=f'resend {name}'))
def get_markup_for_confirmation():
    return InlineKeyboardMarkup().add(InlineKeyboardButton("Подтвердить", callback_data='confirm'),\
                                      InlineKeyboardButton("Удалить", callback_data='delete'))