# состояния для выбора заклинаний и книг
from aiogram.fsm.state import StatesGroup, State


class SpellsStatsState(StatesGroup):
    picking_spell = State()
    picked_spell = State()
    picking_book = State()
    picked_book = State()