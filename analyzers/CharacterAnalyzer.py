# здесь уже непосредственно работа с pymorphy2 и подсчётом статистики по книгам
import re
import pymorphy2
from aiogram import types

from loader import database


class CharacterAnalyzer:
    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

    async def analyze_character(self, name: str, message: types.Message):
        books = database.fetchall(
            '''
            SELECT id, text FROM books
            '''
        )

        character_id = database.fetchone(
            '''
            SELECT id FROM characters WHERE name = ?;
            ''',
            (name,)
        )[0]

        name = name.lower()

        for book in books:
            counter = 0
            words = book[1].split()  # разбиваем книгу на слова

            for word in words:
                letters_word = re.sub("[^а-яА-Я]", "", word)
                if self.morph.parse(letters_word)[0].normal_form == name:  # приводим к начальной форме и сравниваем с именем перса
                    counter += 1  # считаем количество встретившихся имен

            database.insert(
                '''
                INSERT INTO characters_books (character_id, book_id, count) VALUES (?, ?, ?);
                ''',
                (character_id, book[0], counter)
            )
            await message.answer(f'Character {name} was found {counter} times in book {book[0]}')

    async def analyze_spell(self, name: str, message: types.Message):  # всё то же самое для заклинаний
        books = database.fetchall(
            '''
            SELECT id, text FROM books
            '''
        )

        spell_id = database.fetchone(
            '''
            SELECT id FROM spells WHERE name = ?;
            ''',
            (name,)
        )[0]

        name = name.lower()

        for book in books:
            counter = 0
            words = book[1].split()

            for word in words:
                letters_word = re.sub("[^а-яА-Я]", "", word)
                if self.morph.parse(letters_word)[0].normal_form == name:
                    counter += 1

            database.insert(
                '''
                INSERT INTO spells_books (spell_id, book_id, count) VALUES (?, ?, ?);
                ''',
                (spell_id, book[0], counter)
            )
            await message.answer(f'Spell {name} was found {counter} times in book {book[0]}')
