# состояния для функций админа (это добавление персонажей и заклинаний)
from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    adding_admin = State()

    adding_character_name = State()
    added_character_name = State()
    adding_character_surname = State()
    added_character_surname = State()
    adding_character_description = State()
    added_character_description = State()

    adding_spell_name = State()
    added_spell_name = State()
    adding_spell_description = State()
    added_spell_description = State()
