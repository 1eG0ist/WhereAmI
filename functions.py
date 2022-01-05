"""from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import imarkups as nav"""
from isqlighter import SQLighter

db = SQLighter('probase.db')


class StatesFunctions:

    pass


class SimpleFunctions:

    # ~~~Проверка на корректность -> передача в базу данных~~~

    @staticmethod
    def adding_build(slovarik: dict, user_id: int):
        id_of_user = db.get_user_id(user_id)
        if len(id_of_user) == 0:
            db.add_user(user_id)
            id_of_user = db.get_user_id(user_id)
        db.add_new_build(id_of_user, slovarik['building_name'], slovarik['number_of_building'],
                         slovarik['building_town_address'], slovarik['building_street_address'],
                         slovarik['building_number_address'])
