import aioschedule
from aiogram import types, Dispatcher
from config import bot
import asyncio


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await message.answer("Ok")


async def go_to_sleep():
    await bot.send_message(chat_id=chat_id, text="Занятие начинается в 18:00, аудитории 3!(Backend)")


async def wake_up():
    await bot.send_message(chat_id=chat_id,
                           text="иди на урок!!!")


async def scheduler():
    aioschedule.every().tuesday.at("13:00").do(go_to_sleep)
    aioschedule.every().tuesday.at("16:30").do(wake_up)
    aioschedule.every().friday.at("13:00").do(go_to_sleep)
    aioschedule.every().friday.at("16:30").do(wake_up)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handlers_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'Напомни' in word.text)