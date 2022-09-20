import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

# подключение модуля с токеном
import config
# подключение модуля с кнопками
import keyboard

# text_python = 'Python — мультипарадигмальный язык программирования. Полностью поддерживаются объектно-ориентированное,' \
#               ' структурное, обобщённое, функциональное программирование и метапрограммирование. Базовая поддержка ' \
#               'аспектно-ориентированного программирования реализуется за счёт метапрограммирования.'

"""-------------------------------------- настройка бота и логирование -------------------------------------------"""
# хранилище состояний
storage = MemoryStorage()
# инициализация бота
bot = Bot(config.botkey, parse_mode="HTML")
# инициализация диспетчера, при этом указываем ему на хранилище состояний
dp = Dispatcher(bot, storage=storage)
# подключаем логирование
logging.basicConfig(
    # указываем название с логами
    filename='log.txt',
    # указываем уровень логирования
    level=logging.INFO,
    # указываем формат сохранения логов
    format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
           u'[%(asctime)s] %(message)s')

""" -------------------------------------- обработка команды /start ----------------------------------------------"""


@dp.message_handler(commands='start', state=None)
async def welcome(message: types.Message):
    # открываем файл user.txt в режиме чтения
    joined_file = open('user.txt', 'r')
    # создаем множество для хранения имен всех пользователей
    joined_users = set()
    # проходим циклом по каждому пользователю в user.txt
    for line in joined_file:
        # добавляем их в наше множество пользователей
        joined_users.add(line.strip())
    # если пользователь, который нажал /start
    # находится во множестве пользователей
    if not str(message.chat.id) in joined_users:
        # открываем файл user.txt на дозапись
        joined_file = open('user.txt', 'a')
        # записываем в него id нашего пользователя
        joined_file.write(str(message.chat.id) + '\n')
        # добавляем его во множество пользователей
        joined_users.add(message.chat.id)
        # говорим боту отправить сообщение, при этом
    await bot.send_message(
        # обращаемся к id пользователя
        message.chat.id,
        # указываем отправляемое сообщение hello + имя пользователя
        f'Здравствуйте {message.from_user.first_name}\nЕсли хотите записаться на тренировку'
        f'или посмотреть расписание занятий, просто нажмите на нужную кнопку. ',
        # подключаем кнопки из файла keyboard, обратившись к переменной start
        reply_markup=keyboard.start)


""" -------------------------------------- обработка кнопок KeyBoard ----------------------------------------------"""


@dp.message_handler(content_types=['text'])
# задаем функцию-обработчик
async def contacts(message: types.Message):
    # если переданное боту сообщение = 'Информация'
    if message.text == 'Контакты':
        # бот отправляет сообщение пользователю, отправившего его
        # print(message.chat.id)
        await bot.send_message(message.chat.id,
                               # с текстом
                               text='Номер телефона зала: *+375xxxyyoo*\n'
                                    'Хотите посмотреть *карту расположения зал* или может *написать тренеру*?',
                               # режим форматирования
                               parse_mode='Markdown', reply_markup=keyboard.contacts_or_map)
    elif message.text == 'Расписание тренеровок':
        await bot.send_photo(message.chat.id, open('расписание-1.jpg', 'rb'))
        await asyncio.sleep(0.4)
        await bot.send_message(message.chat.id, text="*Ждем вас на тренировках!*", parse_mode="Markdown")


    # elif message.text == "Записаться на занятие":
    #     pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
