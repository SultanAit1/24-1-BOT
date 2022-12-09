from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import logging

TOKEN = config("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Салам хозяин {message.from_user.first_name}")
    await message.answer("This is an answer method")
    await message.reply("This is a reply method")


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT 1", callback_data="button_call_1")
    markup.add(button_call_1)

    question = "Центральный город КР"
    answers = [
        'Ош',
        'Бишкек',
        'Каракол',
        'Москва',
        'Токмок',
    ]

    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Стыдно не знать",
        open_period=5,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT 2", callback_data="button_call_2")
    markup.add(button_call_1)

    question = "By whom invented Python?"
    answers = [
        "Harry Potter",
        "Putin",
        "Guido Van Rossum",
        "Voldemort",
        "Griffin",
        "Linus Torvalds",
    ]

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Стыдно не знать",
        open_period=5,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_call_2")
async def quiz_3(call: types.CallbackQuery):
    question = "АТВИЧАЙ"
    answers = [
        '4',
        '8',
        '4, 6',
        '2, 4',
        '5',
    ]

    photo = open("media/problem1.jpg", "rb")
    await bot.send_photo(call.from_user.id, photo=photo)

    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Стыдно не знать",
        # open_period=5,
    )


@dp.message_handler()
async def echo(message: types.Message):
    # print(message)
    await bot.send_message(chat_id=message.from_user.id, text=message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
