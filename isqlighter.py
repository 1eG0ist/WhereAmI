import sqlite3 as sq


class SQLighter:

    def __init__(self, database_file):
        """Подключение к БД"""
        self.connection = sq.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_user_id(self, user_telegram_id):
        """Все здания человека"""
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

    def add_new_build(self, user_id, build_name, build_floor_number, build_town_address,
                      build_street_address, build_number_address):
        """Добавление нового здания"""
        with self.connection:
            idishnik = self.cursor.execute(
                "INSERT INTO 'buildings' (build_name, build_town_address, build_street_address,"
                " build_number_address) VALUES (?, ?, ?, ?)",
                (build_name, build_town_address, build_street_address,
                    build_number_address)
            ).lastrowid
            self.cursor.execute(
                "INSERT INTO 'user_buildings' (user_id, build_id) VALUES (?, ?)",
                (int(user_id[0][0]), int(idishnik))
            )
            self.cursor.execute(
                "INSERT INTO 'floor' (number_of_floor, number_of_building) VALUES(?, ?)",
                (build_floor_number, int(idishnik))
            )
        self.connection.commit()

    def show_all_buildings_names(self):
        a = self.cursor.execute("SELECT build_name FROM buildings")
        return set(a)

    def show_favourites_user_buildings(self, user_id):
        with self.connection:
            favourites_list = []
            for one_favour_building in self.cursor.execute(f"""SELECT build_name FROM buildings JOIN
             user_buildings JOIN user ON buildings.id = user_buildings.build_id AND 
             user.user_telegram_id = {user_id} AND user_buildings.user_id = user.id"""):
                favourites_list.append(one_favour_building)

        self.connection.commit()
        return [itemik[0] for itemik in favourites_list]

    def delete_building_from_user(self, bname, user_id):
        with self.connection:
            self.cursor.execute(f"""DELETE FROM user_buildings 
                    WHERE user_id = (SELECT id FROM user WHERE user_telegram_id = {user_id})
                    AND build_id = (SELECT id FROM buildings WHERE build_name = "{bname}") 
                    """)

        self.connection.commit()

    def delete_all_buildings_from_user(self, user_id):
        with self.connection:
            self.cursor.execute(f"""DELETE from user_buildings where
                    user_id = (SELECT id FROM user WHERE user_telegram_id = "{user_id}")
                    """)

        self.connection.commit()

    # ~~~~~~~обращение к бд для добавления в избранное юзера уже существующих зданий~~~~~~~

    def check_on_added_buildings_of_user(self, name, user_tg_id):
        names_of_b = self.cursor.execute(f"""SELECT build_name FROM buildings JOIN
                     user_buildings JOIN user ON buildings.id = user_buildings.build_id WHERE
                     buildings.build_name = '{name}' AND user_buildings.user_id = user.id AND
                     user.user_telegram_id = {user_tg_id}
                     """)
        return list(names_of_b)

    def add_another_building_to_user(self, name, user_tg_id):
        with self.connection:
            self.cursor.execute("""INSERT INTO 'user_buildings' 
            (user_id, build_id) VALUES (?, ?)""",
                    (list(self.cursor.execute(f'SELECT id FROM user WHERE '
                                              f'user_telegram_id = {user_tg_id}'))[0][0],
                        list(self.cursor.execute(f'SELECT id FROM buildings '
                                                 f'WHERE build_name = "{name}"'))[0][0]))

        self.connection.commit()

    def check_user_on_admin_status(self, user_tg_id: int) -> bool:
        if (int(user_tg_id),) in list(self.cursor.execute(f"SELECT tg_id_is_admin FROM admins")):
            return True
        else:
            return False

    def check_user_on_photographer_status(self, user_tg_id: int) -> bool:
        if (int(user_tg_id),) in list(self.cursor.execute(f"SELECT tg_id_is_photographer FROM photographers")):
            return True
        else:
            return False

    def add_new_admin(self, tg_id):
        with self.connection:
            self.cursor.execute(f"INSERT INTO 'admins' (tg_id_is_admin) VALUES (?)", (tg_id, ))

        self.connection.commit()

    def add_new_photographer(self, tg_id):
        with self.connection:
            self.cursor.execute(f"INSERT INTO 'photographers' (tg_id_is_photographer) VALUES (?)",
                                (tg_id, ))

        self.connection.commit()

    def add_photo_in_graph(self, photo, name, text, parent):
        b_id = list(self.cursor.execute(f"SELECT id FROM buildings WHERE buildings.build_name = '{name}'"))
        graph_id = max(set(self.cursor.execute(f"SELECT id FROM graph")))[0]+1
        with self.connection:
            self.cursor.execute(f"INSERT INTO 'graph' (id, building_id, photo, description, parent_id) "
                                f"VALUES (?, ?, ?, ?, ?)", (
                graph_id, b_id[0][0], photo, text, parent
            ))

        self.connection.commit()
        return graph_id

    def search_for_needed_id(self, name: str, office_number: str) -> int:
        parent = list(self.cursor.execute(f"SELECT id FROM graph WHERE building_id = (SELECT id FROM buildings WHERE "
                                          f"build_name = '{name}') AND description = '{str(office_number)}'"))
        return parent[0][0]

    def search_for_needed_office(self, graph_id: int, offices_list: list) -> list:
        parent = list(self.cursor.execute(f"SELECT parent_id FROM graph WHERE id = {graph_id}"))[0][0]
        photo = list(self.cursor.execute(f"SELECT photo FROM graph WHERE id = {graph_id}"))[0][0]
        description = list(self.cursor.execute(f"SELECT description FROM graph where id = {graph_id}"))[0][0]
        offices_list.append([photo, description])
        if parent == -1 or parent == '-1':
            return offices_list
        else:
            return SQLighter.search_for_needed_office(self, parent, offices_list)

    def search_for_buildings_in_city(self, city: str) -> list:
        buildings = list(self.cursor.execute(f"SELECT build_name FROM buildings WHERE buildings.build_town_address = "
                                             f"'{city}'"))
        return buildings

    def search_all_cities(self):
        cities = list(set(self.cursor.execute("SELECT build_town_address FROM buildings")))
        return cities

    def take_building_id(self, name):
        building_id = self.cursor.execute(f"SELECT id FROM buildings WHERE buildings.build_name = '{name}'")
        return building_id

    def add_all_offices_of_building(self, offices_names_list, building_id):
        with self.connection:
            for office in offices_names_list:
                self.cursor.execute("INSERT INTO 'offices_names' (building_id, office_number_or_name) "
                                    "VALUES (?, ?)", (
                    building_id, office
                ))

        self.connection.commit()

    def take_all_offices_of_building(self, building_id):
        offices = self.cursor.execute(f"SELECT office_number_or_name FROM offices_names WHERE "
                                      f"offices_names.building_id = '{building_id}'")
        return offices

    def close(self):
        self.connection.close()
