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
            self.cursor.execute(
                "INSERT INTO 'user' (user_telegram_id, access) VALUES (?, ?)",
                (user_tg_id, access)
            )
            self.connection.commit()

    def add_build(self, user_id, build_name, build_floor_number, build_town_address,
                  build_street_address, build_number_address):
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
        self.connection.commit()

    def show_favourites_user_buildings(self, user_id):
        with self.connection:
            favourites_list = []
            for one_favour_building in self.cursor.execute(f"""SELECT build_name FROM buildings JOIN
             user_buildings JOIN user ON buildings.id = user_buildings.id AND 
             user.user_telegram_id = {user_id} WHERE user_buildings.user_to_building_status = 1 
             AND user_buildings.user_id = user.id"""):
                favourites_list.append(one_favour_building)
            self.connection.commit()
            return [itemik[0] for itemik in favourites_list]

    def update_building_from_user(self, bname, user_id, status):
        self.cursor.execute(f"""UPDATE user_buildings 
                SET user_to_building_status = {status} WHERE
                user_id = (SELECT id FROM user WHERE user_telegram_id = {user_id})
                AND build_id = (SELECT id FROM buildings WHERE build_name = "{bname}") 
                """)

        self.connection.commit()

    def update_all_buildings_from_user(self, user_id, status):
        self.cursor.execute(f"""UPDATE user_buildings 
                SET user_to_building_status = {status} WHERE
                user_id = (SELECT id FROM user WHERE user_telegram_id = {user_id})
                """)

        self.connection.commit()

    def close(self):
        self.connection.close()
