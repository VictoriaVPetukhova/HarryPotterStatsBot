# в этом файле код с командами только для админа
import sqlite3

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.fsm.context import FSMContext

from analyezers.CharacterAnalyzer import CharacterAnalyzer
from filters.IsAdmin import IsAdmin
from states.AdminState import AdminState
from loader import database

router = Router()
analyzer = CharacterAnalyzer()


@router.message(Command('add_admin'), IsAdmin())
async def add_admin(message: types.Message, state: FSMContext):
    await message.answer('Введите id пользователя, которого вы хотите сделать администратором')
    await state.set_state(AdminState.adding_admin)


@router.message(Command('back'), IsAdmin())
async def back(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись назад')
    await state.clear()


@router.message(IsAdmin(), StateFilter(AdminState.adding_admin))
async def adding_admin(message: types.Message, state: FSMContext):
    try:
        database.insert(
            '''
            INSERT INTO admins (user_id) VALUES (?);
            ''',
            (message.text,)
        )
        await message.answer(f'Пользователь с id {message.text} теперь администратор')

    except sqlite3.IntegrityError as e:
        await message.answer(f'Пользователь с id {message.text} уже является администратором')

    await state.clear()


@router.message(Command('add_character'), IsAdmin())  # создание персонажа
async def add_character(message: types.Message, state: FSMContext):
    await message.answer('Введите имя и фамилию персонажа')
    await state.set_state(AdminState.adding_character_name)


@router.message(IsAdmin(), StateFilter(AdminState.adding_character_name))  # краткая информация
async def adding_character_name(message: types.Message, state: FSMContext):
    name, surname = message.text.split(' ')
    await state.update_data(
        character_name=name,
        character_surname=surname
    )
    await message.answer('Введите описание персонажа')
    await state.set_state(AdminState.adding_character_description)


@router.message(IsAdmin(), StateFilter(AdminState.adding_character_description))  # картинка
async def adding_character_description(message: types.Message, state: FSMContext):
    await state.update_data(
        character_description=message.text
    )
    await message.answer('Отправьте ссылку на фото персонажа')
    await state.set_state(AdminState.added_character_description)


@router.message(IsAdmin(), StateFilter(AdminState.added_character_description))  # работа с БД
async def added_character_description(message: types.Message, state: FSMContext):
    await state.update_data(
        character_photo_url=message.text
    )

    character_name = (await state.get_data()).get('character_name')
    character_surname = (await state.get_data()).get('character_surname')
    character_description = (await state.get_data()).get('character_description')
    character_photo_url = (await state.get_data()).get('character_photo_url')

    database.fetchall(
        '''
        INSERT INTO characters (name, surname, description, photo_url) VALUES (?, ?, ?, ?);
        ''',
        (
            character_name,
            character_surname,
            character_description,
            character_photo_url
        )
    )
    await message.answer('Обновляем базу данных и \n'
                         'Собираем статистику...\n'
                         'Это займет некоторое время')
    await analyzer.analyze_character((await state.get_data()).get('character_name'), message)
    await message.answer('Персонаж добавлен')
    await state.clear()


@router.message(Command('add_spell'), IsAdmin())  # создание заклинания
async def add_spell(message: types.Message, state: FSMContext):
    await message.answer('Введите название заклинания')
    await state.set_state(AdminState.adding_spell_name)


@router.message(IsAdmin(), StateFilter(AdminState.adding_spell_name))  # описание
async def adding_spell_name(message: types.Message, state: FSMContext):
    await state.update_data(
        spell_name=message.text
    )
    await message.answer('Введите описание заклинания')
    await state.set_state(AdminState.adding_spell_description)


@router.message(IsAdmin(), StateFilter(AdminState.adding_spell_description))  # картинка
async def adding_spell_description(message: types.Message, state: FSMContext):
    await state.update_data(
        spell_description=message.text
    )
    await message.answer('Отправьте ссылку на фото заклинания')
    await state.set_state(AdminState.added_spell_description)


@router.message(IsAdmin(), StateFilter(AdminState.added_spell_description))  # работа с БД
async def added_spell_description(message: types.Message, state: FSMContext):
    await state.update_data(
        spell_photo_url=message.text
    )

    spell_name = (await state.get_data()).get('spell_name')
    spell_description = (await state.get_data()).get('spell_description')
    spell_photo_url = (await state.get_data()).get('spell_photo_url')

    database.fetchall(
        '''
        INSERT INTO spells (name, description, photo_url) VALUES (?, ?, ?);
        ''',
        (
            spell_name,
            spell_description,
            spell_photo_url
        )
    )
    await message.answer('Обновляем базу данных и \n'
                         'Собираем статистику...\n'
                         'Это займет некоторое время')
    await analyzer.analyze_spell((await state.get_data()).get('spell_name'), message)
    await message.answer('Заклинание добавлено')
    await state.clear()
