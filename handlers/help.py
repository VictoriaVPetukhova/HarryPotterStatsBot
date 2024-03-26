# здесь код для сообщения-инструкции, где собраны все функции (кроме админских)
from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer(
        f'Cписок доступных команд 🤔:\n'
        f'/available_characters - список доступных персонажей 🧌🧙🧙🏻‍♂️\n'
        f'/choose_character - выбрать персонажа 🧝🏻‍♀️\n'
        f'/available_spells - доступные заклинания 🪄🔮✨\n'
        f'/choose_spell - выбрать заклинание 🌟\n')

