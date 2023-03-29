from aiogram import Bot, Dispatcher
from decouple import  config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


TOKEN=config('5651777397:AAFTiTgEuG46W-_Ps9WH3wj1JQD0IjB78hk')

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN_ID = [661114436,]
