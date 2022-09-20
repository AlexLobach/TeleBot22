from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton

# добавляем разметку наших кнопок
start = types.ReplyKeyboardMarkup(row_width=2)
# создаем кнопки информация
sign_up = types.KeyboardButton('Записаться на занятие')
# и статистика
schedule = types.KeyboardButton('Расписание тренеровок')
# и разработчик
contacts = types.KeyboardButton('Контакты')
# добавляем кнопки в нашу разметку
start.add(sign_up, schedule, contacts)


"""------------------------------------------Добавление inline-кнопок-----------------------------------------------"""

contacts_or_map = InlineKeyboardMarkup(row_width=2)
contacts_or_map.add(InlineKeyboardButton('Написать тренеру', callback_data='trener'))

url_list = 'https://yandex.by/maps/-/CCUV6ZcsTC'
contacts_or_map.add(InlineKeyboardButton('Где находится клуб', callback_data='list', url=url_list))

