import logging
from random import randint as R
from aiogram import Bot, Dispatcher, executor, types
import markups as nav

TOKEN = '2144915050:AAFasIxNNZHD8MhSJn2pTnpaNP2mSfLQ0W8'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,\
                           'Здарова {0.first_name}'.format(message.from_user),\
                           reply_markup = nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    #await bot.send_message(message.from_user.id, message.text)
    if message.text == '😀Рандомное число':
        await bot.send_message(message.from_user.id, str(R(1, 1000)))
        
    elif message.text == '(<>)Информация':
        await bot.send_message(message.from_user.id,\
                               'У вас пока нет сохраненной информации')
        
    elif message.text == 'Настройки':
        await bot.send_message(message.from_user.id, 'скоро тут будут настройки')
        
    elif message.text == '<- Главное меню':
        await bot.send_message(message.from_user.id, '*<- ГЛАВНОЕ МЕНЮ*', reply_markup = nav.mainMenu)
        
    elif message.text == 'Другое ->':
        await bot.send_message(message.from_user.id, '*ДРУГОЕ*',\
                               reply_markup = nav.otherMenu)

    else:
        bot.send_message(message.from_user.id,\
                         'ЭТО ШТО 0_о, не понял... НОрмально общайся!')

        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
    
