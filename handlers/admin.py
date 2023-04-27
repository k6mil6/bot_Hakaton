from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_creation import bot
from config import CHAT_ID
from sql.postgre_db import add_task, get_tasks, get_last_task, add_rating_to_user
from keyboards.admin_keyboard import get_markup_for_managing
from keyboards.user_keyboard import get_markup_for_submition



class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    task_description = State()
    reward = State()

async def check_admins():
    chat_admins = await bot.get_chat_administrators(CHAT_ID)
    admins_id = 0
    for admins in chat_admins:
        admins_id = admins.user.id
    return admins_id

async def cm_start(message: Message):
    admin_id = await check_admins()
    if message.from_user.id == admin_id and message.chat.type == 'private':
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
        submition_markup = get_markup_for_submition()
        if task[0] == "":
            await bot.send_message(CHAT_ID, task_message, reply_markup=submition_markup)
        else:
            await bot.send_photo(CHAT_ID, task[0], task_message, reply_markup=submition_markup)

    except Exception as ex:
        await message.answer("Неверно указан рейтинг!")
        print(ex)

async def send_task_list(message: Message):
    admin_id = await check_admins()
    if message.from_user.id == admin_id and message.chat.type == 'private':
        tasks = await get_tasks()
        for i in tasks:
            managing_markup = get_markup_for_managing(i[1])
            task_message = f"{i[1]}\nОписание: {i[2]} \nНаграда: {i[3]}"
            if i[0] == "":
                await bot.send_message(message.from_user.id, task_message, reply_markup=managing_markup)
            else:
                await bot.send_photo(message.from_user.id, i[0], task_message, reply_markup=managing_markup)

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

async def delete_user_prof(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()

async def accept_user_prof(callback_query: CallbackQuery):
    cur_task = await get_last_task()
    rating = cur_task[3]
    user_id = callback_query.message.from_user.id
    await add_rating_to_user(rating, user_id)
    await callback_query.message.delete()
    await callback_query.answer()

def register_handlers_admin(dp: Dispatcher):
    dp.register_callback_query_handler(delete_user_prof, lambda c: c.data == 'delete')
    dp.register_callback_query_handler(accept_user_prof, lambda c: c.data == 'accept')
    dp.register_message_handler(cancel_handler, Command('cancel'), state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(skip_handler, Text(equals='пропустить', ignore_case=True), state=FSMAdmin.photo)
    dp.register_message_handler(skip_handler, Command('skip'), state=FSMAdmin.photo)
    dp.register_message_handler(cm_start, Command('sendtask'))
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.task_description)
    dp.register_message_handler(load_reward, state=FSMAdmin.reward)
    dp.register_message_handler(send_task_list, Command('tasks'))