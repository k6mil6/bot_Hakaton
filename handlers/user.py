from aiogram import types 
from main import bot, dp

exception_message = 'Для получения информации начните общение с ботом: \nhttps://t.me/ttteamUp_Bot'
# user
@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    try:
        # Здесь необходима проверка на наличие в БД, также развилка на создание персонажа и тд.
        await bot.send_message(message.from_user.id, 'Приветствую тебя путник! ')
        await message.delete()
    except:
        await message.reply(exception_message)


@dp.message_handler(commands=['help'])
async def command_help(message : types.Message):
    try:
        # добавить правила
        await bot.send_message(message.from_user.id, 'Видно ты заплутал совсем, друже ниже перечислены правила нашего мира')
        await message.delete()
    except:
        await message.reply(exception_message)
