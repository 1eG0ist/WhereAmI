from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import imarkups as nav
from isqlighter import SQLighter
import sqlite3


TOKEN = '2144915050:AAFasIxNNZHD8MhSJn2pTnpaNP2mSfLQ0W8'

# Уровень логгирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация соединения с БД
db = SQLighter('probase.db')


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    global user_id
    user_id = int(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           'Здарова {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)


class DialogWithUser(StatesGroup):
    waiting_for_building_name = State()
    waiting_for_number_of_floors = State()
    waiting_for_town_address = State()
    waiting_for_street_address = State()
    waiting_for_number_address = State()


# await message.reply('Вводите по очереди 1.Наименование здания. 2.Количество этажей в нем'
#                        '. 3.Город в котором оно находится  4.Улицу на которой оно находится '
#                        '5. Номер этого здания на улице которую вы указали только что')


@dp.message_handler(Text(equals='➕Добавить здание'))
async def start_dialog_with_user(message: types.Message):
    await message.answer('1. dddd')

    await DialogWithUser.waiting_for_building_name.set()


async def start_waiting_for_building_name(message: types.Message, state: FSMContext):
    await state.update_data(building_name=message.text.lower())
    await message.answer('2. Введите количество этажей в вашем здании')
    await DialogWithUser.next()


async def start_waiting_for_number_of_floors(message: types.Message, state: FSMContext):
    await state.update_data(number_of_building=message.text.lower())
    await DialogWithUser.next()
    await message.answer('3. Введите город в котором находится ваше здание: ')


async def start_waiting_for_town_address(message: types.Message, state: FSMContext):
    await state.update_data(building_town_address=message.text.lower())
    await DialogWithUser.next()
    await message.answer('4. Теперь введите название улицы на которой находится ваше здание: ')


async def start_waiting_for_street_address(message: types.Message, state: FSMContext):
    await state.update_data(building_street_address=message.text.lower())
    await DialogWithUser.next()
    await message.answer('5. Последнее, что нужно это ввести номер вашего здания на указанной улице')


async def start_waiting_for_number_address(message: types.Message, state: FSMContext):
    await state.update_data(building_number_address=message.text.lower())
    user_new_building_data = await state.get_data()
    await message.answer(f"Проверьте, что ваше новое здание называется "
                         f"{user_new_building_data['building_name']}, количество этажей которого - "
                         f"{user_new_building_data['number_of_building']} и находится оно в городе "
                         f"{user_new_building_data['building_town_address']} по адресу "
                         f"{user_new_building_data['building_street_address']}, "
                         f"{user_new_building_data['building_number_address']}")
    adding_build(user_new_building_data)
    await state.finish()


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⬅Главное меню':
        await bot.send_message(message.from_user.id, '*ГЛАВНОЕ МЕНЮ*', reply_markup=nav.mainMenu)
    elif message.text == '💕Избранное':
        await bot.send_message(message.from_user.id, '*ИЗБРАННОЕ*', reply_markup=nav.LikeMenu)

    elif message.text == 'Другое➱':
        await bot.send_message(message.from_user.id, '*ДРУГОЕ*',
                               reply_markup=nav.otherMenu)

    elif message.text == '⚙Параметры':
        await bot.send_message(message.from_user.id, '*Меню параметров*', reply_markup=nav.SettingsMenu)

    elif message.text == '📜Показать все здания':
        await bot.send_message(message.from_user.id, 'Тут надо из SQLite взять все здания')

    elif message.text == '⛔Удалить ВСЕ здания':
        await bot.send_message(message.from_user.id,
                               'Если вы действительно хотите удалить все здания нажмите на кнопку удаления еще раз',
                               reply_markup=nav.DelAllBuildsMenu)

    elif message.text == '⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ БЕЗВОЗВРАТНО':
        await bot.send_message(message.from_user.id, 'тут вот типо удалится вся бд с значениями зданий')

    elif message.text == '‼Удалить ОДНО здание':
        await bot.send_message(message.from_user.id, 'Тут надо сделать кнопки с названиями всех зданий')

    elif message.text == '✚❥Добавить в избранное':
        await bot.send_message(message.from_user.id, 'Грустно')

    else:
        await message.reply('ЭТО ШТО 0_о, не понял... НОрмально общайся!')


def register_handler_builds(dp1: Dispatcher):
    dp1.register_message_handler(start_dialog_with_user, commands='building', state="*")
    dp1.register_message_handler(start_waiting_for_building_name,
                                 state=DialogWithUser.waiting_for_building_name)

    dp1.register_message_handler(start_waiting_for_number_of_floors,
                                 state=DialogWithUser.waiting_for_number_of_floors)

    dp1.register_message_handler(start_waiting_for_town_address,
                                 state=DialogWithUser.waiting_for_town_address)

    dp1.register_message_handler(start_waiting_for_street_address,
                                 state=DialogWithUser.waiting_for_street_address)

    dp1.register_message_handler(start_waiting_for_number_address,
                                 state=DialogWithUser.waiting_for_number_address)


def adding_build(slovarik):
    id_of_user = db.get_user_id(user_id)
    if len(id_of_user) == 0:
        db.add_user(user_id)
        id_of_user = db.get_user_id(user_id)
    db.add_build(id_of_user, slovarik['building_name'], slovarik['number_of_building'],
                 slovarik['building_town_address'],slovarik['building_street_address'],
                 slovarik['building_number_address'])

register_handler_builds(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
