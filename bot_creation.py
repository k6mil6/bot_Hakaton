from aiogram import Bot, Dispatcher

from config import TOKEN

# loop = asyncio.new_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)