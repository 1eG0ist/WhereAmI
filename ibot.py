from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import imarkups as nav
from isqlighter import SQLighter
from protected_token import TOKEN_copy as T
from functions import SimpleFunctions as SMLF
from functions import StatesFunctions as STFUNC
from PIL import Image
from constants import size_of_photo
import re

# Уровень логгирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота
bot = Bot(token=T)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация соединения с БД
db = SQLighter('probase.db')


@dp.message_handler(Text(equals='!'))
@dp.message_handler(commands=['start', 'subscribe'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Здарова {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, "Это бот для нахождения необходимой аудитории в"
                                                 "учебных заведениях. Для начала работы введите "
                                                 "'/start' после чего вам будет доступен полный "
                                                 "функционал бота: \n1. Добавление зданий в избранное "
                                                 "(как своего так и чужого).\n2. Чтобы найти путь до "
                                                 "нужного кабинета вам сперва нужно зайти во вкладку "
                                                 "избранное, после выбрать здание в котором находится "
                                                 "кабинет, после чего ввести номер нужного кабинета.\n"
                                                 "3. Чтобы добавить здание в избранное вам нужно сперва "
                                                 "зайти во вкладку 'другое', после чего выбрать вкладку "
                                                 "'➕Добавить здание' и зайти во вкладку "
                                                 "'🔍Добавить существующее в боте здание' и отправить "
                                                 "наименование вашего здания.\n 4. Для удаления одного "
                                                 "или всех зданий из избранного вам нужно во вкладке "
                                                 "'другое' войти во вкладку 'параметры' после чего выбрать "
                                                 "то, что вам необходимо\n 5. Пока все, Пока!")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~добавление нового админа~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class AddNewAdmin(StatesGroup):
    wait_tg_id_for_add_in_admins = State()


@dp.message_handler(commands=['add_admin'])
async def adding_new_admin(message: types.message):
    if message.from_user.id != 999734133:
        await message.answer('У вас нет доступа к этой команде')
    else:
        await message.answer("Введите telegram id человека которому вы хотите выдать роль 'admin'")
        await AddNewAdmin.wait_tg_id_for_add_in_admins.set()


async def take_new_admin_tg_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if not db.check_user_on_admin_status(message.text):
            if len(str(message.text)) > 10 or len(str(message.text)) < 8:
                await message.answer("Пользователя с таким id не может существовать")
            else:
                db.add_new_admin(message.text)
                await message.answer("Пользователю с введенным id успешно выдана роль 'admin'")
        else:
            await message.answer("Пользователь с введенным id уже обладает ролью 'admin'")
        await state.finish()
    else:
        await message.answer(f"Вам нужно ввести id -> число")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~Добавление нового человека-фотографа~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class AddNewPhotographer(StatesGroup):
    wait_tg_id_for_add_in_photographers = State()


@dp.message_handler(commands=['add_photographer'])
async def adding_new_photographer(message: types.Message):
    if not db.check_user_on_admin_status(message.from_user.id):
        await message.answer(f"У вас нет доступа к этой команде")
    else:
        await message.answer(f"Введите id пользователя которому вы хотите выдать роль 'photographer'")
        await AddNewPhotographer.wait_tg_id_for_add_in_photographers.set()


async def take_new_photographer_tg_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if not db.check_user_on_photographer_status(int(message.text)):
            if len(str(message.text)) > 10 or len(str(message.text)) < 8:
                await message.answer("Пользователя с таким id не может существовать")
            else:
                db.add_new_photographer(message.text)
                await message.answer(f"Пользователю с указанным id успешно выдана роль 'photographer'")
        else:
            await message.answer(f"Пользователь с указанным id уже обладает ролью 'photographer'")
        await state.finish()
    else:
        await message.answer(f"Вам нужно ввести id -> число")


# ~~~~~~~~~~~~~~~~~~~~~~~~Машина состояний добавления нового здания~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DialogWithUser(StatesGroup):
    waiting_for_building_name = State()
    waiting_for_number_of_floors = State()
    waiting_for_town_address = State()
    waiting_for_street_address = State()
    waiting_for_number_address = State()
    waiting_for_office_numbers = State()
    adding_photos_from_user = State()


@dp.message_handler(Text(equals='🔨📷Добавить здание в бота лично'))
async def start_dialog_with_user(message: types.Message):
    if not db.check_user_on_photographer_status(message.from_user.id):
        await message.answer("К сожалению у вас нет статуса 'admin', "
                             "который необходим для добавления собственных зданий")
    else:
        await message.answer("1. Введите имя вашего здания: \n Если хотите прервать добавление "
                             "нового здания просто напишите сообщение 'Отмена' в чат, или комманду "
                             "'/отмена'.\nЕсли вы ошиблись, то нажав на кнопку 'Назад', вы вернетесь "
                             "на один шаг назад.", reply_markup=nav.AddingBuildMenu)
        await DialogWithUser.waiting_for_building_name.set()


async def start_waiting_for_building_name(message: types.Message, state: FSMContext):
    await state.update_data(building_name=message.text.lower())
    if (message.text.lower(),) in db.show_all_buildings_names():
        await message.answer(f"Здание под названием {message.text} уже добавлено в нашего бота, "
                             f"проверьте, возможно это как раз то здание которое вы ищите "
                             f"если это не так, и названия зданий совпали по случайности, назовите "
                             f"здание по другому")
        await message.answer("Вы перешли на шаг назад, введите другое название здания")
        await DialogWithUser.previous()
        await DialogWithUser.next()
    else:
        await message.answer('2. Введите количество этажей в вашем здании')
        await DialogWithUser.next()


async def start_waiting_for_number_of_floors(message: types.Message, state: FSMContext):
    await state.update_data(number_of_building=message.text.lower())
    await message.answer('3. Введите город в котором находится ваше здание')
    await DialogWithUser.next()


async def start_waiting_for_town_address(message: types.Message, state: FSMContext):
    await state.update_data(building_town_address=message.text.lower())
    await message.answer('4. Введите название улицы на которой находится ваше здание')
    await DialogWithUser.next()


async def start_waiting_for_street_address(message: types.Message, state: FSMContext):
    await state.update_data(building_street_address=message.text.lower())
    await message.answer('5. Введите номер вашего здания на указанной улице')
    await DialogWithUser.next()


async def start_waiting_for_number_address(message: types.Message, state: FSMContext):
    await state.update_data(building_number_address=message.text.lower())
    user_new_building_data = await state.get_data()
    await message.answer(f"Проверьте, что ваше новое здание называется "
                         f"{user_new_building_data['building_name']}, количество этажей которого - "
                         f"{user_new_building_data['number_of_building']} и находится оно в городе "
                         f"{user_new_building_data['building_town_address']} по адресу "
                         f"{user_new_building_data['building_street_address']}, "
                         f"{user_new_building_data['building_number_address']}",
                         reply_markup=nav.AddingPhotosMenu)
    await message.answer(f"Введите номера всех кабинетов через запятую, если номера кабинетов идут подряд, то вы "
                         f"можете указать их так: 557-560.\nОбратите внимание, меньшее число слева-большее справа. "
                         f"Рекомендуем в целом добавлять кабинеты от меньшего к большему")
    SMLF.adding_build(user_new_building_data, int(message.from_user.id))
    await state.update_data(photos=[[1]])
    await DialogWithUser.next()


async def take_numbers_of_building(message: types.Message, state: FSMContext):
    mtext = message.text
    offices_list = []
    try:
        for number in mtext.split(','):
            if number.count('-') > 1:
                await message.answer("К сожалению вы неверно составили сообщение и указали лишнее -, "
                                     "пожалуйста введите перечень кабинетов еще раз")
                await DialogWithUser.previous()
                await DialogWithUser.next()
            elif number.count('-') == 1:
                for i in range(int(number.split('-')[0]), int(number.split('-')[1])+1):
                    offices_list.append(i)
            else:
                offices_list.append(number)
    except Exception:
        await message.answer("Что-то пошло не так, пожалуйста перепроверьте перечень кабинетов еще раз и отправьте "
                             "его заново")
        await DialogWithUser.previous()
        await DialogWithUser.next()

    offices_list = list(map(int, offices_list))
    await state.update_data(offices_list=offices_list)
    await message.answer("Теперь пожалуйста вводите фотографии")
    await DialogWithUser.next()


async def start_adding_photos_from_user(message: types.Message, state: FSMContext):
    if message.content_type not in ['photo', 'sticker']:
        if message.text.lower() == 'следующее':
            a = await state.get_data()
            a['photos'].append([])
            await state.update_data(photos=a['photos'])

        elif message.text == '✔Завершить':
            await message.answer('Ваши данные успешно загружены в базу данных')
            await state.finish()

        else:
            await message.answer('Вам нужно прислать фотографию')
    else:
        await message.photo[-1].download('test.jpg')
        user_photo = Image.open('test.jpg').resize(size_of_photo)
        user_photo.show()
        photo1 = STFUNC.convert_to_binary_data('test.jpg')
        db.add_photo(photo1)

        await bot.send_photo(message.from_user.id, photo1)
        # file_info = await bot.get_file(message.photo[-1].file_id)
        # await message.photo[-1].download(file_info.file_path.split('photos/')[1])

# -------------------------Откат состояния на шаг назад~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


async def cmd_previous(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return
    if await state.get_state() == 'DialogWithUser:waiting_for_building_name':
        await message.answer('Вы не можете вернуться на предыдущий шаг, так как находитесь на первом')
        return
    await message.answer("Вы перешли на шаг назад")
    await DialogWithUser.previous()

# --------------------Функция прерывания работы состояний~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(Text(equals='Отмена'))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Добавление нового здания прекращено", reply_markup=nav.mainMenu)

# ~~~~~~~~~~~~~~~~~~~Добавление существующего в бд здания к пользователю~~~~~~~~~~~~~~~~~~~


class Addexistingbuilding(StatesGroup):
    ex_wait_building_name = State()


@dp.message_handler(Text(equals='🔍Добавить в избранное'))
async def add_another_building(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Введите имя здания которое вы хотите найти',
                           reply_markup=types.ReplyKeyboardRemove())
    await Addexistingbuilding.ex_wait_building_name.set()


async def add_name_of_another_building(message: types.Message, state: FSMContext):
    if (message.text.lower(),) in db.show_all_buildings_names():
        if len(db.check_on_added_buildings_of_user(message.text.lower(), int(message.from_user.id))) == 0:
            db.add_another_building_to_user(message.text.lower(), int(message.from_user.id))
            await message.answer(f"Здание {message.text} успешно добавлено в избранное.",
                                 reply_markup=nav.FollowMenu)
        else:
            await message.answer(f"Здание под название {message.text} уже есть у вас в избранном.",
                                 reply_markup=nav.FollowMenu)
    else:
        await bot.send_message(message.from_user.id, "Похоже, что такого здания в нашего бота еще не "
                                                     "добавляли, проверьте правильно ли вы ввели имя "
                                                     "вашего здания, если да, то предлагаем вам самим "
                                                     "добавить ваше здание.",
                               reply_markup=nav.FollowMenu)
    await state.finish()


# ~~~~~~~~~~~~~~~~~~~~Функция избранного берущая данные из бд~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class WayToOffice(StatesGroup):
    follow_list_wait_for_building_name = State()
    wait_for_office_number = State()


@dp.message_handler(Text(equals='📄Список избранного'))
async def favourites_buildings(message: types.Message):
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    favour_list = db.show_favourites_user_buildings(int(message.from_user.id))
    if len(favour_list) == 0:
        await message.answer("У вас в избранном пока нет ни одного здания")
        return
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=i))
    await message.answer('Ваши здания, если вам не нужно выбирать здание Введите сообщение Отмена',
                         reply_markup=url_keyboard)
    await WayToOffice.follow_list_wait_for_building_name.set()


async def reaction_on_favourites_buildings(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback['data'])
    await state.update_data(bulding=callback['data'])
    await bot.send_message(int(callback.from_user.id), "Введите номер кабинета")
    await WayToOffice.next()


async def take_number_of_building(message: types.Message, state: FSMContext):
    await bot.send_message(int(message.from_user.id), "Тут вот путь тебе в будущем отправят до кабинета")
    await state.update_data(office_number=message.text)
    await state.finish()


# ~~~~~~~~~~~~~~~~~~~~~~~Функция удаления здания из избранного~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DellOneBuild(StatesGroup):
    hold_for_building_name = State()


@dp.message_handler(Text(equals='‼Удалить ОДНО здание'))
async def delete_from_fav_building(message: types.Message):
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    favour_list = db.show_favourites_user_buildings(int(message.from_user.id))
    if len(favour_list) == 0:
        await message.answer("У вас пока нет зданий, которые можно было бы удалить")
        return
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=f"DELONE_{i}"))
    await message.answer('Ваши здания', reply_markup=url_keyboard)
    await DellOneBuild.hold_for_building_name.set()


async def reverse_status_user_with_building(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query['data'].split('_')[1])
    db.delete_building_from_user(callback_query['data'].split('_')[1], int(callback_query.from_user.id))
    await bot.send_message(callback_query.from_user.id, f"Здание {callback_query['data'].split('_')[1]}"
                                                        f" было удалено из списка избранных")
    await callback_query.answer(callback_query['data'].split('_')[1])
    await state.finish()


# ~~~~~~~~~~~~~~~~~~~~~~~~Связь и взаимодействия главного меню~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(content_types=ContentType.ANY)
async def bot_message(message: types.Message):
    if message.text == '⬅Главное меню':
        await bot.send_message(message.from_user.id, '*ГЛАВНОЕ МЕНЮ*', reply_markup=nav.mainMenu)

    elif message.content_type == 'sticker':
        await message.answer('Ты прислал мне стикер')

    elif message.text == '💕Избранное':
        await bot.send_message(message.from_user.id, '*ИЗБРАННОЕ*', reply_markup=nav.FollowMenu)

    elif message.text == 'Другое➱':
        await bot.send_message(message.from_user.id, '*ДРУГОЕ*',
                               reply_markup=nav.otherMenu)

    elif message.text == '➖Удаление из избранного':
        await bot.send_message(message.from_user.id, '*Меню удаления*', reply_markup=nav.SettingsMenu)

    elif message.text == '⛔Удалить ВСЕ здания':
        await bot.send_message(message.from_user.id,
                               'Если вы действительно хотите удалить все здания нажмите на кнопку удаления еще раз',
                               reply_markup=nav.DelAllBuildsMenu)

    elif message.text == '➕Добавить здание':
        await bot.send_message(message.from_user.id,
                               'Имейте ввиде, эта функция доступна только людям, с определенной ролью',
                               reply_markup=nav.AddingChoiceMenu)

    elif message.text == '⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ ИЗ ИЗБРАННОГО БЕЗВОЗВРАТНО':
        db.delete_all_buildings_from_user(int(message.from_user.id))

    else:
        await message.reply('Мне немного не понятно, что именно вы имели ввиду, попробуйте заново')


def register_handler_buildings(dp: Dispatcher):
    dp.register_message_handler(start_dialog_with_user, commands='building', state="*")
    dp.register_message_handler(cmd_cancel, state="*", commands="отмена")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена"), state="*")
    dp.register_message_handler(cmd_previous, Text(equals="назад", ignore_case=True), state="*")
    dp.register_message_handler(start_waiting_for_building_name,
                                state=DialogWithUser.waiting_for_building_name)

    dp.register_message_handler(start_waiting_for_number_of_floors,
                                state=DialogWithUser.waiting_for_number_of_floors)

    dp.register_message_handler(start_waiting_for_town_address,
                                state=DialogWithUser.waiting_for_town_address)

    dp.register_message_handler(start_waiting_for_street_address,
                                state=DialogWithUser.waiting_for_street_address)

    dp.register_message_handler(start_waiting_for_number_address,
                                state=DialogWithUser.waiting_for_number_address)

    dp.register_message_handler(take_numbers_of_building,
                                state=DialogWithUser.waiting_for_office_numbers)

    dp.register_message_handler(start_adding_photos_from_user,
                                content_types=['sticker', 'photo', 'text'],  # нужно обработать ввод текста
                                state=DialogWithUser.adding_photos_from_user)


def register_existing_handler_buildings(dp: Dispatcher):
    dp.register_message_handler(add_another_building, commands='addexisbuilding', state="*")
    dp.register_message_handler(add_name_of_another_building, content_types='text',
                                state=Addexistingbuilding.ex_wait_building_name)


def register_adding_new_admin_func(dp: Dispatcher):
    dp.register_message_handler(adding_new_admin, commands='add_admin', state='*')
    dp.register_message_handler(take_new_admin_tg_id, content_types='text',
                                state=AddNewAdmin.wait_tg_id_for_add_in_admins)


def register_adding_new_photographer_func(dp: Dispatcher):
    dp.register_message_handler(adding_new_photographer, commands='add_photographer', state='*')
    dp.register_message_handler(take_new_photographer_tg_id, content_types='text',
                                state=AddNewPhotographer.wait_tg_id_for_add_in_photographers)


def register_del_building(dp: Dispatcher):
    dp.register_message_handler(delete_from_fav_building, Text(equals='‼Удалить ОДНО здание'), state='*')
    dp.register_callback_query_handler(reverse_status_user_with_building, state=DellOneBuild.hold_for_building_name)


def register_way_to_office(dp: Dispatcher):
    dp.register_message_handler(favourites_buildings, Text(equals="📄Список избранного"), state='*')
    dp.register_callback_query_handler(reaction_on_favourites_buildings,
                                       state=WayToOffice.follow_list_wait_for_building_name)
    dp.register_message_handler(take_number_of_building,
                                state=WayToOffice.wait_for_office_number)


register_way_to_office(dp)
register_handler_buildings(dp)
register_existing_handler_buildings(dp)
register_adding_new_admin_func(dp)
register_adding_new_photographer_func(dp)
register_del_building(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
