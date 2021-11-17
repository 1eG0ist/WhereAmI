from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
     InlineKeyboardButton, InlineKeyboardMarkup

btnMain = KeyboardButton('⬅Главное меню')


# ~~~main-menu~~~
btnRandom = KeyboardButton('💕Избранное')
btnOther = KeyboardButton('Другое➱')
mainMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnRandom, btnOther)


#~~~LikeMenu~~~
btnAddLike = KeyboardButton('✚❥Добавить в избранное')
LikeMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnAddLike, btnMain)


#~~~AddMenu~~~
btnAdd = KeyboardButton('*Добавление нового здания*')
addMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnAdd, btnMain)


#~~~SettingsMenu~~~
btnPrintAll = KeyboardButton('📜Показать все здания')
btnDelAllBuilds = KeyboardButton('⛔Удалить ВСЕ здания')
btnDelOneBuild = KeyboardButton('‼Удалить ОДНО здание')

SettingsMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(
    btnPrintAll, btnDelAllBuilds, btnDelOneBuild, btnMain)
    #~~~DelAllBuildsMenu~~~
btnDoDellAllBuilds = KeyboardButton('⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ БЕЗВОЗВРАТНО')
DelAllBuildsMenu = ReplyKeyboardMarkup(resize_keyboard = False).add(btnDoDellAllBuilds, btnMain)
    #~~~DelOneBuildMenu~~~
DelOneBuildMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnMain)


#~~~OtherMenu~~~
btnInfo = KeyboardButton('➕Добавить здание')
btnMoney = KeyboardButton('⚙️Параметры')
otherMenu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnInfo, btnMoney, btnMain)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~InlineMenu~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
urlkb = InlineKeyboardMarkup(row_width=2)
