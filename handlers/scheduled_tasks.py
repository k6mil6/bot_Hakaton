import asyncio

import aioschedule

from bot_creation import bot
from config import CHAT_ID


async def send_task_everyday():
    everyday_message = "Здесь должны быть ежедневные задания"
    await bot.send_message(CHAT_ID, everyday_message)

async def scheduled():
    aioschedule.every().day.at('11:31').do(send_task_everyday)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


