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
    await bot.send_message(message.from_user.id,
                           'Здарова {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)

# ~~~~~~~~~~~~~Машина состояний добавления нового здания~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DialogWithUser(StatesGroup):
    waiting_for_building_name = State()
    waiting_for_number_of_floors = State()
    waiting_for_town_address = State()
    waiting_for_street_address = State()
    waiting_for_number_address = State()


@dp.message_handler(Text(equals='➕Добавить здание'))
async def start_dialog_with_user(message: types.Message):
    # ~~~запоминаем id юзера~~~
    global user_id
    user_id = int(message.from_user.id)

    await message.answer('1. Введите имя вашего здания')
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


# ~~~~~~~~~~~~~~~~~~~~Функция избранного берущая данные из бд~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@dp.message_handler(Text(equals='💕Избранное'))
async def favourites_buildings(message: types.Message):
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    id_user = int(message.from_user.id)
    favour_list = db.show_favourites_user_buildings(id_user)
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=i))
    await message.answer('Ваши здания', reply_markup=url_keyboard)

    @dp.callback_query_handler(lambda c: c.data in favour_list)
    async def reaction_on_favourites_buildings(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id, callback_query['data'])

# ~~~~~~~~~~~~~~~~~~~~~~~Функция удаления здания из избранного~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(Text(equals='‼Удалить ОДНО здание'))
async def delete_from_fav_building(message: types.Message):
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    id_user = int(message.from_user.id)
    favour_list = db.show_favourites_user_buildings(id_user)
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=i))
    await message.answer('Ваши здания', reply_markup=url_keyboard)

    @dp.callback_query_handler(lambda c: c.data in favour_list)
    async def reverse_status_user_with_build(callback_query: types.CallbackQuery):
        db.update_building_from_user(callback_query['data'], id_user, 0)
        await bot.send_message(message.from_user.id, f"Здание {callback_query['data']}"
                                                     f" было удалено из списка избранных")

# ~~~~~~~~~~~~~~~~~~~~~~~Функция удаления всех здания из избранного~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(Text(equals='⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ ИЗ ИЗБРАННОГО БЕЗВОЗВРАТНО'))
async def delete_from_fav_building(message: types.Message):
    db.update_all_buildings_from_user(int(message.from_user.id), 0)

# ~~~~~~~~~~~~~~~~~~~~~~~~Связь и взаимодействия главного меню~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
                 slovarik['building_town_address'], slovarik['building_street_address'],
                 slovarik['building_number_address'])


register_handler_builds(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
