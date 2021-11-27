import sqlite3 as sq


class SQLighter:

    def __init__(self, database_file):
        """Подключение к БД"""
        self.connection = sq.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_user_id(self, user_telegram_id):
        """Все здания человека"""
        print(user_telegram_id)
        with self.connection:
            return self.cursor.execute(
                "SELECT id FROM 'user' WHERE user_telegram_id = ?",
                (user_telegram_id,),
            ).fetchall()

    def add_user(self, user_tg_id, access=True):
        """Добавление нового пользователя"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'user' (user_telegram_id, access) VALUES (?, ?)",
                (user_tg_id, access)
            )

    def add_build(self, user_id, build_name, build_floor_number, build_town_address, build_street_address,
                  build_number_address):
        """Добавление нового здания"""
        with self.connection:
            idishnik = self.cursor.execute(
                "INSERT INTO 'buildings' (build_name, build_town_address, build_street_address,"
                " build_number_address) VALUES (?, ?, ?, ?)",
                (build_name, build_town_address, build_street_address,
                    build_number_address)
            ).lastrowid
            print(idishnik)
            self.cursor.execute(
                "INSERT INTO 'user_buildings' (user_id, build_id) VALUES (?, ?)",
                (int(user_id[0][0]), int(idishnik))
            )
            self.cursor.execute(
                "INSERT INTO 'floor' (number_of_floor, number_of_building) VALUES(?, ?)",
                (build_floor_number, int(idishnik))
            )

    def close(self):
        self.connection.close()
