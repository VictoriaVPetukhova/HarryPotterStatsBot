# в этом файле представлен код для запуска самого бота

import asyncio
import logging

from handlers import start, help, characters, admin, spells
from loader import dispatcher, database, bot


def on_startup():  # хендлеры
    logging.basicConfig(level=logging.INFO)
    database.create_tables()

    dispatcher.include_router(admin.router)
    dispatcher.include_router(start.router)
    dispatcher.include_router(help.router)
    dispatcher.include_router(characters.router)
    dispatcher.include_router(spells.router)


async def main():  # запуск бота
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    on_startup()
    asyncio.run(main())
