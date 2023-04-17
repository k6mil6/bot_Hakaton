from aiogram import Bot, Dispatcher, executor
import asyncio

from config import TOKEN

loop = asyncio.new_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handlers.admin import dp
    executor.start_polling(dp)
