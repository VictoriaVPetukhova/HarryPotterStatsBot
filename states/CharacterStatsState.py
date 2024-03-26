# состояния для выбора персонажей и книг
from aiogram.fsm.state import StatesGroup, State


class CharacterStatsState(StatesGroup):
    picking_character = State()
    picked_character = State()
    picking_book = State()
    picked_book = State()