from aiogram import Bot, Dispatcher, types, executor

import os

TOKEN = '6193825963:AAFVpKEbQ8veAygTrdBP8ECNfsBCZCrx1Kw'

bot = Bot(token=TOKEN)
# bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

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

# @dp.message_handler()
# async def echo_send(message : types.Message):
#     await message.answer(message.text)
#     await message.reply(message.text)
#     await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp, skip_updates=True)
