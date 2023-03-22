from config import  ADMIN_ID
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup, spam_markup
import sqlite3
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.exceptions import ChatNotFound





conn = sqlite3.connect('users.db')
cursor = conn.cursor()
conn.commit()



cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY)
                """)

conn.commit()



class SpamStates(StatesGroup):
    message = State()
    photo = State()
    video = State()


@dp.message_handler(commands=["spam"])
async def spam(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Отправьте текст сообщения для спама:")
    await SpamStates.message.set()


@dp.message_handler(state=SpamStates.message)
async def set_spam_message(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id, text=message.text, parse_mode=ParseMode.HTML)
        except ChatNotFound:
            pass

  # переходим к отправке фото
    await message.answer("Отправьте фото (опционально):")
    await SpamStates.photo.set()


@dp.message_handler(content_types=types.ContentType.PHOTO, state=SpamStates.photo)
async def set_spam_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)

    await message.answer("Отправьте видео (опционально):")
    await SpamStates.video.set()



@dp.message_handler(content_types=types.ContentType.VIDEO, state=SpamStates.video)
async def set_spam_video(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_text = data.get("message")
    photo_id = data.get("photo")
    video_id = message.video.file_id
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    for user_id in users:
        try:
            await bot.send_photo(chat_id=user_id, photo=photo_id, caption=message_text, parse_mode=ParseMode.HTML)
            await bot.send_video(chat_id=user_id, video=video_id)
        except ChatNotFound:
            pass
    await state.finish()
    await message


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR REPLACE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await bot.send_message(chat_id=message.from_user.id,
                           text="Вступительная информацию",
                           reply_markup=start_markup)



@dp.callback_query_handler(text="one")
async def one(callback: CallbackQuery):
    one = InlineKeyboardButton("one", callback_data="one")
    await bot.edit_message_text("Вступительная инфа",chat_id=callback.message.chat.id,message_id=callback.message.message_id,reply_markup=main_markup)




@dp.callback_query_handler(text="two")
async def two(callback: CallbackQuery):
    two = InlineKeyboardButton('two', callback_data='two')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id, text="партнерство с нами ",
                        reply_markup=main_markup   )


@dp.callback_query_handler(text="three")
async def three(callback: CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id ,text="тут наши товары",
                          reply_markup=url_markup, )


@dp.callback_query_handler(text="last")
async def last(message: types.Message, ):
    last = InlineKeyboardButton('last', callback_data='last')
    await bot.send_message(chat_id=message.from_user.id, text="")


@dp.callback_query_handler(text="exit_1")
async def exit_1(callback: CallbackQuery):
    exit_1 = InlineKeyboardButton('exit_1', callback_data="exit_1")
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id, text="вступительная инфа ",
                           reply_markup=start_markup)

@dp.callback_query_handler(lambda c: c.data == 'cancel')
async def cancel(callback :CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id, text='Рассылка отменена')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.register_message_handler(spam, commands=['spam'])
    dp.callback_query_handler(cancel, text='cancel')
    dp.register_message_handler(set_spam_message, state=SpamStates.message)
    dp.register_message_handler(set_spam_photo, state=SpamStates.photo)
    dp.register_message_handler(set_spam_video, state=SpamStates.video)



