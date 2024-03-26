# здесь код для выбора заклинания и поиска статистики по нему
import os
import textwrap

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from matplotlib import pyplot as plt

from keyboards import keyboard
from loader import database
from states.SpellsStatsState import SpellsStatsState

router = Router()


@router.message(Command('choose_spell'))  # выбор
async def choose_spell(message: types.Message, state: FSMContext):
    spells = database.fetchall(
        '''
        SELECT spells.name FROM spells
        JOIN spells_books ON spells.id = spells_books.spell_id
        GROUP BY spells.name
        ORDER BY spells_books.count
        LIMIT 5;
        '''
    )
    spells = [str(spell[0]) for spell in spells]
    await message.answer(
        text='Выберите или напишите имя заклинания',
        reply_markup=keyboard.make_keyboard(
            *spells,
            'cлучайное заклинание'
        )
    )
    await state.set_state(SpellsStatsState.picking_spell)


@router.message(Command('back'))
async def back(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись назад')
    await state.clear()


@router.message(StateFilter(SpellsStatsState.picking_spell))
async def pick_spell(message: types.Message, state: FSMContext):
    spell_name = message.text

    if spell_name == 'cлучайное заклинание':  # бот может рандомом выбирать заклинание из имеющихся
        spell_name = await random_spell(message)

    spell = database.fetchone(
        '''
        SELECT description, photo_url FROM spells
        WHERE name = ?;
        ''',
        (spell_name,)
    )

    if spell is None:  # не разрешаем писать фигню
        await message.answer(
            text='Такого заклинания нет'
        )
        await state.clear()
        return

    await state.update_data(
        spell_name=spell_name,
        spell_description=spell[0],
        spell_photo_url=spell[1]
    )

    await state.set_state(SpellsStatsState.picked_spell)

    await message.answer_photo(
        photo=spell[1],
        caption=spell[0],
        reply_markup=keyboard.make_keyboard('/choose_book')
    )


@router.message(Command('choose_book'), StateFilter(SpellsStatsState.picked_spell))  # выбор книги
async def choosing_book(message: types.Message, state: FSMContext):
    books = database.fetchall(
        '''
        SELECT books.name FROM books
        JOIN spells_books ON books.id = spells_books.book_id
        JOIN spells ON spells_books.spell_id = spells.id
        WHERE spells.name = ?
        ORDER BY spells_books.count;
        ''',
        ((await state.get_data())['spell_name'],)
    )
    books = [str(book[0]) for book in books]
    await message.answer(
        text='Выберите или напишите имя книги',
        reply_markup=keyboard.make_keyboard(
            *books,
            'cлучайная книга',
            'все книги'
        )
    )
    await state.set_state(SpellsStatsState.picking_book)


@router.message(StateFilter(SpellsStatsState.picking_book))
async def picking_book(message: types.Message, state: FSMContext):
    book_name = message.text

    if book_name == 'cлучайная книга':
        await state.update_data(book_names=[await random_book(message)])

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

    await state.set_state(SpellsStatsState.picked_book)


@router.message(Command('get_stats'), StateFilter(SpellsStatsState.picked_book))
async def get_stats(message: types.Message, state: FSMContext):
    context = await state.get_data()
    spell_name = context['spell_name']
    book_names = context['book_names']

    result = []
    for book_name in book_names:
        count = database.fetchone(
            '''
            SELECT spells_books.count FROM spells_books
            JOIN spells ON spells_books.spell_id = spells.id
            JOIN books ON spells_books.book_id = books.id
            WHERE spells.name = ? AND books.name = ?;
            ''',
            (spell_name, book_name)
        )[0]

        result.append((book_name, count))

    labels, values = zip(*result)

    labels = [textwrap.fill(label, 10) for label in labels]

    plt.figure(figsize=(23, 10))

    plt.bar(labels, values)

    plt.savefig(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png'), format='png', dpi=300)  # создание графика

    await message.answer_photo(
        photo=FSInputFile(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png')),
        caption='Статистика появления заклинания в книгах'
    )

    os.remove(os.path.join(os.getcwd(), 'data', 'assets', 'plot.png'))


@router.message(Command('available_spells'))    # вывод всех заклинаний
async def available_spells(message: types.Message):
    spells = database.fetchall(
        '''
        SELECT name FROM spells;
        '''
    )
    spells = [str(spell[0]) for spell in spells]
    await message.answer(
        text='Доступные заклинания: \n' + '\n'.join(spells)
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


async def random_spell(message: types.Message):    # вывод случайного заклинания
    await message.answer_dice()
    spell = database.fetchone(
        '''
        SELECT name FROM spells
        ORDER BY RANDOM()
        LIMIT 1;
        '''
    )[0]
    await message.answer(
        text='Случайное заклинание: ' + spell
    )
    return spell
