from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from bot_creation import bot
from handlers.admin import check_admins
from sql.postgre_db import add_user, get_user_rating, get_users_ratings, is_not_existed

exception_message = "Для получения информации начните общение с ботом: \nhttps://t.me/ttteamUp_Bot"

async def command_start(message : Message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        if await is_not_existed(user_id):
            await message.answer("Приветствую тебя, путник!")
            await add_user(user_id)
        else:
            rating = await get_user_rating(user_id)
            await message.answer(f"Давно не виделись, друже. \nКстати, вот твой рейтинг: {rating}")

async def command_best_participants(message : Message):
    try:
        top = await get_users_ratings()
        await bot.send_message(message.from_user.id, f"Топ 10 лучших: \n{top}")
        await message.delete()
    except:
        await message.reply(exception_message)

async def command_help(message : Message):
    try:
        admin_id = await check_admins()
        if message.from_user.id == admin_id:
            await bot.send_message(message.from_user.id, "Основные команды: \n/start - посмотреть текущий рейтинг \n/top - топ игроков \n/tasks - последние задания \
                                                          \n/sendtask - отправить задание \n/cancel - отменить отправку")
            await message.delete()

        else:
            await bot.send_message(message.from_user.id, "Основные команды: \n/start - посмотреть текущий рейтинг \n/top - топ игроков")
            await message.delete()
    except:
        await message.reply(exception_message)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(command_start, Command('start'))
    dp.register_message_handler(command_help, Command('help'))
    dp.register_message_handler(command_best_participants, Command('top'))