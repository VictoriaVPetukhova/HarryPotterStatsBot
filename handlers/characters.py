# здесь код для выбора персонажа и поиска статистики по нему
import os

import textwrap

import matplotlib.pyplot as plt

from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from loader import database
from states.CharacterStatsState import CharacterStatsState
from keyboards import keyboard

router = Router()


@router.message(Command('choose_character'))  # выбор персонажа
async def choose_character(message: types.Message, state: FSMContext):
    characters = database.fetchall(
        '''
        SELECT characters.name, characters.surname FROM characters
        JOIN characters_books ON characters.id = characters_books.character_id
        GROUP BY characters.name
        ORDER BY characters_books.count
        LIMIT 5;
        '''
    )
    characters = [str(character[0]) + ' ' + str(character[1]) for character in characters]
    await message.answer(
        text='Выберите или напишите имя персонажа',
        reply_markup=keyboard.make_keyboard(
            *characters,
            'cлучайный персонаж'
        )
    )
    await state.set_state(CharacterStatsState.picking_character)


@router.message(Command('back'))
async def back(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись назад')
    await state.clear()


@router.message(StateFilter(CharacterStatsState.picking_character))  # можно выбрать на радном
async def pick_character(message: types.Message, state: FSMContext):
    character_name = message.text

    if character_name == 'cлучайный персонаж':
        character_name = await random_character(message)

    name, surname = character_name.split(' ')

    character = database.fetchone(
        '''
        SELECT description, photo_url FROM characters
        WHERE name = ? AND surname = ?;
        ''',
        (name, surname)
    )

    if character is None:    # проверяем, что такой персонаж существует
        await message.answer(
            text='Персонаж не найден'
        )
        await state.clear()
        return

    await state.update_data(
        character_name=name,
        character_surname=surname,
        character_description=character[0],
        character_photo_url=character[1]
    )

    await state.set_state(CharacterStatsState.picked_character)

    await message.answer_photo(
        photo=character[1],
        caption=name + ' ' + surname + '\n' + character[0],
        reply_markup=keyboard.make_keyboard('/choose_book')
    )


@router.message(Command('choose_book'), StateFilter(CharacterStatsState.picked_character)  # выбор книги
async def choosing_book(message: types.Message, state: FSMContext):
    books = database.fetchall(
        '''
                SELECT books.name FROM books
                JOIN characters_books ON books.id = characters_books.book_id
                JOIN characters ON characters.id = characters_books.character_id
                WHERE characters.name = ? AND characters.surname = ?
                ORDER BY characters_books.count
                LIMIT 5;
                ''',
        ((await state.get_data())['character_name'], (await state.get_data())['character_surname']),
    )
    books = [book[0] for book in books]
    await message.answer(
        text='Выберите или напишите название книги',
        reply_markup=keyboard.make_keyboard(
            *books,
            'cлучайная книга',
            'все книги'
        )
    )

    await state.set_state(CharacterStatsState.picking_book)


@router.message(StateFilter(CharacterStatsState.picking_book))
async def picking_book(message: types.Message, state: FSMContext):
    book_name = message.text

    if book_name == 'cлучайная книга':
        await state.update_data(book_names=list(await random_book(message)))

    elif book_name == 'все книги':
        book_names = database.fetchall(
            '''
            SELECT books.name FROM books
            '''
        )
        book_names = [book[0] for book in book_names]
        await state.update_data(book_names=book_names)

    else:
        book_names = database.fetchall(
            '''
            SELECT books.name FROM books
            '''
        )
        book_names = [book[0] for book in book_names]
        if book_name not in book_names:
            await message.answer(
                text='Книга не найдена'
            )
            await state.clear()
            return
        await state.update_data(book_names=[book_name])

    await message.answer('Выберите опцию', reply_markup=keyboard.make_keyboard('/get_stats'))  # получение статистики

    await state.set_state(CharacterStatsState.picked_book)


@router.message(Command('get_stats'), StateFilter(CharacterStatsState.picked_book))
async def get_character_stats(message: types.Message, state: FSMContext):
    context = await state.get_data()
    character_name = context['character_name']
    character_surname = context['character_surname']
    book_names = context['book_names']

    result = []

    for book_name in book_names:
        count = database.fetchone(
            '''
            SELECT count FROM characters_books
            JOIN characters ON characters_books.character_id = characters.id
            JOIN books ON characters_books.book_id = books.id
            WHERE characters.name = ? AND characters.surname = ? AND books.name = ?;
            ''',
            (character_name, character_surname, book_name)
        )[0]

        result.append((book_name, count))

    labels, values = zip(*result)

    labels = [textwrap.fill(label, 10) for label in labels]

    plt.figure(figsize=(23, 10))

    plt.bar(labels, values)

    plt.savefig(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png'), format='png', dpi=300)  # создание графика

    await message.answer_photo(
        photo=FSInputFile(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png')),
        caption='Статистика появления персонажа в книгах'
    )

    os.remove(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png'))


@router.message(Command('available_characters'))    # вывод доступных персонажей
async def available_characters(message: types.Message):
    characters = database.fetchall(
        '''
            SELECT characters.name, characters.surname FROM characters;
            '''
    )
    characters = [str(character[0]) + ' ' + str(character[1]) for character in characters]

    await message.answer(
        text='Доступные персонажи:\n' + '\n'.join(characters)
    )


async def random_book(message: types.Message):    # вывод случайной книги
    await message.answer_dice()
    book_name = database.fetchone(
        '''
        SELECT books.name FROM books
        JOIN characters_books ON books.id = characters_books.book_id
        GROUP BY books.name
        ORDER BY RANDOM()
        LIMIT 1;
        '''
    )[0]
    await message.answer(
        text=f'Вам выпала книга {book_name}'
    )
    return book_name


async def random_character(message: types.Message):    # вывод случайного персонажа
    await message.answer_dice()
    character_name, character_surname = database.fetchone(
        '''
        SELECT characters.name, characters.surname FROM characters
        ORDER BY RANDOM()
        LIMIT 1;
        '''
    )
    await message.answer(
        text=f'Вам выпал персонаж {character_name + " " + character_surname}'
    )
    return character_name + " " + character_surname
