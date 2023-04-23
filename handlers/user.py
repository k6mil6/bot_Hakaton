from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from sql.postgre_db import add_user, is_not_existed, get_user_rating, get_users_ratings
from bot_creation import bot

exception_message = "Для получения информации начните общение с ботом: \nhttps://t.me/ttteamUp_Bot"

class FSMAdmin(StatesGroup):
    photo = State()
    task_description = State()
    reward = State()

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
        await get_users_ratings()
        await bot.send_message(message.from_user.id, "Топ 10 лучших: \n")
        await message.delete()
    except:
        await message.reply(exception_message)

async def command_help(message : Message):
    try:
        # добавить правила
        await bot.send_message(message.from_user.id, "Видно ты заплутал совсем, друже ниже перечислены правила нашего мира")
        await message.delete()
    except:
        await message.reply(exception_message)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(command_start, Command('start'))
    dp.register_message_handler(command_help, Command('help'))
    dp.register_message_handler(command_best_participants, Command('top'))