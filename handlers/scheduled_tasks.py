import asyncio
import datetime

from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram import Dispatcher

from bot_creation import bot, dp
from config import chat_id

async def send_task_everyday(message: Message):
    everyday_message = 'QQ'
    await bot.send_message(chat_id, everyday_message)

async def scheduled(wait_for):
    while True:
        now = datetime.datetime.now().time()
        scheduled_time = datetime.time(13, 37, 0)
        time_to_wait = datetime.datetime.combine(datetime.date.today(), scheduled_time) - datetime.datetime.combine(datetime.date.today(), now)
        if time_to_wait > wait_for:
            await asyncio.sleep(time_to_wait.seconds)
            await send_task_everyday
def register_handlers_scheduled_tasks(dp: Dispatcher):
    dp.register_message_handler(scheduled)