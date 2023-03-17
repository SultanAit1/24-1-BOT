
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from config import bot, dp
from keyboards.client_kb import start_markup, main_markup, url_markup



@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
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




def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.callback_query_handler(one, text='one')
    dp.callback_query_handler(two, text='two')
    dp.callback_query_handler(three, text='three')
    dp.callback_query_handler(last, text='last')
    dp.callback_query_handler(exit_1, text='exit_1')
    dp.register_edited_message_handler(one)

