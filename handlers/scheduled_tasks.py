import asyncio
import aioschedule

from bot_creation import bot
from config import chat_id

async def send_task_everyday():
    # Сделать БД с заданиями
    everyday_message = 'QQ'
    await bot.send_message(chat_id, everyday_message)

async def scheduled():
    aioschedule.every().day.at("21:44").do(send_task_everyday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduled())
