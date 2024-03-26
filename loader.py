# в этом файле код для БД и диспетчера
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from utils.db.storage import DatabaseManager

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)
database = DatabaseManager('identifier.sqlite')
