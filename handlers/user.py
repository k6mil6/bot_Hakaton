from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_creation import bot
from handlers.admin import check_admins
from sql.postgre_db import add_user, get_user_rating, get_users_ratings, is_not_existed
from keyboards.admin_keyboard import get_markup_for_confirmation
from keyboards.user_keyboard import get_markup_for_acception


exception_message = "Для получения информации начните общение с ботом: \nhttps://t.me/ttteamUp_Bot"

class FSMUser(StatesGroup):
    photo = State()
    task_description = State()

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

async def task_submition(callback_query: CallbackQuery):
    try:
        acception_markup = get_markup_for_acception()
        await bot.send_message(callback_query.from_user.id, "Подтвердите выполнение задания", reply_markup=acception_markup)
        await callback_query.answer()

    except Exception as ex:
        print(ex)

async def task_confirmation(callback_query: CallbackQuery):

    await FSMUser.photo.set()
    await bot.send_message(callback_query.from_user.id, "Загрузите фото для подтверждения выполнения задания")
    await callback_query.answer()

async def load_photo_confirmation(message: Message, state: FSMContext):
    
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMUser.next()
    await message.answer("Опишите, что вы сделали")

async def load_description_confirmation(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    confirmation_markup = get_markup_for_confirmation()
    admin_id = await check_admins()
    async with state.proxy() as data:
        msg = list(data.values())
        await bot.send_photo(admin_id, msg[0], f"{msg[1]} \nот {message.from_user.first_name}, @{message.from_user.username}", reply_markup=confirmation_markup)
    await state.finish()


def register_handlers_user(dp: Dispatcher):
    dp.register_callback_query_handler(task_submition, lambda c: c.data == 'submit')
    dp.register_callback_query_handler(task_confirmation, lambda c: c.data == 'confirm')
    dp.register_message_handler(command_start, Command('start'))
    dp.register_message_handler(command_help, Command('help'))
    dp.register_message_handler(command_best_participants, Command('top'))
    dp.register_message_handler(load_photo_confirmation, content_types=['photo'], state= FSMUser.photo)
    dp.register_message_handler(load_description_confirmation, state=FSMUser.task_description)
