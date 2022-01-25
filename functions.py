from isqlighter import SQLighter

db = SQLighter('probase.db')


class StatesFunctions:

    @staticmethod
    def convert_to_binary_data(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobdata = file.read()
        return blobdata


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