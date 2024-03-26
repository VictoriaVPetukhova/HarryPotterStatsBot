# этот код нужен для отправки пользователю сообщения с приветсвием
import os

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile

router = Router()


@router.message(Command('start'))
async def help_command(message: types.Message):
    await message.answer_photo(
        photo=FSInputFile(os.path.join(os.getcwd(), 'data', 'assets', 'start.jpg')),
        caption=
        f'Првиет, {message.from_user.first_name}! Я бот, '
        'который поможет тебе узнать тебе некоторую статистику из книг о Гарри Поттере!\n'
        'Для начала работы воспользуйся командой /help\n',
    )
