from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from main import bot, dp
from config import admin_id, chat_id

@dp.message_handler(Command('sendnewtask'))
async def send_new_task(message: Message):
    if message.chat.id == admin_id:
        await message.answer('Start')
        await bot.send_message(chat_id, message.text[message.text.find(' '):])

        await message.answer('Done')
    else:
        await message.answer('Error')