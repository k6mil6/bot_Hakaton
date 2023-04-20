from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram import Dispatcher

from bot_creation import bot, dp
from config import admin_id, chat_id

# @dp.message_handler(Command('sendnewtask'))
async def send_new_task(message: Message):
    if message.chat.id == admin_id and message.chat.type == 'private':
        await bot.send_message(chat_id, message.text[message.text.find(' '):])
        await message.answer('Задания отправлены успешно')
    else:
        await message.answer('Ошибка')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(send_new_task, Command('sendnewtask'))