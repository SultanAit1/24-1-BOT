from aiogram import Bot, Dispatcher



from handlers import client
from config import dp
import logging
from aiogram.utils import executor
import sqlite3
from decouple import config
client.register_handlers_client(dp)


TOKEN=config('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
ADMIN_ID = [661114436,]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)