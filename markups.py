from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('<- Главное меню')
# ~~~main-menu~~~
btnRandom = KeyboardButton('😀Рандомное число')
btnOther = KeyboardButton('Другое ->')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnRandom, btnOther)


# ~~~Other Menu~~~
btnInfo = KeyboardButton('(<>)Информация')
btnMoney = KeyboardButton('Настройки')
otherMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnInfo, btnMoney, btnMain)
