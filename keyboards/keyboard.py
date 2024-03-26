# здесь кнопки для бота
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def make_keyboard(*args):
    buttons = [[KeyboardButton(text=str(arg))] for arg in args]
    reply_markup = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return reply_markup
