import asyncio
import subprocess

from aiogram import executor

from bot_creation import dp, bot



# subprocess.check_call(["pip", "install", "-r", "requirements.txt"])


    

if __name__ == '__main__':
    from handlers import admin, scheduled_tasks, user
    user.register_handlers_user(dp)
    admin.register_handlers_admin(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=scheduled_tasks.on_startup)
