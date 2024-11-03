import asyncio
from telebot import async_telebot, types
# from aiogram import Bot, Dispatcher, executor

import aioschedule
from scheduler.asyncio import Scheduler
from decouple import config
import pytz
import datetime

from psql_connect import add_manager, add_employee, add_team, add_place, get_manager, get_managers
from geo import check_location
from sheets_func import check_attendance


bot = async_telebot.AsyncTeleBot(config('API_TOKEN'))


@bot.message_handler(commands=['start'])
async def start(message):
    text = 'Здравствуйте! Чтобы начать работу, введите команду /begin ваше имя и фамилию.\nВведите имя и фамилию через пробел, не добавляя никаких других симоволов. Пример: /begin Дастан Бактыбеков'
    await bot.send_message(message.chat.id, text) 
    # msg = await handle_manager(data)
    # await bot.reply_to(message, msg)


@bot.message_handler(commands=['begin'])
async def begin(message):
    id = message.from_user.id
    data = message.text.split(' ')
    del data[0]
    add_manager(id, data[0], data[1])
    text = 'Отлично! Теперь добавьте свой отдел командой /team Название команды.\nПример: /team Santo Кардио Отдел'
    await bot.send_message(message.chat.id, text) 


@bot.message_handler(commands=['team'])
async def team(message):
    name_of_team = message.text[10:]
    id = message.from_user.id
    add_team(name_of_team, id)
    text = 'Теперь вы можете добавить сотрудников командой /employee телеграм id, имя и фамилия сотрудника\nВводите каждые значение через пробел, не добавляя никаких других символов\nПример: /employee 750257416 Жаныш Кубанычбеков\nP.S. Инструкция, как узнать свой телеграм id описана по этой ссылке: https://blb.uz/kak-uznat-id-telegram.html'
    await bot.send_message(message.chat.id, text) 


@bot.message_handler(commands=['employee'])
async def employee(message):
    id = message.from_user.id
    data = message.text.split(' ')
    del data[0]
    add_employee(id, data[0], data[1], data[2])
    text = 'Сотрудник добавлен! С помощью этой же команды вы можете добавить больше сотрудников'
    await bot.send_message(message.chat.id, text) 


@bot.message_handler(content_types=['location']) 
async def handle_location(message):
    now = datetime.datetime.now(pytz.timezone('Asia/Bishkek')).time()
    if check_location(message.location):
        check_attendance(now, message.location)
    else:
        check_attendance(None, message.location)


@bot.message_handler(commands=['place']) 
async def place(message):
    data = message.text[7:]
    data = data.replace('°', '').split(',')
    title = data[0]
    del data [0]
    coordinates = []
    for item in data:
        coordinates.append(item.strip().split())
    add_place(title, coordinates)
    await bot.send_message(message.chat.id, 'Добавлено')


@bot.message_handler(commands=['connect'])
async def connect(message):
    await bot.send_message(message.chat.id, 'Вы успешно подключены!')


async def send_sheet():
    managers = get_managers()
    for m in managers:
        await bot.send_document(m[0], f'sheets/Отчет -- {m[0]}.xlsx')

# @bot.message_handler(commands=['send_shee'])
async def send_shee():
    managers = get_managers()
    for m in managers:
        sheet = open(f'sheets/Отчет -- {m[0]}.xlsx', 'rb')
        await bot.send_document(m[0], sheet)


# @bot.message_handler(commands=['get_manager'])
# async def manager(message):
#     # print(type(message.from_user.id))
#     print(get_manager(message.from_user.id))
# # async def handle_manager(data):
# #     print(data)
# #     return data


# @bot.message_handler(commands=['bebebe'])
# async def bebebe(message):
#     await bot.send_message(1260539121, 'Здравствуйте, Бактыбеков Дастан!') #1260539121
#     await bot.send_message(1260539121, 'Вы лох!') #1260539121


# async def run_scheduler():
#     aioschedule.every(1).day.at('3:38').do(send_sheet)

#     while True:
#         await aioschedule.run_pending()
#         await asyncio.sleep(1)


async def main():
    schedule = Scheduler(tzinfo=datetime.timezone.utc)
    schedule.daily(datetime.time(hour=8, minute=1, tzinfo=pytz.timezone('Asia/Bishkek')), send_shee)
    schedule.daily(datetime.time(hour=16, minute=31, tzinfo=pytz.timezone('Asia/Bishkek')), send_shee)
    await bot.polling()

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
# asyncio.create_task(run_scheduler)
# executor.start_polling(bot)