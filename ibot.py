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

# Уровень logging'а
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
                           "Приветствую вас, {0.first_name}, я бот для нахождения кабинетов в зданиях. Ниже "
                           "представлена инструкция по использованию "
                           .format(message.from_user),
                           reply_markup=nav.mainMenu)
    await bot.send_message(message.from_user.id, "ЦЕЛЬ: Бот существует для того, чтобы помочь вам находить кабинеты "
                                                 "в зданиях")

    await bot.send_message(message.from_user.id, "Пояснение, что значат названия кнопок в различных меню(меню-набор "
                                                 "кнопок внизу экрана)\n1. 💕Избранное - Список вашего избранного\n2. "
                                                 "⚙Ред. избранного - здесь вы можете добавлять здания "
                                                 "в список избранного, а так же удалять здания из него\n3. 🏠Главное - "
                                                 "Кнопка возвращающая вас в основное меню\n4. Спец. меню🎥 - кнопка "
                                                 "только для людей, которые сами хотят добавить здание(вводить в бота "
                                                 "фотографии)")

    await bot.send_message(message.from_user.id, "Для того, чтобы начать использовать бота в нужном для вас здании, "
                                                 "вам нужно сперва добавить его в избранное. Как это сделать?:\n"
                                                 "1. Вам нужно нажать на кнопку снизу экрана под названием "
                                                 "'⚙Ред. избранного'\n2. Нажмите на кнопку '🔍Добавить'\n"
                                                 "3. Если вы знаете название вашего здания и нажмете 'Знаю название💡', "
                                                 "то\n3.1Введите название здания которое вы хотите добавить"
                                                 "(сначала попробуйте ввести аббревиатуру, если здание не нашлось, "
                                                 "введите название вашего здания полностью)\n Обратите внимание, "
                                                 "здания будут загружаться в бота постепенно и возможно на данном этапе"
                                                 " здания в нем еще нет."
                                                 "\nЕсли это не сработало, то\n3.2 Нажмите на кнопку "
                                                 "'Показать здания в городе🏙' в этом же меню. После введите ваш город, "
                                                 "а далее выберите из списка всех зданий в этом городе ваше здание, "
                                                 "если оно есть, если нет, то нажмите на кнопку 'Отмена❌'")

    await bot.send_message(message.from_user.id, f"Данный бот, рассчитан на то, что люди будут сами постепенно "
                                                 f"добавлять свои здания в бота и тем самым будут помогать остальным. "
                                                 f"Если вашего здания нет в боте и вы хотите лично добавить его, "
                                                 "то пожалуйста напишите сюда - { https://t.me/sjwevalz }, Сразу "
                                                 "указывайте город и название здания, после этого вам будет выдана "
                                                 "соответствующая роль.")

    await bot.send_message(message.from_user.id, "Приятного использования!")

    if len(db.get_user_id(message.from_user.id)) == 0:
        db.add_user(message.from_user.id)


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, "Это бот для нахождения необходимой аудитории в"
                                                 "учебных заведениях. Для начала работы введите "
                                                 "'/start' после чего вам будет доступен полный "
                                                 "функционал бота: \nДобавление зданий в избранное "
                                                 "(как своего так и чужого).\nЧтобы пользоваться каким-либо зданием"
                                                 "его сперва нужно добавить в список избранного во вкладке избранное")

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
                await bot.send_message(message.text, "Вам выдана роль 'admin'")
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
                await bot.send_message(message.text, "Вам выдана роль 'photographer'")
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
    wait_for_entrance_photo = State()
    adding_photos_from_user = State()
    wait_new_last_number = State()


@dp.message_handler(Text(equals='🔨📷Добавить здание в бота лично'))
async def start_dialog_with_user(message: types.Message):
    if not db.check_user_on_photographer_status(message.from_user.id):
        await message.answer("К сожалению у вас нет статуса 'photographer',  "
                             "который необходим для добавления собственных зданий, если вы действительно хотите "
                             "добавить здание, то обратитесь к человеку в телеграмме <ссылка>, указав наименование и "
                             "город учреждения план которого вы хотите добавить")
    else:
        await message.answer("Если хотите прервать добавление "
                             "нового здания - нажмите кнопку 'Отмена', или введите команду "
                             "'/отмена'.\nЕсли вы ошиблись, то нажав на кнопку 'Назад', вы вернетесь "
                             "на один шаг назад(работает только при указании информации о здании)")

        await message.answer("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        await message.answer("1. Введите имя вашего здания:", reply_markup=nav.AddingBuildMenu)
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
                         f"можете указать их так: 557-560 или 345-360,401-420.\nОбратите внимание, меньшее число "
                         f"слева-большее справа. Рекомендуем в целом добавлять кабинеты от меньшего к большему. Так "
                         f"же вам нужно указать все буквенные названия кабинетов(буква в букву как вы укажите в "
                         f"подписи под фотографией), чтобы пользователи "
                         f"могли воспользоваться этим списком")
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
                if number.isdigit():
                    offices_list.append(number)
                else:
                    offices_list.append(number.lower().strip())

        user_new_building_data = await state.get_data()
        building_id = db.take_building_id(user_new_building_data["building_name"])
        building_id = list(building_id)[0][0]
        db.add_all_offices_of_building(offices_list, building_id)

        await state.update_data(offices_list=offices_list)

        await message.answer("Теперь пожалуйста введите фотографию входа в ваше здание(внутри, спиной к входной "
                             "двери) и подпишите как <ВХОД>, когда вы добавите все кабинеты введите /stop или нажмите "
                             "кнопку '✔Завершить'")
        await DialogWithUser.next()

    except Exception:
        await message.answer("Что-то пошло не так, пожалуйста перепроверьте перечень кабинетов еще раз и отправьте "
                             "его заново")


async def adding_entrance_of_building(message: types.Message, state: FSMContext):
    try:
        # Скачиваем фотографию в детализации 1, где 0-мыло, 1-норм, 2-хорошо, 3-изначальное разрешение
        await message.photo[1].download('photo_beta.jpg')
        # Скачиваем уже сжатое до значения 1 фото под именем photo.jpg
        Image.open('photo_beta.jpg').save('photo.jpg')

        # Переводим сжатое изображение в бинарный формат
        photo1 = STFUNC.convert_to_binary_data('photo.jpg')

        # Добавляем значения и фотографию в бинарном виде в бд
        building_data = await state.get_data()

        graph_id = db.add_photo_in_graph(photo1, building_data['building_name'], message.caption, -1)
        await state.update_data(last_number=graph_id)

        await state.update_data(redefinition_numbers={1: graph_id})

        await state.update_data()
        await message.answer(f"Хорошо, теперь основание вашего ветвления имеет номер 1, когда захотите "
                             f"пустить ветвь фотографий начиная от этой фотографии, вам нужно будет указать этот номер")

        await message.answer(f"Теперь вам нужно подписывать каждую фотографию, например - "
                             f"<пройдите вперед по коридору до упора> или <войдите через дверь>")

        await message.answer(f"По умолчанию ваша следующая фотография будет привязываться к предшествующей, если вам "
                             f"нужно сделать новую ветку - нажмите кнопку <новая ветка> и введите номер фотографии, с "
                             f"которой будет начинаться новая ветка")

        await message.answer(f"ВАЖНО: когда ветвь заканчивается и на фото кабинет, к которому ведет путь в подписи "
                             f"к нему должен быть только его номер")

        await message.answer(f"Пожалуйста, для полного понимая процесса прочтите все сообщения")

        await message.answer(f"Вводите фотографии: ")
        await DialogWithUser.next()

    except Exception:
        await message.answer("Что-то пошло не так, пожалуйста повторите попытку")


async def start_adding_photos_from_user(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        if message.text == "Новая ветка":
            await message.answer("Пожалуйста введите номер фотографии, к которой будет привязана следующая фотография")
            await DialogWithUser.next()
    else:
        try:
            # Скачиваем фотографию в детализации 1, где 0-мыло, 1-норм, 2-хорошо, 3-изначальное разрешение
            await message.photo[1].download('photo_beta.jpg')

            # Скачиваем уже сжатое до значения 1 фото под именем photo.jpg
            Image.open('photo_beta.jpg').save('photo.jpg')

            # Переводим сжатое изображение в бинарный формат
            photo1 = STFUNC.convert_to_binary_data('photo.jpg')

            building_data = await state.get_data()

            graph_id = db.add_photo_in_graph(photo1, building_data['building_name'],
                                             message.caption.lower(), building_data['last_number'])

            data = await state.get_data()
            updated_dict = data["redefinition_numbers"]
            max_dict = max(set(map(int, data['redefinition_numbers'].keys())))
            updated_dict[max_dict+1] = graph_id
            await state.update_data(redefinition_numbers=updated_dict)
            await state.update_data(last_number=graph_id)
            await message.answer(f"номер этой фотографии - {max_dict+1}")

        except Exception:
            await message.answer("Что-то пошло не так, пожалуйста отправьте фотографию заново, возможно вы указали "
                                 "номер фотографии которого не существует, так что убедитесь, "
                                 "что бот отправлял в ответ на ваше фото номер, которой вы указали")


async def start_waiting_for_last_number(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        data = data["redefinition_numbers"]
        print("data: ", data)
        await state.update_data(last_number=data[int(message.text)])
        await message.answer("Теперь следующая фотография будет привязана к этому номеру")
        await message.answer("Введите фотографию: ")
        await DialogWithUser.previous()
    except ValueError:
        await message.answer("Что-то пошло не так, повторите попытку")


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


@dp.message_handler(commands=['stop'])
@dp.message_handler(Text(equals='Отмена'))
@dp.message_handler(Text(equals='✔Завершить'))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Процесс завершен", reply_markup=nav.mainMenu)

# ~~~~~~~~~~~~~~~~~~~Добавление существующего в бд здания к пользователю ~~~~~~~~~~~~~~~~~~~


class Addexistingbuilding(StatesGroup):
    ex_wait_building_name = State()


@dp.message_handler(Text(equals='Знаю название💡'))
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~Функция для поиска здания по городу~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SearchInCity(StatesGroup):
    wait_for_name_of_the_city = State()
    wait_for_building_name = State()


@dp.message_handler(Text(equals='Показать здания\nв городе🏙'))
async def start_waiting_city_s_name(message: types.Message):
    url_keyboard_cities = InlineKeyboardMarkup(row_width=2)
    cities = db.search_all_cities()
    for i in cities:
        url_keyboard_cities.add(InlineKeyboardButton(i[0], callback_data=i[0]))
    url_keyboard_cities.add(InlineKeyboardButton("Отмена❌", callback_data="Отмена❌"))
    await message.answer("Выберите город: ",
                         reply_markup=url_keyboard_cities)
    await message.answer("Если вашего города нет-нажмите 'Отмена❌'")
    await SearchInCity.wait_for_name_of_the_city.set()


async def take_city_and_show_buildings(callback: types.CallbackQuery, state: FSMContext):
    if callback['data'] == 'Отмена❌':
        await bot.send_message(callback.from_user.id, "Выбор города прекращен, сожалеем, что в вашем городе, еще нет "
                                                      "добавленных зданий", reply_markup=nav.mainMenu)
        await state.finish()
    else:
        mes = callback['data']
        buildings = db.search_for_buildings_in_city(mes)
        await bot.send_message(callback.from_user.id, "Для отмены процесса вы можете нажать кнопку 'Отмена❌'",
                               reply_markup=nav.FavouriteListMenu)
        url_keyboard_buildings = InlineKeyboardMarkup(row_width=2)
        for building in buildings:
            i = building[0]
            url_keyboard_buildings.add(InlineKeyboardButton(i, callback_data=i))
        url_keyboard_buildings.add(InlineKeyboardButton("Отмена❌", callback_data="Отмена❌"))
        await bot.send_message(callback.from_user.id, 'Все здания в вашем городе',
                               reply_markup=url_keyboard_buildings)
        await SearchInCity.next()


async def add_building_or_not(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback['data'])
    name = callback['data']
    if name == "Отмена❌":
        await bot.send_message(callback.from_user.id, "Сожалеем, что вашего здания все еще нет в боте. Бот постоянно "
                                                      "обновляется, для того чтобы такого впредь не происходило",
                               reply_markup=nav.mainMenu)
        await state.finish()

    else:
        try:
            if len(db.check_on_added_buildings_of_user(name, int(callback.from_user.id))) == 0:
                db.add_another_building_to_user(name, callback.from_user.id)
                await bot.send_message(callback.from_user.id, f"Здание {name} успешно добавлено к вам в избранное",
                                       reply_markup=nav.mainMenu)
                await state.finish()
            else:
                await bot.send_message(callback.from_user.id, f"Здание под название {name} уже есть у вас в избранном.",
                                       reply_markup=nav.mainMenu)
        except Exception:
            await bot.send_message(callback.from_user.id, "Что-то пошло не так, вы возвращены в главное меню",
                                   reply_markup=nav.mainMenu)

    await state.finish()

# ~~~~~~~~~~~~~~~~~~~~Функция избранного берущая данные из бд~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class WayToOffice(StatesGroup):
    follow_list_wait_for_building_name = State()
    wait_for_office_number = State()
    send_photo = State()


@dp.message_handler(Text(equals='💕Избранное'))
async def favourites_buildings(message: types.Message):
    await message.answer("Для отмены процесса нажмите кнопку 'Отмена'", reply_markup=nav.FavouriteListMenu)
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    favour_list = db.show_favourites_user_buildings(int(message.from_user.id))
    if len(favour_list) == 0:
        await message.answer("У вас в избранном пока нет ни одного здания")
        return
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=i))
    await message.answer('Ваши здания',
                         reply_markup=url_keyboard)
    await WayToOffice.follow_list_wait_for_building_name.set()


async def reaction_on_favourites_buildings(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback['data'])
    await state.update_data(building=callback['data'])
    await bot.send_message(int(callback.from_user.id), "Введите номер или название кабинета, если не знаете как "
                                                       "называется или какой номер имеет ваш кабинет, то выйдите в "
                                                       "главное меню и введите команду '/showoffices'")
    await state.update_data(send_number=1)
    await WayToOffice.next()


async def take_number_of_building(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        graph_id = db.search_for_needed_id(data['building'], message.text)
        await state.update_data(offices_list=db.search_for_needed_office(graph_id, [])[::-1])
        await message.answer("Для того, чтобы получить следующее фото, нажмите на кнопку 'Следующее фото', для отмены "
                             "процесса нажмите кнопку 'Отмена'", reply_markup=nav.PhotosSendMenu)
        data = await state.get_data()
        await bot.send_photo(int(message.from_user.id), data['offices_list'][0][0], data['offices_list'][0][1])
        await WayToOffice.next()

    except Exception:
        await message.answer(f"Похоже такого кабинета в здании нет, поиск прекращен", reply_markup=nav.mainMenu)
        await state.finish()


async def send_photo_to_user(message: types.Message, state: FSMContext):
    try:
        if message.text == "Следующее фото":
            data = await state.get_data()
            await bot.send_photo(int(message.from_user.id),
                                   data['offices_list'][data['send_number']][0],
                                   data['offices_list'][data['send_number']][1])

            if data['send_number'] == len(data['offices_list'])-1:
                await message.answer("Вы у цели", reply_markup=nav.mainMenu)
                await state.finish()
            else:
                await state.update_data(send_number=int(data['send_number'])+1)

        else:
            await message.answer("Сообщение не распознано\nДля того, чтобы получить следующее фото, нажмите на кнопку "
                                 "'Следующее фото', для отмены процесса нажмите кнопку 'Отмена'\nПожалуйста повторите")
    except Exception:
        await message.answer("Похоже что-то пошло не так, отправка пути прекращена", reply_markup=nav.mainMenu)


# ~~~~~~~~~~~~~~~~~~~~~~~Функция удаления здания из избранного~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class DellOneBuild(StatesGroup):
    hold_for_building_name = State()


@dp.message_handler(Text(equals='‼Удалить ОДНО'))
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
    db.delete_building_from_user(callback_query['data'].split('_')[1], int(callback_query.from_user.id))
    await bot.send_message(callback_query.from_user.id, f"Здание {callback_query['data'].split('_')[1]}"
                                                        f" было удалено из списка избранных")
    await callback_query.answer(callback_query['data'].split('_')[1])
    await state.finish()


# ~~~~~~~~~~~~~Представление пользователю всех кабинетов выбранного здания~~~~~~~~~~~~~~~~~~

class ShowAllOffices(StatesGroup):
    wait_for_building_name_for_show_offices = State()


@dp.message_handler(commands=['showoffices'])
async def show_buildings_choice(message: types.Message):
    await message.answer("Для отмены процесса нажмите кнопку 'Отмена'", reply_markup=nav.FavouriteListMenu)
    url_keyboard = InlineKeyboardMarkup(row_width=2)
    favour_list = db.show_favourites_user_buildings(int(message.from_user.id))
    if len(favour_list) == 0:
        await message.answer("Прежде чем посмотреть список кабинетов здания, вам нужно добавить это здание в избранное")
        return
    for i in favour_list:
        url_keyboard.add(InlineKeyboardButton(i, callback_data=i))
    await message.answer('Выберите здание,\nкабинеты которого вы хотите увидеть: ',
                         reply_markup=url_keyboard)
    await ShowAllOffices.wait_for_building_name_for_show_offices.set()


async def show_all_offices_in_building(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(callback['data'])
    building_id = list(db.take_building_id(callback['data']))[0][0]
    offices_str = ""
    offices_list = sorted(list(map(lambda x: str(x[0]), list(db.take_all_offices_of_building(building_id)))))
    for i in range(len(offices_list)-1):
        offices_str += offices_list[i]+','

    offices_str += offices_list[len(offices_list)-1]

    await bot.send_message(callback.from_user.id, f"Кабинеты в здании {callback['data']}: \n{offices_str}",
                           reply_markup=nav.mainMenu)
    await state.finish()


# ~~~~~~~~~~~~~~~~~~~~~~~~Связь и взаимодействия главного меню~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@dp.message_handler(content_types=ContentType.ANY)
async def bot_message(message: types.Message):
    if message.text == '🏠Главное':
        await bot.send_message(message.from_user.id, 'вы в главном меню', reply_markup=nav.mainMenu)

    elif message.content_type == 'sticker':
        await message.answer('Ты прислал мне стикер')

    elif message.text == '⚙Ред. избранного':
        await bot.send_message(message.from_user.id, 'вы в меню редактирования избранного', reply_markup=nav.FollowMenu)

    elif message.text == 'Спец. меню🎥':
        await bot.send_message(message.from_user.id, 'вы в меню для контентмейкеров',
                               reply_markup=nav.otherMenu)

    elif message.text == '➖Удалить':
        await bot.send_message(message.from_user.id, 'вы в меню удаления', reply_markup=nav.SettingsMenu)

    elif message.text == '⛔Удалить ВСЕ':
        await bot.send_message(message.from_user.id,
                               'Если вы действительно хотите удалить все здания нажмите на кнопку удаления еще раз',
                               reply_markup=nav.DelAllBuildsMenu)

    elif message.text == '➕Добавить здание':
        await bot.send_message(message.from_user.id,
                               'Имейте ввиду, эта функция доступна только людям, с определенной ролью',
                               reply_markup=nav.AddingChoiceMenu)

    elif message.text == '⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ ИЗ ИЗБРАННОГО БЕЗВОЗВРАТНО':
        db.delete_all_buildings_from_user(int(message.from_user.id))
        await message.answer("Здания успешно удалены")

    elif message.text == '🔍Добавить':
        await bot.send_message(message.from_user.id, "Вы в меню выбора, если вы знаете название здания в боте - "
                                                     "нажмите кнопку 'Знаю название', иначе, нажмите 'Показать здания "
                                                     "в городе🏙'",
                               reply_markup=nav.ChoiceInAddingMenu
                               )

    else:
        await message.reply('Мне немного не понятно, что именно вы имели ввиду, попробуйте заново')


def register_handler_buildings(dp: Dispatcher):
    dp.register_message_handler(start_dialog_with_user, commands='building', state="*")
    dp.register_message_handler(cmd_cancel, state="*", commands="stop")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена"), state="*")
    dp.register_message_handler(cmd_cancel, Text(equals='✔Завершить'), state='*')
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

    dp.register_message_handler(adding_entrance_of_building, content_types=['sticker', 'photo', 'text'],
                                state=DialogWithUser.wait_for_entrance_photo)

    dp.register_message_handler(start_adding_photos_from_user,
                                content_types=['sticker', 'photo', 'text'],  # нужно обработать ввод текста
                                state=DialogWithUser.adding_photos_from_user)

    dp.register_message_handler(start_waiting_for_last_number, state=DialogWithUser.wait_new_last_number)


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
    dp.register_message_handler(favourites_buildings, Text(equals="💕Избранное"), state='*')
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена"), state="*")
    dp.register_callback_query_handler(reaction_on_favourites_buildings,
                                       state=WayToOffice.follow_list_wait_for_building_name)
    dp.register_message_handler(take_number_of_building,
                                state=WayToOffice.wait_for_office_number)
    dp.register_message_handler(send_photo_to_user, state=WayToOffice.send_photo)


def register_choice_add_fn(dp: Dispatcher):
    dp.register_message_handler(start_waiting_city_s_name, Text(equals="'Показать здания\nв городе🏙'"), state='*')
    dp.register_callback_query_handler(take_city_and_show_buildings, state=SearchInCity.wait_for_name_of_the_city)
    dp.register_callback_query_handler(add_building_or_not, state=SearchInCity.wait_for_building_name)


def register_showing_offices_fn(dp: Dispatcher):
    dp.register_message_handler(show_buildings_choice, commands=['showoffices'], state='*')
    dp.register_callback_query_handler(show_all_offices_in_building,
                                       state=ShowAllOffices.wait_for_building_name_for_show_offices)


register_way_to_office(dp)
register_handler_buildings(dp)
register_existing_handler_buildings(dp)
register_adding_new_admin_func(dp)
register_adding_new_photographer_func(dp)
register_del_building(dp)
register_choice_add_fn(dp)
register_showing_offices_fn(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
