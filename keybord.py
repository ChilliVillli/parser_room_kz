from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('Фильтр')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.insert(b1)

keyboard_stop = types.InlineKeyboardMarkup()
button_stop = types.InlineKeyboardButton(text="Остановить", callback_data="stop")
keyboard_stop.add(button_stop)