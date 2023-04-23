from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot_creation import bot, dp
from config import chat_id


class FSMAdmin(StatesGroup):
    photo = State()
    task_description = State()
    reward = State()

async def cm_start(message: Message):
    chat_admins = await bot.get_chat_administrators(chat_id)
    for admins in chat_admins:
        admins_id = admins.user.id
    if message.from_user.id == admins_id and message.chat.type == 'private':
        await FSMAdmin.photo.set()
        await message.answer("Загрузите фото (если нет - отправьте -) \nДля отмены напишите - /cancel или отмена")

async def load_photo(message: Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Введите описание задания")

async def load_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Укажите количество рейтинга, которое получит выполнивший задание")
    
async def load_reward(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['reward'] = int(message.text)
        async with state.proxy() as data:
            await message.answer(str(data))
        await state.finish()
    except:
        await message.answer("Неверно указан рейтинг!")

async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Отменено") 

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cancel_handler, Command('cancel'), state="*")
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(cm_start, Command('sendtask'))
    dp.register_message_handler(load_photo, state=FSMAdmin.photo)
    dp.register_message_handler(load_description, state=FSMAdmin.task_description)
    dp.register_message_handler(load_reward, state=FSMAdmin.reward)