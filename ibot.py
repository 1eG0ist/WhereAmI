import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import imarkups as nav
from isqlighter import SQLighter
import sqlite3
TOKEN = '2144915050:AAFasIxNNZHD8MhSJn2pTnpaNP2mSfLQ0W8'

# Уровень логгирования
logging.basicConfig(level=logging.INFO)

# Инициализируем бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Инициализация соединения с БД
db = SQLighter('probase.db')


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    else:
        db.update_user(message.from_user.id, True)

    await message.answer("Вы успешно зарегестрировались")


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Здарова {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⬅Главное меню':
        await bot.send_message(message.from_user.id, '*ГЛАВНОЕ МЕНЮ*', reply_markup=nav.mainMenu)
        
    elif message.text == '💕Избранное':
        await bot.send_message(message.from_user.id, '*ИЗБРАННОЕ*', reply_markup=nav.LikeMenu)
        
    elif message.text == 'Другое➱':
        await bot.send_message(message.from_user.id, '*ДРУГОЕ*',
                               reply_markup=nav.otherMenu)

    elif message.text == '➕Добавить здание':
        await bot.send_message(message.from_user.id,
                               'Введите через запятую: \n*Название здания*,*Сколько в здании этажей*',
                               reply_markup=nav.addMenu)
        
    elif message.text == '⚙️Параметры':
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
        await bot.send_message(message.from_user.id,
            'Введите название здания, которое вы хотите добавить в избранное'
            '(вот тут надо в бд пройтись по столбику с именами зданий и добавить их в другую бд - избранное)')

    else:
        await message.reply('ЭТО ШТО 0_о, не понял... НОрмально общайся!')

        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
