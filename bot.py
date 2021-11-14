import telebot
import config
import random

from telebot import types
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])

def welcome(message):
    sti = open('static/hellosticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рандомное число)")
    item2 = types.KeyboardButton("Добавить новое здание")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданый чтобы быть подопытным кроликом в странном эксперементе. Если вы упростить себе жизнь, то вы по адресу".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def communication_with_bot(message):
    if message.chat.type == 'private':
        if message.text == "Рандомное число)":
            bot.send_message(message.chat.id, str(random.randint(1, 100)))
        elif message.text == "Добавить новое здание":

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Учебное здание', callback_data='study_building')
            item2 = types.InlineKeyboardButton('Рабочее здание', callback_data='work_building')

            markup.add(item1, item2)
                        
            bot.send_message(message.chat.id, 'Давай выберем тип здания', reply_markup=markup)
        elif message.text.lower()[0:2] == "**":
            global type_of_building
            type_of_building = message.text[2:]
            if message.text.lower() == "**университет":
                markup = types.InlineKeyboardMarkup(row_width=8)
                list_of_floors = ['8', '7', '6', '5', '4', '3', '2', '1']
                for i in range(len(list_of_floors)):
                    item_floor = types.InlineKeyboardButton(list_of_floors[i], callback_data=list_of_floors[i])
                    markup.add(item_floor)
                        
                bot.send_message(message.chat.id, f'Давай выберем cколько этажей в твоем {type_of_building}е', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'я залагал')
        else:
            bot.send_message(message.chat.id, 'Даже не знаю, что ответить')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'study_building':
                bot.send_message(call.message.chat.id, 'Введи две звездочки, а после как твое учебное здание называется(университет, колледж и т.д.)')
                
            elif call.data == 'work_building':
                bot.send_message(call.message.chat.id, 'Введи две звездочки, а после как твое рабочее здание называется(завод, офис и т.д.)')
                
            elif call.data in [str(i) for i in range(8)]:
                number_of_floors = int(call.data)
                bot.send_message(call.message.chat.id, f'Хорошо, я запомнил, что количество этажей в твоем {type_of_building}е ровно {str(number_of_floors)}')
                
    except Exception as e:
        print(repr(e))
#RUN
bot.polling(none_stop=True)
