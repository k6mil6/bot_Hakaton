from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from bot_creation import bot

exception_message = "Для получения информации начните общение с ботом: \nhttps://t.me/ttteamUp_Bot"


async def command_start(message : Message):
    try:
        # Здесь необходима проверка на наличие в БД, также развилка на создание персонажа и тд.
        
        await bot.send_message(message.from_user.id, "Приветствую тебя путник!")
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