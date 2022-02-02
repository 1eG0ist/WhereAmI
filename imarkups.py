from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅Главное меню')
btnCancel = KeyboardButton('Отмена')

# ~~~main-menu~~~
btnRandom = KeyboardButton('💕Избранное')
btnOther = KeyboardButton('Другое➱')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnOther)


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

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMain)

# ~~~ChoiceAddMenu~~~
btnAddNewBuilding = KeyboardButton('🔨📷Добавить здание в бота лично')
AddingChoiceMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAddNewBuilding,
                                                                 btnMain)

# ~~~Adding_build_menu~~~
btnPrevious = KeyboardButton('Назад')
AddingBuildMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel, btnPrevious)


# ~~~Adding_photos_menu~~~
btnFinish = KeyboardButton('✔Завершить')
btnNewBranch = KeyboardButton('Новая ветка')
AddingPhotosMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel, btnFinish, btnNewBranch)

# ~~~ Following_menu ~~~
btnListFollow = KeyboardButton('📄Список избранного')
btnAddExistingBuilding = KeyboardButton('🔍Добавить в избранное')
btnMoney = KeyboardButton('➖Удаление из избранного')
FollowMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnListFollow, btnAddExistingBuilding, btnMoney, btnMain)

# ~~~ Photos_menu ~~~
btnNextPhoto = KeyboardButton('Следующее фото')
PhotosSendMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNextPhoto, btnCancel)
