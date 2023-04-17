from aiogram import executor
from bot_creation import dp


if __name__ == '__main__':
    from handlers import user, admin, scheduled_tasks
    user.register_handlers_user(dp)
    admin.register_handlers_admin(dp)
    executor.start_polling(dp, skip_updates=True)
