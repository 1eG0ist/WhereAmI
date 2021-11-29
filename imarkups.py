from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅Главное меню')


# ~~~main-menu~~~
btnRandom = KeyboardButton('💕Избранное')
btnOther = KeyboardButton('Другое➱')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnOther)


# ~~~LikeMenu~~~
btnAddLike = KeyboardButton('✚❥Добавить в избранное')
LikeMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAddLike, btnMain)


# ~~~SettingsMenu~~~
btnDelAllBuilds = KeyboardButton('⛔Удалить ВСЕ здания')
btnDelOneBuild = KeyboardButton('‼Удалить ОДНО здание')

SettingsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(
    btnDelAllBuilds, btnDelOneBuild, btnMain)
# ~~~DelAllBuildsMenu~~~
btnDoDellAllBuilds = KeyboardButton('⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ ИЗ ИЗБРАННОГО БЕЗВОЗВРАТНО')
DelAllBuildsMenu = ReplyKeyboardMarkup(resize_keyboard=False).add(btnDoDellAllBuilds, btnMain)
# ~~~DelOneBuildMenu~~~
DelOneBuildMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnMain)


# ~~~OtherMenu~~~
btnInfo = KeyboardButton('➕Добавить здание')
btnMoney = KeyboardButton('⚙Параметры')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney, btnMain)
