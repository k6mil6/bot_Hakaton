import asyncio
import subprocess

from aiogram import executor

from bot_creation import dp, bot
from handlers import admin, scheduled_tasks, user
from sql.postgre_db import sql_start
from config import CHAT_ID



# subprocess.check_call(["pip", "install", "-r", "requirements.txt"])


async def on_startup(_):

    sql_start()
    asyncio.create_task(scheduled_tasks.scheduled())


if __name__ == '__main__':
    
    
    user.register_handlers_user(dp)
    admin.register_handlers_admin(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
