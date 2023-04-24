from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, InputMediaPhoto
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_creation import bot, dp
from config import chat_id
from sql.postgre_db import add_task, get_tasks, get_last_task

ADMINS_ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    task_description = State()
    reward = State()

async def cm_start(message: Message):
    chat_admins = await bot.get_chat_administrators(chat_id)
    for admins in chat_admins:
        ADMINS_ID = admins.user.id
    if message.from_user.id == ADMINS_ID and message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await message.answer("Загрузите фото (если нет - напишите: пропустить или /skip) \nДля отмены напишите - /cancel или отмена")

async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Введите имя задания")

async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Введите описание задания")

async def load_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите количество рейтинга, которое получит выполнивший задание")
    
async def load_reward(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['reward'] = int(message.text)
        await add_task(state)
        await state.finish()
        task = await get_last_task()
        task_message = f"{task[1]}\nОписание: {task[2]} \nНаграда: {task[3]}"
        if task[0] == "":
            await bot.send_message(chat_id, task_message)
        else:
            await bot.send_photo(chat_id, task[0], task_message)

    except Exception as ex:
        await message.answer("Неверно указан рейтинг!")
        print(ex)

async def send_tasks(message: Message):
    
    tasks = await get_tasks()
    for i in tasks:
        task_message = f"{i[1]}\nОписание: {i[2]} \nНаграда: {i[3]}"
        if i[0] == "":
            await bot.send_message(message.from_user.id, task_message)
        else:
            await bot.send_photo(message.from_user.id, i[0], task_message)

async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Отменено") 

async def skip_handler(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = ""
    await FSMAdmin.next()
    await message.answer("Введите имя задания")

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Command('cancel'), state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(skip_handler, Text(equals='пропустить', ignore_case=True), state=FSMAdmin.photo)
    dp.register_message_handler(skip_handler, Command('skip'), state=FSMAdmin.photo)
    dp.register_message_handler(cm_start, Command('sendtask'))
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.task_description)
    dp.register_message_handler(load_reward, state=FSMAdmin.reward)
    dp.register_message_handler(send_tasks, Command('tasks'))