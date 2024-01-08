from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b1 = KeyboardButton('Фильтр')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.insert(b1)

keyboard_590 = KeyboardButton('590')
keyboard_790 = KeyboardButton('790')
keyboard_1000 = KeyboardButton('1000')
keyboard_1250 = KeyboardButton('1250')
keyboard_1500 = KeyboardButton('1500')
keyboard_2000 = KeyboardButton('2000')
keyboard_2500 = KeyboardButton('2500')
keyboard_3000 = KeyboardButton('3000')
keyboard_4000 = KeyboardButton('4000')
keyboard_all = KeyboardButton('2000+')
keyboard_next = KeyboardButton('Без тарифа')
keyboard_tariff = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_tariff.insert(keyboard_590).insert(keyboard_790).insert(keyboard_1000).insert(keyboard_1250).insert(keyboard_1500).insert(keyboard_2000).insert(keyboard_2500).insert(keyboard_3000).insert(keyboard_4000).add(keyboard_all).add(keyboard_next)


keyboard_gold = KeyboardButton('gold')
keyboard_brilliant = KeyboardButton('brilliant')
keyboard_platinum = KeyboardButton('platinum')
keyboard_silver = KeyboardButton('silver')
keyboard_bronze = KeyboardButton('bronze')
keyboard_bronze_vip = KeyboardButton('bronze_vip')
keyboard_next_category = KeyboardButton('Без категории')
keyboard_category = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_category.insert(keyboard_gold).insert(keyboard_brilliant).insert(keyboard_platinum).insert(keyboard_silver).insert(keyboard_bronze).insert(keyboard_bronze_vip).add(keyboard_next_category)


b2 = KeyboardButton('Пропустить')
kb_skip = ReplyKeyboardMarkup(resize_keyboard=True)
kb_skip.insert(b2)

b3 = KeyboardButton('Yes')
b4 = KeyboardButton('No')
kb_reserv = ReplyKeyboardMarkup(resize_keyboard=True)
kb_reserv.insert(b3).insert(b4). add('отмена')

b5 = KeyboardButton('Дальше')
kb_mask = ReplyKeyboardMarkup(resize_keyboard=True)
kb_mask.insert(b5)


b6 = KeyboardButton('отмена')
kb_s = ReplyKeyboardMarkup(resize_keyboard=True)
kb_s.insert(b6)