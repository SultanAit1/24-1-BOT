
from aiogram.types import InlineKeyboardButton, CallbackQuery
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup, profil_markup
import sqlite3
from aiogram import Dispatcher
from aiogram import types
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY)
                """)
conn.commit()



# noinspection SqlResolve
@dp.message_handler(content_types=['voice'])
async def handle_voice(message: types.Message):
    if message.from_user.id != 661114436:
        return
        voice_id = message.voice.file_id
        try:
            # Отправляем фото всем подписчикам
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            for row in rows:
                user_id = row[0]
                await bot.send_voice(chat_id=user_id, voice=voice_id)
                await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
        except Exception as e:
            print(f"Ошибка при отправке видео: {e}")


# noinspection SqlResolve
@dp.message_handler(content_types=['video_note'])
async def handle_note(message: types.Message):
    if message.from_user.id != 661114436:
        return
        video_note_id = message.video_note.file_id
        try:
            # Отправляем фото всем подписчикам
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            for row in rows:
                user_id = row[0]
                await bot.send_video_note(chat_id=user_id, video_note=video_note_id)
                await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
        except Exception as e:
            print(f"Ошибка при отправке видео: {e}")




# noinspection SqlResolve
@dp.message_handler(commands=['/spam'])
async def spam_commands(message: types.Message):

    # Проверка, что отправитель является администратором
    if message.from_user.id != 661114436:
        await message.answer("Вы не являетесь администратором.")
        return

    # Получение всех подписчиков из базы данных
    cursor.execute("SELECT user_id FROM users")
    rows = cursor.fetchall()

    # Отправка сообщения всем подписчикам
    for row in rows:
        user_id = row[0]
        try:
            # Определение типа сообщения
            if message.photo:
                photo_id = message.photo[-1].file_id
                photo_obj = await bot.get_file(photo_id)
                photo = photo_obj.download()
                await bot.send_photo(chat_id=user_id, photo=open(photo, 'rb'))
            elif message.video:
                await bot.send_video(chat_id=user_id, video=message.video.file_id, caption=message.caption[6:])
            else:
                await bot.send_message(chat_id=user_id, text=message.text[6:])
        except Exception as e:
            print(f"Ошибка при отправке сообщения для пользователя {user_id}: {e}")

    await message.answer(f"Сообщение успешно отправлено всем подписчикам ({len(rows)} человек).")


# class UserStates(StatesGroup):
#     waiting_for_start = State()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.chat.id
    cursor.execute("INSERT OR REPLACE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    if message.from_user.id != 661114436:
        await bot.send_message(chat_id=message.from_user.id,
        text="Вступительная информацию",
        reply_markup=start_markup)

    else:
        await bot.send_message(chat_id=message.from_user.id, text='Вступительная информацию', reply_markup=profil_markup)
    # await UserStates.waiting_for_start.set()
    # await state.update_data(user_id=message.from_user.id, username=message.from_user.username)
    # # отправляем уведомление администратору
    # await bot.send_message(661114436,
    #                        f"Пользователь {message.from_user.id} ({message.from_user.username}) начал использовать бота")


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


@dp.callback_query_handler(text="comand")
async def comand(callback: CallbackQuery):
    comand = InlineKeyboardButton('comand', callback_data='comand')
    await bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.message_id,
                                text=" основное меню - /start;       "
                                   '           Кружочки в тг - автоматически;     '
                                   '                        фото с текстом - /spam;     '
                                   '                   видео с текстом - /spam;      '
                                   '  голосовое сообщение - автоматически.  ',
                                reply_markup=main_markup

    )

@dp.message_handler(commands=["follow"])
async def get_subscribers_count(message: types.Message):
    if message.from_user.id != (await bot.get_chat_member(message.chat.id, message.from_user.id)).user.id:
        return
    count = await bot.get_chat_members_count(message.chat.id)
    await message.answer(f"количество подписчиков бота: {count}")

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(get_subscribers_count, commands=['follow'])
    dp.register_message_handler(start_handler, commands=['start'])
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.callback_query_handler(comand, text='comand')
    dp.register_message_handler(handle_note, commands=['note'])
    dp.register_message_handler(spam_commands, commands=['spam'])
    dp.register_message_handler(handle_voice, commands=['voice'])





