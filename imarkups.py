from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('🏠Главное')
btnCancel = KeyboardButton('Отмена')

# ~~~FavouriteListMenu~~~
FavouriteListMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnCancel)


# ~~~main-menu~~~
btnListFollow = KeyboardButton('💕Избранное')
btnRandom = KeyboardButton('⚙Ред. избранного')
btnOther = KeyboardButton('Спец. меню🎥')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnRandom, btnListFollow, btnOther)


# ~~~SettingsMenu~~~
btnDelAllBuilds = KeyboardButton('⛔Удалить ВСЕ')
btnDelOneBuild = KeyboardButton('‼Удалить ОДНО')

SettingsMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnDelAllBuilds, btnDelOneBuild,
                                                                                      btnMain)
# ~~~DelAllBuildsMenu~~~
btnDoDellAllBuilds = KeyboardButton('⚠❗⛔УДАЛИТЬ ВСЕ ЗДАНИЯ ИЗ ИЗБРАННОГО БЕЗВОЗВРАТНО')
DelAllBuildsMenu = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False).add(btnDoDellAllBuilds, btnMain)
# ~~~DelOneBuildMenu~~~
DelOneBuildMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnMain)

# ~~~OtherMenu~~~
btnInfo = KeyboardButton('➕Добавить здание')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnInfo, btnMain)

# ~~~ChoiceAddMenu~~~
btnAddNewBuilding = KeyboardButton('🔨📷Добавить здание в бота лично')
AddingChoiceMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnAddNewBuilding,
                                                                                          btnMain)

# ~~~Adding_build_menu~~~
btnPrevious = KeyboardButton('Назад')
AddingBuildMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnCancel, btnPrevious)


# ~~~Adding_photos_menu~~~
btnFinish = KeyboardButton('✔Завершить')
btnNewBranch = KeyboardButton('Новая ветка')
AddingPhotosMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnCancel, btnFinish,
                                                                                          btnNewBranch)

# ~~~ Following_menu ~~~

btnAddExistingBuilding = KeyboardButton('🔍Добавить')
btnMoney = KeyboardButton('➖Удалить')
FollowMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnAddExistingBuilding, btnMoney,
                                                                                    btnMain)

# ~~~ Photos_menu ~~~
btnNextPhoto = KeyboardButton('Следующее фото')
PhotosSendMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(btnNextPhoto, btnCancel)

# ~~~ Choice_in_adding~~~
btnIKnow = KeyboardButton('Знаю название💡')
btnDontKnow = KeyboardButton('Показать здания\nв городе🏙')
ChoiceInAddingMenu = ReplyKeyboardMarkup(one_time_keyboard=False).add(btnIKnow, btnDontKnow)

# ~~~ Follow_choice_menu ~~~
btnFollowListKnow = KeyboardButton("Знаю💡")
btnFollowOfficesList = KeyboardButton("Список кабинетов📜")
ChoiceFollowMenu = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True).add(btnFollowListKnow,
                                                                                          btnFollowOfficesList,
                                                                                          btnCancel)
