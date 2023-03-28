import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ChatType

from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup, confirm_broadcast_keyboard
import sqlite3
from aiogram import Dispatcher
from aiogram import types


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY)
                """)
conn.commit()


# # noinspection SqlResolve
# @dp.message_handler(content_types=['photo', 'video'])
# async def handle_all(message: types.Message):
#     media_group = []
#     for media in [message.photo[-1], message.video]:
#         media_id = media.file_id
#         media_group.append(types.InputMedia(media=media_id, caption=message.caption[6:]))
#
#     try:
#         cursor.execute("SELECT user_id FROM users")
#         rows = cursor.fetchall()
#         for row in rows:
#             user_id = row[0]
#             await bot.send_media_group(chat_id=user_id, media=media_group)
#         await message.answer(f"Медиа-файлы успешно отправлены всем подписчикам ({len(rows)} человек).")
#     except Exception as e:
#         print(f"Ошибка при отправке медиа-файлов: {e}")# # noinspection SqlResolve
@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    # Получаем идентификатор фото
    video_id = message.video.file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_video(chat_id=user_id, video=video_id,caption=message.caption[6:] )
        await message.answer(f"Видео успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")

# noinspection SqlResolve
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    # Получаем идентификатор фото
    photo_id = message.photo[-1].file_id
    try:
        # Отправляем фото всем подписчикам
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        for row in rows:
            user_id = row[0]
            await bot.send_photo(chat_id=user_id, photo=photo_id,caption=message.caption[6:] )
        await message.answer(f"Фото успешно отправлено всем подписчикам ({len(rows)} человек).")
    except Exception as e:
        print(f"Ошибка при отправке фото: {e}")


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


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.chat.id
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


conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY)''')
conn.commit()

@dp.message_handler(content_types=["new_chat_members"])
async def new(message: types.Message):
    # Записываем айди пользователя в базу данных
    user_id = message.new_chat_members[0].id
    cursor.execute('''INSERT OR REPLACE INTO  members (id) VALUES (?)''', (user_id,))
    conn.commit()


# Обработка команды для вывода количества подписчиков
@dp.message_handler(commands=["subscribers"])
async def get(message: types.Message):
    # Проверяем, является ли отправитель администратором группы
    if message.from_user.id != (await bot.get_chat_member(message.chat.id, message.from_user.id)).user.id:
        return
    # Запрос количества подписчиков группы
    count = await bot.get_chat_members_count(message.chat.id)
    await message.answer(f"Subscribers count: {count}")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.callback_query_handler(cancel, text='cancel')
    dp.register_message_handler(get, commands=['subscribers'])
    dp.register_message_handler(new, commands=['new'])


    dp.callback_query_handler(confirm_broadcast_keyboard, text_contains='confirm_broadcast')
    dp.register_message_handler(spam_commands, commands=['spam'])
    # dp.register_message_handler(handle_all, commands=['spam'])
    dp.register_message_handler(handle_photo, commands=['spam'])
    dp.register_message_handler(handle_video, commands=['spam'])



