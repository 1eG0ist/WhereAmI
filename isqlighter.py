import sqlite3


class SQLighter:

    def __init__(self, database_file):
        """Подключение к БД"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_builds(self, build_name=True):
        """Все здания человека"""
        with self.connection:
            return self.cursor.execute(
                "SELECT * FROM 'users_of_WhereAmI' WHERE 'build_name' = ?",
                (build_name,)
            ).fetchall()

    def user_exists(self, user_id):
        """Есть ли юзер в базе"""
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM 'users_of_WhereAmI' WHERE 'user_id' = ?", (user_id,)
            ).fetchall()
            return bool(len(result))

    def add_user(self, user_id, status=True):
        """Добавление нового пользователя"""
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users_of_WhereAmI' ('user_id', status) VALUES (?, ?)",
                (user_id, status)
            )

    def update_user(self, user_id, status):
        """Обновляем статус подписки"""
        return self.cursor.execute(
            "UPDATE 'users_of_WhereAmI' SET 'status' = ? WHERE 'user_id' = ?",
            (status, user_id)
        )

    def close(self):
        self.connection.close()
